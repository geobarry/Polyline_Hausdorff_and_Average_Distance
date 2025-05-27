# -*- coding: utf-8 -*-
"""
Constructs images of all synthetic test cases used for algorithm and code validation. 
"""
##################################################
# PARAMETERS
# full path to folder to save results to; this should be an empty folder
save_folder = f"C:\\temp\\figures\\figure_10"
##################################################

from test_utils import case, plot_hausdorff_solution

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
