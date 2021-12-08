### TILE SHOWING THE RESULTS
from datetime import datetime as dt

from sepal_ui import sepalwidgets as sw
from sepal_ui import mapping as sm
from sepal_ui.scripts import utils as su
import ipyvuetify as v

from component.message import ms
from component import scripts as cs
from component import parameter as pm

# create an empty result tile that will be filled with displayable plot, map, links, text
class SelectionTile(sw.Tile):
    def __init__(self, aoi_model, model, viz_tile, export_tile, **kwargs):

        # gather the model
        self.aoi_model = aoi_model
        self.model = model
        self.viz_tile = viz_tile
        self.export_tile = export_tile

        # widgets
        w_time_title = v.Html(
            tag="H3", class_="mt-3", children=[ms.selection.time_range]
        )
        self.start_picker = sw.DatePicker(label=ms.selection.start)
        self.end_picker = sw.DatePicker(label=ms.selection.end)
        w_time_range = v.Layout(row=True, children=[self.start_picker, self.end_picker])

        w_collection_title = v.Html(
            tag="H3", class_="mt-3", children=[ms.selection.collection]
        )
        self.sensors = v.Select(
            label=ms.selection.sensor,
            items=pm.sensors,
            v_model=None,
            chips=True,
            multiple=True,
        )
        self.t2 = v.Switch(class_="ml-5", label=ms.selection.t2, v_model=False)
        self.sr = v.Switch(class_="ml-5", label=ms.selection.sr, v_model=False)

        self.model.bind(self.start_picker, "start").bind(self.end_picker, "end").bind(
            self.sensors, "sensors"
        ).bind(self.t2, "t2").bind(self.sr, "sr")

        # construct the Tile with the widget we have initialized
        super().__init__(
            id_="selection_widget",  # the id will be used to make the Tile appear and disapear
            title=ms.selection.title,  # the Title will be displayed on the top of the tile
            inputs=[
                w_time_title,
                w_time_range,
                w_collection_title,
                self.sensors,
                self.t2,
                self.sr,
            ],
            btn=sw.Btn(ms.selection.btn),
            alert=sw.Alert(),
        )

        # now that the Tile is created we can link it to a specific function
        self.btn.on_event("click", self._on_run)

    @su.loading_button(debug=False)
    def _on_run(self, widget, data, event):

        # check that the input that you're gonna use are set (Not mandatory)
        if not self.alert.check_input(self.aoi_model.name, ms.process.no_aoi):
            return
        if not self.alert.check_input(self.model.sensors, ms.process.no_sensors):
            return
        if not self.alert.check_input(self.model.start, ms.process.no_date):
            return
        if not self.alert.check_input(self.model.end, ms.process.no_date):
            return

        # check the dates
        d_format = "%Y-%m-%d"
        if not dt.strptime(self.model.start, d_format) < dt.strptime(
            self.model.end, d_format
        ):
            self.alert.add_msg(ms.process.no_order, "error")
            return

        dataset = cs.analysis(
            self.aoi_model.feature_collection,
            self.model.start,
            self.model.end,
            self.model.sensors,
            self.model.t2,
            self.model.sr,
        )

        # change the model values as its a mutable object
        # useful if the model is used as an input in another tile
        self.model.dataset = dataset

        # release the export btn
        self.export_tile.asset_btn.disabled = False
        self.export_tile.sepal_btn.disabled = False

        # conclude the computation with a message
        self.alert.add_live_msg(ms.process.end_computation, "success")

        return
