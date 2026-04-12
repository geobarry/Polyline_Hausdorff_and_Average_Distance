# -*- coding: utf-8 -*-
"""
Produces data used in Figure 14 & Table 3, comparing computed values and computation time of exact and approximate methods
for increasing precision of approximation (i.e. decreasing vertex spacing). This will take a while to run - you may want to 
decrease the value of the "levels" parameter for faster results.
"""
##################################################
# PARAMETERS
# levels of increasing precision for approximations:
#  - use 5 levels for code testing, will take about 5-10 minutes
#  - use 13 levels for manuscript data reproduction
levels = 5
# folder containing the shapefiles that came with this project
sample_data_folder = r"sample_data\original"
# path to file to save results to (*.csv)
output_file = "results\\figure_14_exact_vs_approximate.csv"
##################################################

from utils_timing import compare_with_approx
from utils_data import get_sample_feature

feat_list = ["manhattan","lake_shelbyville","cannonball","india_bangladesh"]

output = ''

for name in feat_list:
    print(f"Processing feature {name}:")
    feat = get_sample_feature(name,sample_data_folder)
    y = 10 ** (1/4)
    spacings = [1000/(y ** x) for x in range(levels)]
    output += name + ",original to simplified\n" + compare_with_approx(feat,spacings,reverse = False) + "\n"
    output += name + ",simplified to original\n" + compare_with_approx(feat,spacings,reverse = True) + "\n"

with open(output_file,'w',encoding = 'utf-8') as file:
    file.write(output)

print("finished!")