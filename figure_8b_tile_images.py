# -*- coding: utf-8 -*-
"""
Creates figure from images constructed in figure_8a....py
"""
##################################################
# PARAMETERS
# full path to folder containing output images produced by "figure_10a_construct_images.py"
folder_containing_images = "results\\animation_frames"
# folder to save final combined figure
fig_8_output_file = "results\\figure_8.png"
##################################################

from PIL import Image, ImageDraw, ImageFont

def create_figure(case_list,forward_list,seg_list,k_list,name_list,row_n,col_n,out_file):
    file_list = zip(case_list,forward_list,seg_list,k_list)
    file_list = [f"{folder_containing_images}\\{c}_{seg}{f}\\k_0_{k:03d}.png" for c,f,seg,k in file_list]

    image_list = [Image.open(x) for x in file_list]
    size = image_list[0].size
    print(f'size: {size}')
    # create combined image
    wd = size[0]
    ht = size[1]
    text_ht = 90
    margin = 120
    row_ht = ht + text_ht + 2*margin
    new_image = Image.new('RGB',(col_n*wd,row_n*row_ht),color = (255,255,255))
    draw = ImageDraw.Draw(new_image)

    for row in range(row_n):
        for col in range(col_n):
            id = col_n * row + col
            new_image.paste(image_list[id],(col * wd,margin + row * row_ht))
            # label
            lbl = chr(ord('a') + id)
            txt_x = (col + 1/2) * wd
            txt_y = margin + row * row_ht + ht
            font = ImageFont.truetype("arial.ttf",size = 65)
            draw.text((txt_x,txt_y),f"({lbl})",font = font,fill = (0,0,0))
            # description
            font = ImageFont.truetype("arial.ttf",size = 52)
            txt_y = margin + row * row_ht
            draw.text((txt_x,txt_y),f"{name_list[id]}",font = font,fill = (0,0,0),anchor="ms")
            new_image.save(out_file)

case_list = [0,2,5,4,8,10]
forward_list = ["","","","","",""] # "" or "_reverse" 
seg_list = [1,1,1,1,0,0]
k_list=[900,500,900,900,900,900]
name_list=["Hangouët example","parallel segment","multiple parallel segments","overlapping segment","loop","multiple complexities"]
create_figure(case_list, forward_list, seg_list, k_list, name_list, 2, 3, fig_8_output_file)





