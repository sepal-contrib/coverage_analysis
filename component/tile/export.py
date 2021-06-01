# It is strongly suggested to use a separate file to define the tiles of your process and then call them in your notebooks. 
# it will help you to have control over their fonctionalities using object oriented programming
import ee 
ee.Initialize()

from sepal_ui import sepalwidgets as sw
import ipyvuetify as v

from component import scripts
from component.message import ms
from component import parameter as pm

# the tiles should all be heriting from the sepal_ui Tile object 
# if you want to create extra reusable object, you can define them in an extra widget.py file 
class ExportTile(sw.Tile):
    
    def __init__(self, aoi_model, model, **kwargs):

        # gather the model
        self.aoi_model = aoi_model
        self.model = model

        # create an output alert 
        self.output = sw.Alert()

        # widget
        self.stats_exp = sw.Markdown(pm.stats_exp)
        self.count = v.Switch(class_="ml-5", label=ms.export.count, v_model=True)
        self.all = v.Switch(class_="ml-5", label=ms.export.all, v_model=False)
        self.ndvi_median = v.Switch(class_="ml-5", label=ms.export.ndvi_median, v_model=False)
        self.ndvi_stdDev = v.Switch(class_= "ml-5", label=ms.export.ndvi_stdDev, v_model=False)

        # Temporal extent
        self.temporal_exp = sw.Markdown(pm.temporal_exp)
        self.total_exp = v.Switch(class_="ml-5", label=ms.export.total_exp, v_model=True)
        self.annual_exp = v.Switch(class_="ml-5", label=ms.export.annual_exp, v_model=False)
        self.scale = v.TextField(label=ms.export.scale, v_model=30)
        
        # create buttons
        self.asset_btn = sw.Btn(ms.export.asset_btn, 'mdi-download', disabled=True, class_='ma-5')
        self.sepal_btn = sw.Btn(ms.export.sepal_btn, 'mdi-download', disabled=True, class_='ma-5')

        # bindings
        self.model \
            .bind(self.all, 'all') \
            .bind(self.count, 'count') \
            .bind(self.ndvi_median, 'ndvi_median') \
            .bind(self.ndvi_stdDev, 'ndvi_stdDev') \
            .bind(self.annual_exp, 'annual_exp') \
            .bind(self.total_exp, 'total_exp') \
            .bind(self.scale, 'scale') 

        # note that btn and output are not a madatory attributes 
        super().__init__(
            id_ = "export_widget",
            title = ms.export.title,
            inputs = [self.stats_exp, self.all, self.count, self.ndvi_median, self.ndvi_stdDev, self.temporal_exp , self.total_exp, self.annual_exp, self.scale],
            alert = sw.Alert(),
            btn = v.Layout(row=True, children = [self.asset_btn, self.sepal_btn])
        )

        #link the btn 
        self.asset_btn.on_event('click', self._on_asset_click)
        self.sepal_btn.on_event('click', self._on_sepal_click)

    def _select_layers(self):
        
        def unmask(image):
            return image.unmask(1)
            
        coll = self.model.dataset
        start = self.model.start
        end = self.model.end
        aoi = self.aoi_model.feature_collection
        
        dataset = None
        
        if self.model.total_exp:
           
            if self.model.all:
                
                pixel_all = ( 
                    coll
                        .select('B3')
                        .filterDate(start, end)
                        .map(unmask)
                        .reduce(ee.Reducer.count()).rename('count_total')
                        .clip(aoi)
                )
                
                dataset = pixel_all
        
            if self.model.count:
                pixel_total = ( 
                    coll
                        .select('B3')
                        .filterDate(start, end)
                        .reduce(ee.Reducer.count()).rename('cloudfree_count_total')
                        .clip(aoi)
                )
                
                dataset = dataset.addBands(pixel_total) if dataset else pixel_total
            
            if self.model.ndvi_median:
                ndvi_med_total = ( 
                    coll
                        .select('NDVI')
                        .filterDate(start, end)
                        .reduce(ee.Reducer.median()).rename('ndvi_median_total')
                        .clip(aoi)
                )
                
                dataset = dataset.addBands(ndvi_med_total) if dataset else ndvi_med_total
            
            if self.model.ndvi_stdDev:
                ndvi_sd_total = ( 
                    coll
                        .select('NDVI')
                        .filterDate(start, end)
                        .reduce(ee.Reducer.stdDev()).rename('ndvi_stdDev_total')
                        .clip(aoi)
                )
            
                dataset = dataset.addBands(ndvi_sd_total) if dataset else ndvi_sd_total
                
        if self.model.annual_exp:

            end, end_y = ee.Date(end).getInfo()['value'], 0
            while end > end_y:
                
                # advance year and just get the year part so we make sure to get the 1st of Jan
                advance_start = ee.Date(start).advance(1, 'year').format('Y')
                year = ee.Date(start).format('Y').getInfo()
                
                # get last day of current year
                end_y = ee.Date(advance_start).advance(-1, 'day').getInfo()['value']

                # catch last iterartion and set to actual end date
                if end_y > end:
                    end_y = end

                if self.model.all:
                    pixel_all = ( 
                        coll
                            .select('B3')
                            .filterDate(start, end_y)
                            .map(unmask)
                            .reduce(ee.Reducer.count()).rename(f'count_{year}')
                            .clip(aoi)
                    )

                    dataset = dataset.addBands(pixel_all) if dataset else pixel_all
                
                
                if self.model.count:
                    # create collection and fill list
                    pixel_year = (
                        coll
                            .select('B3')
                            .filterDate(start, end_y)
                            .reduce(ee.Reducer.count()).rename(f'pixel_count_{year}')
                            .clip(aoi)
                    )

                    dataset = dataset.addBands(pixel_year) if dataset else pixel_year
                   
                
                if self.model.ndvi_median:
                    
                    # create collection and fill list
                    ndvi_med_year = (
                        coll
                            .select('NDVI')
                            .filterDate(start, end_y)
                            .reduce(ee.Reducer.median()).rename(f'ndvi_median_{year}')
                            .clip(aoi)
                    )

                    dataset = dataset.addBands(ndvi_med_year) if dataset else ndvi_med_year   
                
                
                if self.model.ndvi_stdDev:
                    
                    # create collection and fill list
                    ndvi_sd_year = (
                        coll
                            .select('NDVI')
                            .filterDate(start, end_y)
                            .reduce(ee.Reducer.stdDev()).rename(f'ndvi_stdDev_{year}')
                            .clip(aoi)
                    )

                    dataset = dataset.addBands(ndvi_sd_year) if dataset else ndvi_sd_year 
                    
                    
                # reset start ot new start of the year
                start = ee.Date(advance_start).format('Y-MM-dd').getInfo()
        
        return dataset
        
    def _on_asset_click(self, widget, data, event):
        
        widget.toggle_loading()
        self.sepal_btn.toggle_loading()
        
        dataset = self._select_layers()

        asset_id = scripts.export_to_asset(
            self.aoi_model, 
            dataset, 
            pm.asset_name(self.aoi_model, self.model),
            self.model.scale,
            self.output
        )

        widget.toggle_loading()
        self.sepal_btn.toggle_loading()
        
        return
    
    def _on_sepal_click(self, widget, data, event):
        
        widget.toggle_loading()
        self.asset_btn.toggle_loading()
        
        # get selected layers
        dataset = self._select_layers()
        
        try:
            pathname = scripts.export_to_sepal(
                self.aoi_model, 
                dataset, 
                pm.asset_name(self.aoi_model, self.model), 
                self.model.scale, 
                self.output
            )
        
        except Exception as e:
            self.output.add_live_msg(str(e), 'error')
            
        widget.toggle_loading()
        self.asset_btn.toggle_loading()
        
        return