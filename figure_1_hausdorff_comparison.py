# -*- coding: utf-8 -*-
"""
Reproduces Figure 2, with additional information on results of scipy and shapely Hausdorff functions shown in interpreter.
"""

##################################################
# PARAMETERS 
# path of file to save resulting image to
output_file = r"results\figure_2_hausdorff_variations.png"
##################################################

# Import main module and utilities
import polyline_hausdorff as ph
import utils_geom
import utils_hausdorff

# Create two polylines
A = [(26, 8), (13, -2), (13, 19), (10, 19), (10, 23), (1, 17)]
B = [(15, 1), (28, 11), (13, 26), (1, 18)]

# Compute the hausdorff distance. This will return a tuple of three items.
h_dist, avg_d, transitions = ph.hausdorff_average_distance(A,B)

# The hausdorff distance is the first item in the tuple
print("The true Polyline Hausdorff distance is {:.3f}.".format(h_dist))

# Identify locations involved in Hausdorff distance
# transitions contains tuples of (position, distance, component)
h_transition = max(transitions,key = lambda x: x[1])
id = transitions.index(h_transition)
seg = int(h_transition[0])
k = h_transition[0] - seg
h_origin = utils_geom.location(A,seg,k)

print(f'Hausdorff origin: {h_origin}')
h_destination = []

for id in [id,id-1]:
    if id >= 0:
        h_destination.append(utils_hausdorff.nearLoc(h_origin,B,transitions[id][2]))
print(f'Hausdorff destination: {h_destination}')





"""
***********************************************
                 PLOT RESULTS
***********************************************
"""

import matplotlib.pyplot as plt
import math


# set up plot
plt.figure(figsize=(4.5,4.5),dpi=128)
# plot the original polylines
x,y = zip(*A)
plt.plot(x,y,linewidth=2,c='darkorange',marker='o',markersize=8,mfc='white',mec='gray')
x,y = zip(*B)
plt.plot(x,y,linewidth=2,c='blue',marker='o',markersize=8,mfc='white',mec='gray')
plt.axis('equal')
#plt.axis('off')

# label polylines
# calculate rotation parameters for text
plt.text(A[-1][0] + 2,A[-1][1],"A",ha='center',va='center',fontsize=12)
plt.text(B[-1][0] + 2,B[-1][1] + 2.5,"B",ha='center',va='center',fontsize=12)

# plot the polyline Hausdorff source location
plt.plot(h_origin[0],h_origin[1],marker='_',mec='red',mfc='red',markersize=9)

# plotting A[-1][0] + 2and arrows is complicated - let's make a function for it
def showDist(src_loc,trg_loc,lbl,augment=0, showdistances=False):
    # draw arrow from source to target
    plt.arrow(src_loc[0],src_loc[1],(trg_loc[0]-src_loc[0]),(trg_loc[1]-src_loc[1]),color='black',head_width=0.55,head_length=0.75,overhang=0.15,length_includes_head = True)
    # calculate rotation parameters for text
    r = math.degrees(math.atan2(trg_loc[1]-src_loc[1],trg_loc[0]-src_loc[0]))% 360
    if 100 < r < 260:
        r -= 180
    # calculate text placement
    
    offset = 0.5 if showdistances else -0.95
    
    textx,texty = -1*offset*math.sin(math.radians(r)) + (src_loc[0]+trg_loc[0])/2, offset*math.cos(math.radians(r)) + (src_loc[1]+trg_loc[1])/2    
    # plot text
    plt.text(textx,texty,lbl,ha='center',va='center',fontsize=11+augment,rotation=r)
    if showdistances:
        # calculate distance
        dx2 = (trg_loc[0] - src_loc[0])**2 
        dy2 = (trg_loc[1] - src_loc[1])**2 
        d = math.sqrt(dx2+dy2)
        # show on plot
        offset=-0.6
        textx,texty = -1*offset*math.sin(math.radians(r)) + (src_loc[0]+trg_loc[0])/2, offset*math.cos(math.radians(r)) + (src_loc[1]+trg_loc[1])/2    
        plt.text(textx,texty,"{:.2f}".format(d),ha='center',va='center',fontsize=10+augment,rotation=r)    

# plot the target locations, with text and arrows
for loc in h_destination:
    showDist(h_origin,loc,"H$_{A\\rightarrow B}$",1)

"""
***********************************************
COMPARE WITH SCIPY
***********************************************
"""
try:
    from scipy.spatial.distance import directed_hausdorff
    import numpy as np
    # create numpy arrays
    u = np.array(A)
    v = np.array(B)
    # calculate hausdorff distance and get participating vertices
    d1,a1,b1 = directed_hausdorff(u,v)
    d2,b2,a2 = directed_hausdorff(v,u)
    if d1 > d2:
        d = d1
        src_loc = A[a1]
        trg_loc = B[b1]
    else:
        d = d2
        src_loc = B[b2]
        trg_loc = A[a2]
    # print results
    print(f"SciPy Hausdorff distance is {d:.2f}.")
    print(f'src_loc: {src_loc}')
    print(f'trg_loc: {trg_loc}')
    # show graphically
    showDist(src_loc,trg_loc,"H$_{v_{A}\\rightarrow v_{B}}$")
except ImportError:
    print("Install scipy & numpy to see a comparison with SciPy's Directed Hausdorff distance.")


"""
***********************************************
COMPARE WITH SHAPELY
***********************************************
"""
import utils_hausdorff as uh
# shapely appears to calculate the largest distance from a
# vertex on the first polyline to the nearest point
# on the second polyline
try:   
    from shapely.geometry import LineString
    # create linestring objects
    lineA = LineString(A)
    lineB = LineString(B)
    # calculate hausdorff distance
    shapely_hausdorff = lineA.hausdorff_distance(lineB)
    # print results
    print("Shapely Hausdorff distance is {:.2f}.".format(shapely_hausdorff))
    # show graphically
    src_loc = A[2] 
    trg_loc = utils_hausdorff.nearLoc(src_loc, B, (True,1)) 
    showDist(src_loc,trg_loc,"H$_{v_{A}\\rightarrow B}$")
except ImportError:
    print("Install shapely to see a comparison with shapely's Hausdorff distance.")

# Add coordinates into title for reproducibility
# plt.title(f"A: {str(A)[1:-1]}\nB: {str(B)[1:-1]}",
#         size = 10, y = -0.1, va = "top")

# This is conceptual so we don't need axis lines
ax = plt.gca()
ax.set_axis_off()


plt.savefig(output_file,dpi=300)
    
plt.show()
print("finished.")