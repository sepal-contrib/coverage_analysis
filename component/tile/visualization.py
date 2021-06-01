### TILE SHOWING THE RESULTS

from sepal_ui import sepalwidgets as sw
from sepal_ui import mapping as sm
import ipyvuetify as v

from component.message import ms
from component.scripts import * 
from component import parameter as pm

# create an empty result tile that will be filled with displayable plot, map, links, text
class VisualizationTile(sw.Tile):
    
    def __init__(self, aoi_model, model, **kwargs):
        
        # gather the model
        self.aoi_model = aoi_model
        self.model = model
        
        # widgets
        self.stats = sw.Markdown(pm.stats)
        self.measure = v.Select(label=ms.selection.measure, v_model=None, items=pm.measures)
        self.annual = v.Switch(class_ ="ml-5", label=ms.selection.annual, v_model=False)
        
        # add the map
        self.m = sm.SepalMap()
        
        # create an output alert 
        self.model.bind(self.measure, 'measure').bind(self.annual, 'annual')
       
        # construct the Tile with the widget we have initialized 
        super().__init__(
            id_    = "visualization_widget", # the id will be used to make the Tile appear and disapear
            title  = ms.visualization.title, # the Title will be displayed on the top of the tile
            inputs = [self.stats, self.measure, self.annual, self.m],
            alert = sw.Alert()
        )
        
        self.measure.observe(self._on_change, 'v_model')
        self.annual.observe(self._on_change, 'v_model')
    
    def _on_change(self, change): 
        
        coll = self.model.dataset
        start = self.model.start
        end = self.model.end
        aoi = self.aoi_model.feature_collection
        
        if self.model.measure == 'pixel_count_all':
            
            def unmask(image):
                return image.unmask(1)
            
            reducer = ee.Reducer.count()
            coll = coll.select('B3').map(unmask)
            viz = pm.visParamCount

        if self.model.measure == 'pixel_count':
            reducer = ee.Reducer.count()
            coll = coll.select('B3')
            viz = pm.visParamCount

        elif self.model.measure == 'ndvi_median':
            reducer = ee.Reducer.median()
            coll = coll.select('NDVI')
            viz = pm.visParamNDVIMean
            
        elif self.model.measure == 'ndvi_stdDev':
            reducer = ee.Reducer.median()
            coll = coll.select('NDVI')
            viz = pm.visParamNDVIStdDev
            
        list_of_images = {}
        
        if self.model.annual:

            end, end_y = ee.Date(end).getInfo()['value'], 0
            while end > end_y:
                
                # advance year and just get the year part so we make sure to get the 1st of Jan
                advance_start = ee.Date(start).advance(1, 'year').format('Y')

                # get last day of current year
                end_y = ee.Date(advance_start).advance(-1, 'day').getInfo()['value']

                # catch last iterartion and set to actual end date
                if end_y > end:
                    end_y = end


                # create collection and fill list
                list_of_images[start] = (
                    coll
                        .filterDate(start, end_y)
                        .reduce(reducer).rename(self.model.measure)
                        .clip(aoi)
                )

                # reset start ot new start of the year
                start = ee.Date(advance_start).format('Y-MM-dd').getInfo()

        else:
            list_of_images['total'] = (
                coll
                    .filterDate(start, end)
                    .reduce(reducer).rename(self.model.measure)
                    .clip(aoi)
            )

        # Display the map
        display_result(
            self.aoi_model.feature_collection,
            list_of_images,
            self.m, 
            viz,
            self.model.measure,
            self.model.annual
        )
        
        return
        
        
