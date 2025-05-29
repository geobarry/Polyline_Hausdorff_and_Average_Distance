# -*- coding: utf-8 -*-
"""
Constructs images of all synthetic test cases used for algorithm and code validation. 
"""
##################################################
# PARAMETERS
# path to folder to save results to; this should be an empty folder
save_folder = "results\\Hausdorff_still_frames"
##################################################

from test_utils import case, plot_hausdorff_solution
import os

os.makedirs(save_folder,exist_ok = True)

for id in range(case(-1)):
    print(f"GROUP {id}")
    print("...forward")
    A,B = case(id)
    for seg in range(len(A)-1):
        print(f"......seg {seg}")
        plot_hausdorff_solution(A,seg,B,imagefile = f"{save_folder}\\case_{id}_forward_{seg}.png")
    print("...forward")
    B,A = case(id)
    for seg in range(len(A)-1):
        print(f"......seg {seg}")
        plot_hausdorff_solution(A,seg,B,imagefile = f"{save_folder}\\case_{id}_backward_{seg}.png")
print("finished")
