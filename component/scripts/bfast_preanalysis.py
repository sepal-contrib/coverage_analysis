import ee

from .helpers import *
from .cloud_masking import cloud_mask_S2

ee.Initialize()


def analysis(aoi, start, end, sensors, t2, sr):
    coll = None
    coll_type = "SR" if sr else "TOA"

    if "l8" in sensors:
        # create collection (with masking) and add NDVI
        coll = create_collection(
            ee.ImageCollection(f"LANDSAT/LC08/C01/T1_{coll_type}"),
            t2,
            start,
            end,
            aoi,
            sr,
        ).map(addNDVIL8)

    if "l7" in sensors:
        # create collection (with masking) and add NDVI
        l7_coll = create_collection(
            ee.ImageCollection(f"LANDSAT/LE07/C01/T1_{coll_type}"),
            t2,
            start,
            end,
            aoi,
            sr,
        ).map(addNDVILsat)

        # merge collection
        coll = coll.merge(l7_coll) if coll else l7_coll

    if "l5" in sensors:
        # create collection (with masking) and add NDVI
        l5_coll = create_collection(
            ee.ImageCollection(f"LANDSAT/LT05/C01/T1_{coll_type}"),
            t2,
            start,
            end,
            aoi,
            sr,
        ).map(addNDVILsat)

        # merge collection
        coll = coll.merge(l5_coll) if coll else l5_coll

    if "l4" in sensors:
        # create collection (with masking) and add NDVI
        l4_coll = create_collection(
            ee.ImageCollection(f"LANDSAT/LT04/C01/T1_{coll_type}"),
            t2,
            start,
            end,
            aoi,
            sr,
        ).map(addNDVILsat)

        # merge collection
        coll = coll.merge(l4_coll) if coll else l4_coll

    if "s2" in sensors:
        # define collection name based on SR or TOA

        s2_coll_name = "S2_SR" if sr else "S2"

        # Import and filter S2 SR.
        s2_coll = (
            ee.ImageCollection(f"COPERNICUS/{s2_coll_name}")
            .filterBounds(aoi)
            .filterDate(start, end)
        )

        # Import and filter s2cloudless.
        s2_cloudless_coll = (
            ee.ImageCollection("COPERNICUS/S2_CLOUD_PROBABILITY")
            .filterBounds(aoi)
            .filterDate(start, end)
        )

        # Join the filtered s2cloudless collection to the SR collection by the 'system:index' property.
        joined_coll = ee.ImageCollection(
            ee.Join.saveFirst("s2cloudless").apply(
                **{
                    "primary": s2_coll,
                    "secondary": s2_cloudless_coll,
                    "condition": ee.Filter.equals(
                        **{"leftField": "system:index", "rightField": "system:index"}
                    ),
                }
            )
        )

        s2_coll = (
            joined_coll.map(cloud_mask_S2) if sr else joined_coll.map(cloud_mask_S2)
        )
        s2_coll = s2_coll.map(addNDVIS2)

        # merge collection
        coll = coll.merge(s2_coll) if coll else s2_coll

    return coll
