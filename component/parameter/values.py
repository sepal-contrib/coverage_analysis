#measures = ['pixel_count', 'ndvi_median', 'ndvi_stdDev']

measures = [   
    {'text': 'Cloud-free pixel count', 'value': 'pixel_count'},
    {'text': 'Total pixel count (i.e. scene coverage)', 'value': 'pixel_count_all'},
    {'text': 'NDVI Median', 'value': 'ndvi_median'},
    {'text': 'NDVI Std. Dev.', 'value': 'ndvi_stdDev'}
]

# name of the file in the output directory 
def asset_name(aoi_io, io, fnf=False):
    """return the standard name of your asset/file"""
    

    filename = f"coverage_{aoi_io.get_aoi_name()}_{io.start}_{io.end}"

    if io.l8 != 'NONE':
        filename += f"_L8"

    if io.l7:
        filename += '_L7'

    if io.l5:
        filename += '_L5'

    if io.l4:
        filename += '_L4'

    if io.s2:
        filename += '_S2'

    if io.sr:
        filename += '_SR'
    else:
        filename += '_TOA'
        
    return filename