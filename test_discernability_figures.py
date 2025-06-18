# -*- coding: utf-8 -*-
"""
Created on Tue Dec 26 21:30:19 2023

@author: Administrator
"""

folder = r"C:\CaGIS Board Dropbox\cantaloupe bob\Research\Conferences\CaGIS\2024 Columbus\figures"
filename = "Perkal.png"
image_path = f"{folder}\\{filename}"
dpi = 600

import matplotlib.pyplot as plt
import numpy
import math


def pot_of_gold(v,d,b):
    """
        v   :   (float,float)
        d   :   float (distance)
        b  :   float (in degrees)
    """  
    rad = math.radians(b)
    x = v[0] + d * math.sin(rad)
    y = v[1] + d * math.cos(rad)
    return (x,y)    

def circle_section(C,d,b1,b2):
    """
        C   :   (float,float)
        d   :   float (distance)
        b1,b2  :   float (in degrees)
    """
    r = []
    b1 = math.radians(b1)
    b2 = math.radians(b2)
    for rad in numpy.linspace(b1,b2):
        x = C[0] + d * math.sin(rad)
        y = C[1] + d * math.cos(rad)
        r.append((x,y))
    return r

def line_section(v1,v2,n=5):
    r = []
    for id in range(n):
        x = v1[0] + (v2[0] - v1[0]) * id / n
        y = v1[1] + (v2[1] - v1[1]) * id / n
        r.append((x,y))
    r.append(v2)
    return r
    

def Perkal_figure():
    """Illustrate problems with Perkal method"""
    # CREATE A FIGURE WITH A CLEAR NECK
    fig, ax = plt.subplots(figsize = (9,3),dpi = dpi)
    # Create polyline
    poly = []
    poly = circle_section((57,5),5,180,360)
    poly += circle_section((57,25),15,180,0)
    poly += line_section((57,40),(43,40))
    poly += circle_section((43,25),15,360,180)
    poly += circle_section((43,5),5,0,180)
    
    # Draw polyline
    x,y = zip(*poly)
    ax.plot(x,y,color = "darkslateblue")
    
    # Create buffer line
    poly = circle_section((57,0),3,180,0)
    poly += circle_section((57,5),2,180,360)
    poly += circle_section((57,25),18,180,0)
    poly += line_section((57,43),(43,43))
    poly += circle_section((43,25),18,360,180)
    poly += circle_section((43,5),2,0,180)
    poly += circle_section((43,0),3,360,180)
    poly += circle_section((43,5),8,180,0)
    poly += circle_section((43,25),12,180,360)
    poly += line_section((43,37),(57,37))
    poly += circle_section((57,25),12,0,180)
    poly += circle_section((57,5),8,360,180)
    
    # Draw buffer line
    x,y = zip(*poly)
    ax.plot(x,y,color = "red", linestyle = "dotted", linewidth = 1)
    
    # Create legend
    ax.plot([35,35],[48,50],color = "black")
    ax.plot([35,41],[49,49],color = "black")
    ax.plot([41,41],[48,50],color = "black")
    ax.text(45,49,"minimum discernible gap",va = "center")
    
    # Create label
    ax.text(50,-10,"(a)", ha = "center")

    # NARROW WEDGE
    poly = line_section((100,0),(105,40))
    poly += line_section((105,40),(110,0))
    
    # Draw polyline
    x,y = zip(*poly)
    ax.plot(x,y,color = "darkslateblue")

    # Create buffer
    theta = math.degrees(math.atan2(40,5))
    v1 = pot_of_gold((103,24),3,theta)
    v2 = pot_of_gold((100,0),3,theta)
    poly = line_section(v1,v2)
    poly += circle_section((100,0),3,180-theta,360-theta)
    v1 = pot_of_gold((100,0),3,360-theta)
    v2 = pot_of_gold((105,40),3,360-theta)
    poly += line_section(v1,v2)
    poly += circle_section((105,40),3,360-theta,360+theta)
    v1 = pot_of_gold((105,40),3,theta)
    v2 = pot_of_gold((110,0),3,theta)
    poly += line_section(v1,v2)
    poly += circle_section((110,0),3,theta,180+theta)
    v1 = pot_of_gold((110,0),3,180+theta)
    v2 = pot_of_gold((107,24),3,180+theta)
    poly += line_section(v1,v2)
      
    # Draw buffer line
    x,y = zip(*poly)
    ax.plot(x,y,color = "red", linestyle = "dotted", linewidth = 1)

    # Create label
    ax.text(105,-10,"(b)", ha = "center")

    # ACUTE ANGLE MORE COMPLICATED
    cx = 180
    theta = math.degrees(math.atan2(28,3.5))

    # Create polyline
    poly = line_section((cx-5,0),(cx-1.5,28))
    poly += line_section((cx-1.5,28),(cx-2.5,36))
    rad = ((2.5**2) + (0.625**2))**0.5
    C = pot_of_gold((cx-2.5,36),rad,theta)
    poly += circle_section(C,rad,360-theta,360+theta)
    poly += line_section((cx+2.5,36),(cx+1.5,28))
    poly += line_section((cx+1.5,28),(cx+5,0))

    # Draw polyline
    x,y = zip(*poly)
    ax.plot(x,y,color = "darkslateblue")
    
    # Create buffer line
    v1 = pot_of_gold((cx-2,24),3,180-theta)
    v2 = pot_of_gold((cx-5,0),3,180-theta)
    poly = line_section(v1,v2)
    poly += circle_section((cx-5,0),3,180-theta,360-theta)
    v1 = pot_of_gold((cx-5,0),3,360-theta)
    dx_inflection = (9+0.375 ** 2)**0.5
    v2 = (cx-1.5-dx_inflection,28)
    poly += line_section(v1,v2)
    v1 = v2
    v2 = pot_of_gold((cx-2.5,36),3,180+theta)
    poly += line_section(v1,v2)
    poly += circle_section(C,rad+3,360-theta,360+theta)
    v1 = pot_of_gold((cx+2.5,36),3,180-theta)
    v2 = (cx+1.5+dx_inflection,28)
    poly += line_section(v1,v2)
    v1 = v2
    v2 = pot_of_gold((cx+5,0),3,theta)
    poly += line_section(v1,v2)
    poly += circle_section((cx+5,0),3,theta,180+theta)
    v1 = pot_of_gold((cx+5,0),3,180+theta)
    v2 = pot_of_gold((cx+2,24),3,180+theta)
    poly += line_section(v1,v2)
    
    # Draw buffer line
    x,y = zip(*poly)
    ax.plot(x,y,color = "red", linestyle = "dotted", linewidth = 1)

    # Create label
    ax.text(cx,-10,"(d)", ha = "center")

    # VERY GENTLE ANGLE
    cx = 145
    poly = line_section((cx,0),(cx-5,20))
    poly += line_section((cx-5,20),(cx,40))
    
    # Draw polyline
    x,y = zip(*poly)
    ax.plot(x,y,color = "darkslateblue")
    
    # Create buffer
    theta = math.degrees(math.atan2(20,5))    
    v1 = pot_of_gold((cx-5.2,22),3,theta)
    v2 = pot_of_gold((cx,0),3,theta)
    poly = line_section(v1,v2)
    poly += circle_section((cx,0),3,theta,180+theta)
    v1 = pot_of_gold((cx,0),3,180+theta)
    v2 = pot_of_gold((cx-5,20),3,180+theta)
    poly += line_section(v1,v2)
    poly += circle_section((cx-5,20),3,180+theta,360-theta)
    v1 = pot_of_gold((cx-5,20),3,360-theta)
    v2 = pot_of_gold((cx,40),3,360-theta)
    poly += line_section(v1,v2)
    poly += circle_section((cx,40),3,360-theta,540-theta)
    v1 = pot_of_gold((cx,40),3,180-theta)
    v2 = pot_of_gold((cx-5.2,18),3,180-theta)
    poly += line_section(v1,v2)

    # Draw buffer line
    x,y = zip(*poly)
    ax.plot(x,y,color = "red", linestyle = "dotted", linewidth = 1)

    # Create label
    ax.text(cx+1,-10,"(c)", ha = "center")
    
    # Clean figure
    plt.axis('equal')
    plt.axis("off")

