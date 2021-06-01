Coverage analysis tool for optical data
=======================================

Module using the `sepal_ui <https://github.com/12rambau/sepal_ui>`_ framework and an interactive **Voila** dashboard to create maps of cloud-free observations for major optical satellites as available on Google's Earth Engine Platform.
The framework follows themain ideas from bfasts' countObs and summaryBrick functions as described [here](http://www.loicdutrieux.net/bfastSpatial/#Data_Inventory). 

For B-Fast sepcific requirements read [Schultz et al. 2013](http://dx.doi.org/10.1109/JSTARS.2015.2477473) for further background.

The process is done in 3 steps described in the bellow sections

Select an AOI
-------------

Using the provided AOI selector, select an AOI of your choice between the different methods available in the tool. We provide 3 administration descriptions (from level 0 to 2) and 3 custom shapes (drawn directly on the map, asset or shapefile). 

.. figure:: https://raw.githubusercontent.com/BuddyVolly/coverage_analysis/main/doc/img/aoi_select.png 
    
    aoi selector 
    
.. note::

    If a custom aoi from shape or drawing is selected, you will be able to use it directly and the upload to GEE will be launched in the background
    
Select dataset parameters
-------------------------

To perform the bfast preanalysis you need to provide the tool with key parameters: 

-   **date range**: The extreme dates of your analysis
-   **sensors**: The list of senesors you want to use (landsat family + sentinel 2)
-   **Tier 2**: for the landsat familly sensors you can also include Tier 2 images to the analysis
-   **SR**: wheteher to use Surface reflectance images (SR). default to Top of atmosphere (TOA)

Once all your parameters are selected you can click on the btn to load your dataset

.. figure:: https://raw.githubusercontent.com/BuddyVolly/coverage_analysis/main/doc/img/parameters.png 

Display dataset
---------------

Once you have selected your parameter you can move to the Visualization tile. 
Select a statistical measure to display in the following list:

-   Cloud-free pixel count
-   Total pixel count (i.e. scene coverage)
-   NDVI Median
-   NDVI Std. Dev.

You can also decide to produce stats on yearly basis using the provided switch

.. figure:: https://raw.githubusercontent.com/BuddyVolly/coverage_analysis/main/doc/img/display.png 

.. note::

    The image will be dynamically reevaluate and recentered on every change
    
Export dataset 
--------------

Once you're happy with the information displayed then can be exported to be further used in a GIS software or in a GEE process. The tool provide 2 main exportation options, as an asset(in GEE) or as a Tif file in SEPAL. 

Both use the GEE export system and share the same set of parameter: 

-   statistical measures to export 
    
    -   count of cloud-free observation per pixel
    -   NDVI's median of cloud-free observations
    -   NDVI\'s std. dev. of cloud-free observations
    -   count for all observations per pixel

-   time-period
    
    -   full timespan calculation(s)
    -   annual calculation(s)

-   scale: the scale to us in GEE exported file

.. figure:: https://raw.githubusercontent.com/BuddyVolly/coverage_analysis/main/doc/img/export.png 

.. danger::

    When the image is exported to SEPAL, you cannot quit the application until the downloading is finished.