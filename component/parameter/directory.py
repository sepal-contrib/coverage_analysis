from pathlib import Path

result_dir = Path().home().joinpath('module_results/coverage_analysis')

start = """  
### Start date selection

Pick the date of the timeseries' start.
"""

end = """  
### End date selection

Pick the date of the timeseries' end.
"""

select = """  
### Satellite selection

Select the satellite(s) you want to include for the pre-analysis.
"""

sr = """
### Selection of collection type

Choose between Surface Reflectance or Top-of-Atmosphere collections for the slected satellites.
"""

stats = """  
### Selection of statistics

Select the statistical measure you want to visualize. Switch to annual for per-year calculations.
"""

stats_exp = """  


### Selection of statistical measure(s) to export
"""

temporal_exp = """


### Selection of full time- period and/or inclusion of annual bands 
"""