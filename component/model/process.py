# It is strongly suggested to us a separate file to define the io of your tile and process. 
# it will help you to have control over it's fonctionality using object oriented programming

# in python variable are not mutable object (their value cannot be changed in a function)
# Thus use a class to define your input and output in order to have mutable variables

from sepal_ui import model 
from traitlets import Any

class Process (model.Model):
        
    # set up your inputs
    start = Any(None).tag(sync=True)
    end = Any(None).tag(sync=True)
    sensors = Any([]).tag(sync=True)
    t2 = Any(False).tag(sync=True)
    sr = Any(False).tag(sync=True)
    measure = Any('pixel_count').tag(sync=True) 
    annual = Any(False).tag(sync=True) 

    # exports 
    all = Any(False).tag(sync=True) 
    count = Any(True).tag(sync=True) 
    ndvi_median = Any(False).tag(sync=True) 
    ndvi_stdDev = Any(False).tag(sync=True) 
    annual_exp = Any(False).tag(sync=True) 
    total_exp = Any(True).tag(sync=True) 
    scale = Any(30).tag(sync=True) 

    # set up your outputs
    asset_id = Any(None).tag(sync=True) 
    dataset  = Any(None).tag(sync=True)