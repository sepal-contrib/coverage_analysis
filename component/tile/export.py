# It is strongly suggested to use a separate file to define the tiles of your process and then call them in your notebooks.
# it will help you to have control over their fonctionalities using object oriented programming
import ee

from sepal_ui import sepalwidgets as sw
import ipyvuetify as v

from component import scripts
from component.message import cm
from component import parameter as pm


# the tiles should all be heriting from the sepal_ui Tile object
# if you want to create extra reusable object, you can define them in an extra widget.py file
class ExportTile(sw.Tile):
    def __init__(self, aoi_model, model, **kwargs):
        # gather the model
        self.aoi_model = aoi_model
        self.model = model

        # widgets
        self.stats = v.Select(
            label=cm.export.stats,
            v_model=model.stats,
            items=pm.stats,
            chips=True,
            multiple=True,
        )
        self.temps = v.Select(
            label=cm.export.temps,
            v_model=model.temps,
            items=pm.temps,
            chips=True,
            multiple=True,
        )
        self.scale = v.TextField(label=cm.export.scale, v_model=30)

        # create buttons
        self.asset_btn = sw.Btn(
            cm.export.asset_btn, "mdi-download", disabled=True, class_="ma-5"
        )
        self.sepal_btn = sw.Btn(
            cm.export.sepal_btn, "mdi-download", disabled=True, class_="ma-5"
        )

        # bindings
        self.model.bind(self.stats, "stats").bind(self.temps, "temps").bind(
            self.scale, "scale"
        )

        # note that btn and output are not a madatory attributes
        super().__init__(
            id_="export_widget",
            title=cm.export.title,
            inputs=[self.stats, self.temps, self.scale],
            alert=sw.Alert(),
            btn=v.Layout(row=True, children=[self.asset_btn, self.sepal_btn]),
        )

        # link the btn
        self.asset_btn.on_event("click", self._on_asset_click)
        self.sepal_btn.on_event("click", self._on_sepal_click)

    def _select_layers(self):
        def unmask(image):
            return image.unmask(1)

        coll = self.model.dataset
        start = self.model.start
        end = self.model.end
        aoi = self.aoi_model.feature_collection

        dataset = None

        if "total_exp" in self.model.temps:
            if "all" in self.model.stats:
                pixel_all = (
                    coll.select("B3")
                    .filterDate(start, end)
                    .map(unmask)
                    .reduce(ee.Reducer.count())
                    .rename("count_total")
                    .clip(aoi)
                )

                dataset = pixel_all

            if "count" in self.model.stats:
                pixel_total = (
                    coll.select("B3")
                    .filterDate(start, end)
                    .reduce(ee.Reducer.count())
                    .rename("cloudfree_count_total")
                    .clip(aoi)
                )

                dataset = dataset.addBands(pixel_total) if dataset else pixel_total

            if "ndvi_median" in self.model.stats:
                ndvi_med_total = (
                    coll.select("NDVI")
                    .filterDate(start, end)
                    .reduce(ee.Reducer.median())
                    .rename("ndvi_median_total")
                    .clip(aoi)
                )

                dataset = (
                    dataset.addBands(ndvi_med_total) if dataset else ndvi_med_total
                )

            if "ndvi_stdDev" in self.model.stats:
                ndvi_sd_total = (
                    coll.select("NDVI")
                    .filterDate(start, end)
                    .reduce(ee.Reducer.stdDev())
                    .rename("ndvi_stdDev_total")
                    .clip(aoi)
                )

                dataset = dataset.addBands(ndvi_sd_total) if dataset else ndvi_sd_total

        if "annual_exp" in self.model.temps:
            end, end_y = ee.Date(end).getInfo()["value"], 0
            while end > end_y:
                # advance year and just get the year part so we make sure to get the 1st of Jan
                advance_start = ee.Date(start).advance(1, "year").format("Y")
                year = ee.Date(start).format("Y").getInfo()

                # get last day of current year
                end_y = ee.Date(advance_start).advance(-1, "day").getInfo()["value"]

                # catch last iterartion and set to actual end date
                if end_y > end:
                    end_y = end

                if "all" in self.model.stats:
                    pixel_all = (
                        coll.select("B3")
                        .filterDate(start, end_y)
                        .map(unmask)
                        .reduce(ee.Reducer.count())
                        .rename(f"count_{year}")
                        .clip(aoi)
                    )

                    dataset = dataset.addBands(pixel_all) if dataset else pixel_all

                if "count" in self.model.stats:
                    # create collection and fill list
                    pixel_year = (
                        coll.select("B3")
                        .filterDate(start, end_y)
                        .reduce(ee.Reducer.count())
                        .rename(f"pixel_count_{year}")
                        .clip(aoi)
                    )

                    dataset = dataset.addBands(pixel_year) if dataset else pixel_year

                if "ndvi_median" in self.model.stats:
                    # create collection and fill list
                    ndvi_med_year = (
                        coll.select("NDVI")
                        .filterDate(start, end_y)
                        .reduce(ee.Reducer.median())
                        .rename(f"ndvi_median_{year}")
                        .clip(aoi)
                    )

                    dataset = (
                        dataset.addBands(ndvi_med_year) if dataset else ndvi_med_year
                    )

                if "ndvi_stdDev" in self.model.stats:
                    # create collection and fill list
                    ndvi_sd_year = (
                        coll.select("NDVI")
                        .filterDate(start, end_y)
                        .reduce(ee.Reducer.stdDev())
                        .rename(f"ndvi_stdDev_{year}")
                        .clip(aoi)
                    )

                    dataset = (
                        dataset.addBands(ndvi_sd_year) if dataset else ndvi_sd_year
                    )

                # reset start ot new start of the year
                start = ee.Date(advance_start).format("Y-MM-dd").getInfo()

        return dataset

    def _on_asset_click(self, widget, data, event):
        widget.toggle_loading()

        # check inputs
        if not self.alert.check_input(self.model.stats, cm.process.no_input):
            return widget.toggle_loading()
        if not self.alert.check_input(self.model.temps, cm.process.no_input):
            return widget.toggle_loading()
        if not self.alert.check_input(self.model.scale, cm.process.no_input):
            return widget.toggle_loading()

        dataset = self._select_layers()

        asset_id = scripts.export_to_asset(
            self.aoi_model,
            dataset,
            pm.asset_name(self.aoi_model, self.model),
            self.model.scale,
            self.alert,
        )

        widget.toggle_loading()

        return

    def _on_sepal_click(self, widget, data, event):
        widget.toggle_loading()

        # check inputs
        if not self.alert.check_input(self.model.stats, cm.process.no_input):
            return widget.toggle_loading()
        if not self.alert.check_input(self.model.temps, cm.process.no_input):
            return widget.toggle_loading()
        if not self.alert.check_input(self.model.scale, cm.process.no_input):
            return widget.toggle_loading()

        # get selected layers
        dataset = self._select_layers()

        try:
            pathname = scripts.export_to_sepal(
                self.aoi_model,
                dataset,
                pm.asset_name(self.aoi_model, self.model),
                self.model.scale,
                self.alert,
            )

        except Exception as e:
            self.output.add_live_msg(str(e), "error")

        widget.toggle_loading()

        return
