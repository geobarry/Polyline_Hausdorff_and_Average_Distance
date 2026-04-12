# -*- coding: utf-8 -*-
"""
Creates animations
"""
##################################################
# PARAMETERS
# full path to folder containing output images produced by "figure_10a_construct_images.py"
folder_containing_images = "results\\animation_frames"
# folder to save final combined figure
out_folder = "animations\\"
##################################################

import os
import imageio.v2 as iio

#wipe outputs folder
if not os.path.isdir(out_folder):      
    os.mkdir(out_folder)

case_list = [0,2,5,4,8,10]
forward_list = ["","","","","",""] # "" or "_reverse" 
seg_list = [1,1,1,1,0,0]
folder_list = zip(case_list,forward_list,seg_list)
folder_list = [f"{folder_containing_images}\\{c}_{seg}{f}\\" for c,f,seg in folder_list]
name_list=["Hangouët example","parallel segment","multiple parallel segments","overlapping segment","loop","multiple complexities"]

for folder,name in zip(folder_list,name_list):
    file_list=os.listdir(folder)    
    print(f"{folder} :: {len(file_list)}")
    
    out_file=f"{out_folder}{name.replace(" ","_")}.mp4"
    with iio.get_writer(out_file,codec='libx264',fps = 30) as writer:
        for file in file_list:
            filepath = f"{folder}\\{file}"
            img=iio.imread(filepath)
            writer.append_data(img)
    print(f'video saved to {out_file}')


#writer = imageio.get_writer('test.mp4', fps=30, codec='mjpeg', quality=10, pixelformat='yuvj444p')
    