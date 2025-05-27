# -*- coding: utf-8 -*-
"""
Created on Fri Sep  8 16:28:23 2023

@author: Administrator
"""

from linesimplify import apsc
from linesimplify import douglas_peucker as dp
import shapefile
import time
import matplotlib.pyplot as plt
from operator import itemgetter
import utils_hausdorff
import utils_geom
import polyline_hausdorff
from utils_data import get_sample_feature,copy2clip
import test_utils

def approx_polyline_distances(A,B):
    """
    Calculates the average and maximum distances between two polylines

    Parameters
    ----------
    A : List of (x,y) tuples
        The first polyline which we are measuring distances from
    B : List of (x,y) tuples
        The second polyline which we are measuring distances to

    Returns
    -------
    (max,avg) : the two distance metrics

    """
    # create index of segments of second polyline
    idx = utils_hausdorff.seg_idx(B)
    # initialize results
    max_dist = 0
    sum_dist = 0
    # debugging
    nearSeg = -1
    fromVertex = -1
    # loop through vertices of first polyline
    for v in range(len(A)):
        seg = utils_hausdorff.nearSegment(A,B,v,idx)
        comp = (True,seg)
        
        loc = utils_hausdorff.nearLoc(A[v],B,comp)
        d = utils_geom.distance(A[v],loc)
        # print(f"v{v} -> s{seg} ({d} {loc})")
        sum_dist += d
        if d > max_dist:
            max_dist = d
            fromVertex = v
            nearSeg = seg
    avgD = sum_dist / len(A)
    return max_dist,avgD,fromVertex,nearSeg


def compare_with_approx(A,B):
    """
    compare time and accuracy of exact and approximate methods
    """
    msg = "method\tspacing\tnA\tnB\tmax_dist\tfromComp\ttoComp\tavgD\telapsed_sec"
    def add_msg_line(msg,method,nA,nB,max_dist,fromComp,toComp,avgD,elapsed_sec):
        val = [method,nA,nB,max_dist,fromComp,toComp,avgD,elapsed_sec]
        msg_line = '\t'.join([f"{x:.4f}" if type(x) == float else str(x) for x in val])
        msg = f"{msg}\n{msg_line}"        
        return msg
    
    
    # run exact method
    print("running exact method...")
    start = time.time() 
    max_dist,avgD,dist_func = polyline_hausdorff.hausdorff_average_distance(A,B,verbose = True)
    
    print("pos   \td     \tcomp")
    for pos,d,comp in dist_func:
        print(f"{pos:.4f}\t{d:.4f}\t{utils_hausdorff.component_label(comp)}")
    
    fromSeg = utils_hausdorff.component_label(max(dist_func,key = itemgetter(1))[2])
    finish = time.time()
    elapsed_sec = finish-start
    msg = add_msg_line(msg,"exact",len(A),len(B),max_dist,f"{fromSeg}","n/a",avgD,elapsed_sec)

    # run approximate method

    start = time.time() 
    max_dist,avgD,fromVertex,nearSeg = approx_polyline_distances(A,B)
    finish = time.time()
    elapsed_sec = finish-start
    msg = add_msg_line(msg,"approx",len(A),len(B),max_dist,fromVertex,nearSeg,avgD,elapsed_sec)
    copy2clip(msg)

    print(msg)    



# FIND BUG IN INDIA BANGLADESH
A,B = test_utils.case(12)
A=A[1:]
compare_with_approx(A,B)

# Figure out why transition goes from s6 to s5
# create simplified feature

dr1 = utils_hausdorff.segDistRep(A,B,0,6)
dr2 = utils_hausdorff.segDistRep(A,B,0,5)
switch_k = utils_hausdorff.segSegSwitchPoint(dr1,dr2)[0]
print(f'switch_k: {switch_k}')
ei2 = utils_hausdorff.segEffectiveInterval(A,B,0,5)
print(f"ei2: {ei2}")
print(f"{switch_k - ei2[1]}")

