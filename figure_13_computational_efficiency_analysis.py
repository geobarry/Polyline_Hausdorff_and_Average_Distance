# -*- coding: utf-8 -*-
"""
Produces data used in Figure 12 & Table 2, comparing computed values and computation time of exact and approximate methods.
"""
##################################################
# PARAMETERS
# folder containing the shapefiles that came with this project
sample_data_folder = r"C:\Users\barry\CaGIS Board Dropbox\cantaloupe bob\Barry\Research\Projects\polyline difference metrics\Hausdorff\git_code\sample_data\original"
# full path to file to save results to (*.csv)
output_file = r"C:\\temp\\figures\\figure_13\\computational_efficiency.csv"
##################################################

from utils_timing import time_test_unequal
from utils_data import get_sample_feature


# COMPUTATIONAL EFFICIENCY ANALYSIS
feat = get_sample_feature("india_bangladesh",sample_data_folder)

nv = len(feat)

n = [20,50,100,200,500,1000,2000,5000,10000,20000,50000]
n = [x for x in n if x < nv]

data = ""
c = min(50000,nv)
for i in range(5):
    if i == 0:
        na = n
        nb = n
        lbl = "n=m"
    elif i == 1:
        na = n
        nb = [int(x / 10) for x in n]
        lbl = "n=10m"
    elif i == 2:
        na = [int(x / 10) for x in n]
        nb = n
        lbl = "m=10n"
    elif i == 3:
        na = [c] * len(n)
        nb = n
        lbl = "n constant"
    elif i == 4:
        na = n
        nb = [c] * len(n)
        lbl = "m constant"
    print(f'working on: {lbl}')
    data += f"{lbl}\n" + time_test_unequal(feat,na,nb) + "\n"

with open(output_file,'w',encoding = 'utf-8') as file:
    file.write(data)

print("finished!")
