# -*- coding: utf-8 -*-
"""
Produces data used in Figure 12 & Table 2, comparing computed values and computation time of exact and approximate methods.
"""
##################################################
# PARAMETERS
# folder containing the shapefiles that came with this project
sample_data_folder = r"C:\Users\barry\CaGIS Board Dropbox\cantaloupe bob\Barry\Research\Projects\polyline difference metrics\Hausdorff\git_code\sample_data\original"
# full path to file to save results to (*.csv)
output_file = r"C:\\temp\\figures\\figure_12\\timing_comparison.csv"
# use 5 levels for code testing, will take about 5 minutes; change to 13 for manuscript data reproduction
levels = 5
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