def discernability_regions_figure(image_path,version = 1):
    dpi = 600
    fig, ax = plt.subplots(figsize = (5,2),dpi = dpi)
    dmin = 10
    lmin = 20
    tol = 1
    # draw boundary between regions of discernability and indiscernibility
    if version == 1: # "square"
        border = [
                (lmin,0),
                (lmin,dmin),
                (lmin * 2,dmin)
            ]
    else        :
        border = [
                (tol,0),
                (lmin,dmin),
                (lmin * 2,dmin)
            ]

    x,y = zip(*border)
    ax.plot(x,y)

    # dotted line
    if version == 3:
        border = [(lmin,0),(lmin,dmin)]
        x,y = zip(*border)
        ax.plot(x,y,"--",color=u"#1f77b4")

    ax.set_xlim((0,lmin * 2))
    ax.set_ylim((0,dmin * 1.4))
    plt.xlabel(u"path length ($\u2113$)",loc = "left",labelpad = -12)
    plt.ylabel(u"distance ($d$)",loc="bottom",labelpad = -21)
    plt.xticks([20],[u"$\u2113_{min}$"])
    ax.tick_params(direction='out', pad=5)
    plt.yticks([10],[u"$d_{min}$"])
    ax.margins(0)
    plt.text(lmin * 0.9,dmin * 1.2,"discernible",ha = "center")
    if version == 3:
        msg = "outer conflict"
    else:
        msg = "indiscernible"
    plt.text(lmin * 1.5,dmin * 0.5,msg,ha = "center",va = "center")
    if version == 3:
        plt.text(lmin * 0.81,dmin * 0.5,"inner\nconflict",ha = "center",va = "center") 
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    plt.tight_layout()
    plt.savefig(image_path)
    print("Finished.")

folder = r"C:\CaGIS Board Dropbox\cantaloupe bob\Barry\Research\Conferences\CEGIS\2024 Discernability Conflicts\figures"
filename = "discernability_regions_3.png"
image_path = f"{folder}\\{filename}"

discernability_regions_figure(image_path,3)
    
# Perkal_figure()
# plt.savefig(image_path)1