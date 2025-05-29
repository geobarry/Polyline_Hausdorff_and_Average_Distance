# -*- coding: utf-8 -*-
"""
This module constructs image frames for animations, which were combined into videos for assessment using ffmpeg.
Frames are saved to the folder "results\animation_frames".
Image frames used as figures in the manuscript are as follows:

Figure 6: 7_0\k_0_750.png
Figure 7: 5_1\k_0_360.png

If you wish to reconstruct videos with ffmpeg (usually comes with windows, maybe other os's also; if not, install from https://ffmpeg.org/):
 - open a command prompt
 - cd into the folder with your image sequence
 - enter the following command into a command prompt:

ffmpeg -framerate 30 -i k_%d.png -c:v libx264 -r 30 -pix_fmt yuv420p animation.mp4

Parameters in above that you might to want to change:
 10	               input images per second
 k_%d.png          file name; %d will be replaced by numbers
 -r 30             output frames per second
 animation.mp4     output file name
"""
base_image_folder = r'results\animation_frames'
cases = [(5,1,False),(7,0,False)] # Parameters to create figures 6, 7=12

import test_utils as tu
import os
import numpy as np

# uncomment the following to create animations for all test cases
# n = tu.case(-1)
# cases = []
# for i in range(n):
#     A,B = tu.case(i)    
#     for j in range(len(A)-1):
#         cases.append((i,j,False))
#     for j in range(len(B)-1):
#         cases.append((i,j,True))




# define animation parameters
dpi = 200 # default image size is 6" x 4"
k_buffer = 0.005 # overlap between successive distance function sections
steps = 200 # number of frames to produce

#wipe outputs folder
if not os.path.isdir(base_image_folder):      
    os.mkdir(base_image_folder)

#loop over all cases
for case_num, seg_num, rev in cases:
    # setup case number folder and file information
    rev_text = "_reverse" if rev else ""
    folder = f"{case_num}_{seg_num}{rev_text}"
    print("case: "+str(folder))
    case_num_folder = os.path.join(base_image_folder,folder)
    if not os.path.isdir(case_num_folder):              
        os.mkdir(case_num_folder)
    image_file_base = os.path.join(case_num_folder, "k_")

    # get data for given case
    A,B = tu.case(case_num)
    if rev:
        A,B = B,A

    # establish k values for each frame in the animation
    step_size = 1/steps
    # parameterbs_list = tuple(round(k,2) for k in np.arange(0, 1+step_size, step_size))

    def generate_plot(plot_num, steps):
            step_text = f"{(plot_num/steps):.3f}".replace(".","_")
            imagefile = f"{image_file_base}{step_text}.png"
            
            tu.plot_hausdorff_solution(A, seg_num, B, 
                                show_labels = True, 
                                k=plot_num/steps,
                                k_buffer = k_buffer,
                                imagefile = imagefile,
                                dpi = dpi,
                                k_use_hausdorff=False,
                                stop_distance_function_at_k=True)
    for i in range(steps+1):
        if i % 25 == 0:
            print("generating frame {} of {}".format(i,steps))
        generate_plot(i,steps)
print("finished!!!")