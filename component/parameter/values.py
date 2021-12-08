# measures = ['pixel_count', 'ndvi_median', 'ndvi_stdDev']

measures = [
    {"text": "Cloud-free pixel count", "value": "pixel_count"},
    {"text": "Total pixel count (i.e. scene coverage)", "value": "pixel_count_all"},
    {"text": "NDVI Median", "value": "ndvi_median"},
    {"text": "NDVI Std. Dev.", "value": "ndvi_stdDev"},
]

sensors = [
    {"text": "Landsat 8", "value": "l8"},
    {"text": "Landsat 7", "value": "l7"},
    {"text": "Landsat 5", "value": "l5"},
    {"text": "Landsat 4", "value": "l4"},
    {"text": "Sentinel 2", "value": "s2"},
]

stats = [
    {"text": "count of cloud-free observation per pixel", "value": "count"},
    {"text": "NDVI's median of cloud-free observations", "value": "ndvi_median"},
    {"text": "NDVI's std. dev. of cloud-free observations", "value": "ndvi_stdDev"},
    {"text": "count for all observations per pixel", "value": "all"},
]

temps = [
    {"text": "full timespan calculation(s)", "value": "total_exp"},
    {"text": "annual calculation(s)", "value": "annual_exp"},
]

# name of the file in the output directory
def asset_name(aoi_model, model, fnf=False):
    """return the standard name of your asset/file"""

    filename = f"coverage_{aoi_model.name}_{model.start}_{model.end}"

    if "l8" in model.sensors:
        filename += f"_L8"

    if "l7" in model.sensors:
        filename += "_L7"

    if "l5" in model.sensors:
        filename += "_L5"

    if "l4" in model.sensors:
        filename += "_L4"

    if "s2" in model.sensors:
        filename += "_S2"

    if model.sr:
        filename += "_SR"
    else:
        filename += "_TOA"

    return filename
