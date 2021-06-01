### TILE SHOWING THE RESULTS

from sepal_ui import sepalwidgets as sw
from sepal_ui import mapping as sm
from sepal_ui.scripts import utils as su
import ipyvuetify as v

from component.message import ms
from component.scripts import * 
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
        self.start = sw.Markdown(pm.start)
        self.start_picker = sw.DatePicker(label='Start date')
        self.end = sw.Markdown(pm.end)
        self.end_picker = sw.DatePicker(label='End date')
        
        self.select = sw.Markdown(pm.select)
        self.l8 = v.Switch(class_  = "ml-5",label   = ms.selection.l8,v_model = False)
        self.l7 = v.Switch(class_  = "ml-5",label   = ms.selection.l7,v_model = False)
        self.l5 = v.Switch(class_  = "ml-5",label   = ms.selection.l5,v_model = False)
        self.l4 = v.Switch(class_  = "ml-5",label   = ms.selection.l4,v_model = False)
        self.t2 = v.Switch(class_  = "ml-5",label   = ms.selection.t2,v_model = False)
        self.s2 = v.Switch(class_  = "ml-5",label   = ms.selection.s2,v_model = False)
                           
        self.sr_mess = sw.Markdown(pm.sr)
        self.sr = v.Switch(class_  = "ml-5",label   = ms.selection.sr,v_model = False)
        
        self.model \
            .bind(self.start_picker, 'start')  \
            .bind(self.end_picker, 'end')  \
            .bind(self.l8, 'l8') \
            .bind(self.l7, 'l7') \
            .bind(self.l5, 'l5') \
            .bind(self.l4, 'l4') \
            .bind(self.t2, 't2') \
            .bind(self.s2, 's2') \
            .bind(self.sr, 'sr')            
        
        # construct the Tile with the widget we have initialized 
        super().__init__(
            id_    = "selection_widget", # the id will be used to make the Tile appear and disapear
            title  = ms.selection.title, # the Title will be displayed on the top of the tile
            inputs = [self.start, self.start_picker, self.end, self.end_picker, 
                      self.select, self.l8, self.l7, self.l5, self.l4, self.t2, self.s2,
                      self.sr_mess, self.sr],
            btn    = sw.Btn(),
            alert = sw.Alert()
        )
        
        # now that the Tile is created we can link it to a specific function
        self.btn.on_event("click", self._on_run)
        
    
    @su.loading_button(debug=False)
    def _on_run(self, widget, data, event): 
            
        # check that the input that you're gonna use are set (Not mandatory)
        if not self.alert.check_input(self.aoi_model.name, ms.process.no_aoi): return widget.toggle_loading()
                   
        dataset = analysis(
            self.aoi_model.feature_collection,
            self.model.start,
            self.model.end,
            self.model.l8,
            self.model.l7,
            self.model.l5,
            self.model.l4,
            self.model.t2,
            self.model.s2,
            self.model.sr,
        )

        # change the model values as its a mutable object 
        # useful if the model is used as an input in another tile
        self.model.dataset = dataset

        # release the export btn
        self.export_tile.asset_btn.disabled = False
        self.export_tile.sepal_btn.disabled = False

        # conclude the computation with a message
        self.alert.add_live_msg(ms.process.end_computation, 'success')
        
        return