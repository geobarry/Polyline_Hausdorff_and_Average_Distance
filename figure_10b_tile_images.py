# -*- coding: utf-8 -*-
"""
Combines images produced by "figure_10a_construct_images.py". 
"""
##################################################
# PARAMETERS
# full path to folder containing output images produced by "figure_10a_construct_images.py"
folder_containing_images = r"C:\temp\figures\figure_10"
# folder to save final combined figure
save_folder = r"C:\temp\figures\figure_10"
##################################################

from PIL import Image, ImageDraw, ImageFont
file_list = []
case_list = [8,10,5,10,4,7]
forward_list = ["f","b","f","b","f","f"]
forward_list = ["forward" if x == "f" else "backward" for x in forward_list]
print(f'forward_list: {forward_list}')
seg_list = [0,2,1,6,1,0]
file_list = zip(case_list,forward_list,seg_list)
file_list = [f"{folder_containing_images}\\case_{c}_{f}_{seg}.png" for c,f,seg in file_list]
print(f'file_list: {file_list}')
image_list = [Image.open(x) for x in file_list]
size = image_list[0].size
print(f'size: {size}')
# create combined image
wd = size[0]
ht = size[1]
text_ht = 90
margin = 120
row_ht = ht + text_ht + margin
new_image = Image.new('RGB',(3*wd,2*row_ht),color = (255,255,255))
draw = ImageDraw.Draw(new_image)
font = ImageFont.truetype("arial.ttf",size = 90)
for row in range(2):
    for col in range(3):
        id = 3 * row + col
        lbl = chr(ord('a') + id)
        new_image.paste(image_list[id],(col * wd,row * row_ht))
        txt_x = (col + 1/2) * wd
        txt_y = row * row_ht + ht
        draw.text((txt_x,txt_y),f"({lbl})",font = font,fill = (0,0,0))
f = f"{save_folder}\\figure_10.png"
new_image.save(f)