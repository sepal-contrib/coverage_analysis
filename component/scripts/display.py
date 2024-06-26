import ee
import ipyvuetify as v

from component.message import cm
from component import parameter as pm


def display_result(ee_aoi, dataset, m, vis, measure, annual):
    """
    Display the results on the map

    Args:
        ee_aoi: (ee.Geometry): the geometry of the aoi
        dataset (ee.Image): the image the display
        m (sw.SepalMap): the map used for the display
        db (bool): either to use the db scale or not

    Return:
        (sw.SepalMap): the map with the different layers added
    """

    for layer in m.layers:
        if layer.name != "CartoDB.DarkMatter":
            m.remove_layer(layer)

    try:
        m.remove_colorbar()
    except:
        pass

    if measure == "pixel_count":
        _max = 20 if annual else 100
        vis.update(max=_max)

    if measure == "pixel_count_all":
        _max = 40 if annual else 200
        vis.update(max=_max)

    # AOI borders in blue
    empty = ee.Image().byte()
    outline = empty.paint(featureCollection=ee_aoi, color=1, width=3)

    # Zoom to AOI
    m.zoom_ee_object(ee_aoi.geometry())

    for year in sorted(dataset.keys()):
        label = year[:4] if annual else "total"
        # if dataset[year].reduceRegion(ee.Reducer.max(), ee_aoi.geometry(), 5000).getInfo():
        m.addLayer(dataset[year], vis, f"{measure} {label}")

    m.add_colorbar(
        colors=vis["palette"],
        vmin=vis["min"],
        vmax=vis["max"],
        layer_name="Colorbar",
        position="bottomleft",
    )

    return
