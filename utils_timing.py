# -*- coding: utf-8 -*-
"""
Create series of time measurements to assess algorithm efficiency.
While we are at it, looks for possible errors where there is a
significant difference between exact and approximate methods.
"""

from linesimplify import apsc
from linesimplify import douglas_peucker as dp
import time
import matplotlib.pyplot as plt
from operator import itemgetter
import utils_hausdorff
import utils_geom
import polyline_hausdorff
from utils_data import get_sample_feature

def time_test_equal_vertex_counts(feat_a_func,feat_b_func,vertex_counts,brute_force = False):
    msg = f"n\tm\telapsed\tavg_dist"
    print(msg)
    data = msg
    for n in vertex_counts:    
        # Create two versions of a simplified line
        feat_a = feat_a_func(n)
        feat_b = feat_b_func(n)
        # calculate average polyline distance
        start = time.time() 
        avgD = polyline_hausdorff.hausdorff_average_distance(feat_a,feat_b,brute_force)[1]
        finish = time.time()
        elapsed = finish-start
        msg = f"{n},{n},{elapsed},{avgD}"
        data = data + "\n" + msg
        print(msg)
    return data
    
def time_test_unequal_vertex_counts(
        feat_a_func,
        feat_b_func,
        a_counts,
        b_counts,
        brute_force = False,
        its = 5):
    msg = f"n,m,elapsed,avg_dist"    
    print(msg)
    data = msg
    for i in range(len(a_counts)):
        elapsed = 0
        for it in range(its):
            n = a_counts[i]
            m = b_counts[i]
            # Create two versions of a simplified line
            feat_a = feat_a_func(n)
            feat_b = feat_b_func(m)
            # calculate average polyline distance
            start = time.time() 
            avgD = polyline_hausdorff.hausdorff_average_distance(feat_a,feat_b,brute_force)[1]
            finish = time.time()
            elapsed += finish-start
        elapsed = elapsed / its
        msg = f"{n},{m},{elapsed:.6f},{avgD:.6f}"
        data += "\n" + msg
    return data

def zigzag(n,vertical=False):
    pts = [(i/(n-1),i%2) for i in range(n)]
    if vertical:
        pts = [(y,x) for x,y in pts]
    return pts

def test_same_polyline(feat):
    """
    See if it's really giving a nonzero distance for the same polylines compared with each other'
    """
    simp_table=apsc.simplificationTable(feat) # create the simplification table 
    vertex_counts = [1000,100]
    def get_first_feature(n):
        return apsc.simplifiedLine(simp_table,min_pts=n) 
    time_test_equal_vertex_counts(get_first_feature,get_first_feature,vertex_counts)

def time_test_equal(feat,vertex_counts):
    """ Tests how long it takes to compute average distance between 
        two polylines with equal numbers of vertices """
    # precalculate
    simp_table=apsc.simplificationTable(feat) # create the simplification table 
    errors, sorted_errors = dp.get_errors_sortedErrors(feat) # get displacement distance for each point
    def get_first_feature(n):
        return apsc.simplifiedLine(simp_table,min_pts=n) 
    def get_second_feature(n):
        return dp.simplify_by_numPts(feat, n, errors, sorted_errors) # simplify to 10 pts,[]
    time_test_equal_vertex_counts(get_first_feature,get_second_feature,vertex_counts)

def time_test_unequal(feat,a_counts,b_counts,brute_force = False):
    """ Tests how long it takes to compute average distance between 
        two polylines with unequal numbers of vertices """
    # precalculate
    simp_table=apsc.simplificationTable(feat) # create the simplification table 
    errors, sorted_errors = dp.get_errors_sortedErrors(feat) # get displacement distance for each point
    def get_first_feature(n):
        return apsc.simplifiedLine(simp_table,min_pts=n) 
    def get_second_feature(n):
        return dp.simplify_by_numPts(feat, n, errors, sorted_errors) # simplify to 10 pts,[]
    return time_test_unequal_vertex_counts(
        get_first_feature,
        get_second_feature,
        a_counts,
        b_counts,
        brute_force = brute_force)


def time_test_zigzag(vertex_counts):
    def zigzag_vertical(n):
        return zigzag(n,False)
    def zigzag_horizontal(n):
        return zigzag(n,True)
    time_test_equal_vertex_counts(zigzag_vertical,zigzag_horizontal,vertex_counts)

def compare_with_approx(feat,spacings,vertex_ratio = 0.1,reverse = False):
    """
    compare time and accuracy of exact and approximate methods
    """
    msg = "method,d_avg,max_dist,spacing,nA,nB,fromComp,toComp,elapsed_sec"
    def add_msg_line(msg,method,d_avg,max_dist,spacing,nA,nB,fromComp,toComp,elapsed_sec):
        val = [method,d_avg,max_dist,spacing,nA,nB,fromComp,toComp,elapsed_sec]
        msg_line = ','.join([f"{x:.6f}" if type(x) == float else str(x) for x in val])
        print(f"{msg_line}")
        msg = f"{msg}\n{msg_line}"        
        return msg
    # create simplified feature
    A = feat
    simp_table=apsc.simplificationTable(A,report_interval = 20000) # create the simplification table 
    errors, sorted_errors = dp.get_errors_sortedErrors(A) # get displacement distance for each point
    n = int(len(A) * vertex_ratio)
    B = apsc.simplifiedLine(simp_table,min_pts=n) 

    if reverse:
        A,B = B,A

    # run exact method
    print("running exact method...")
    start = time.time() 
    max_dist,d_avg,dist_func = polyline_hausdorff.hausdorff_average_distance(A,B,verbose = False)
    fromSeg = utils_hausdorff.component_label(max(dist_func,key = itemgetter(1))[2])
    finish = time.time()
    elapsed_sec = finish-start
    msg = add_msg_line(msg,"exact",d_avg,max_dist,"n/a",len(A),len(B),f"{fromSeg}","n/a",elapsed_sec)

    # run approximate method
    for spacing in spacings:
        print(f"running approx method (spacing={spacing})")
        start = time.time() 
        dense_poly = utils_geom.densify(A, spacing)
        max_dist,d_avg,fromVertex,nearSeg = approx_polyline_distances(dense_poly,B)
        finish = time.time()
        elapsed_sec = finish-start
        msg = add_msg_line(msg,"approx",d_avg,max_dist,spacing,len(dense_poly),len(B),"v"+str(fromVertex),"s"+str(nearSeg),elapsed_sec)
    return msg

def create_example_plots(orig_feat):
    """
    create sample plots for paper demonstrating scenarios with
    differences in computational complexity
    """
    c1 = "blue"
    c2 = "darkorange"
    fig, axes = plt.subplots(1,3,figsize=(7,2))
    plt.axis('equal')
    for ax in axes:
        ax.axis("off")
        plt.axis('equal')
    # show two polylines with equal number of vertices
    n = 25
    simp_table=apsc.simplificationTable(orig_feat) # create the simplification table 
    errors, sorted_errors = dp.get_errors_sortedErrors(orig_feat) # get displacement distance for each point
    feat_a = apsc.simplifiedLine(simp_table,min_pts=n) 
    feat_b = dp.simplify_by_numPts(orig_feat, n, errors, sorted_errors)
    ax = axes[0]
    x,y = zip(*feat_a)
    ax.plot(x,y,color=c1,linewidth=0.5)
    x,y = zip(*feat_b)
    ax.plot(x,y,color=c2,linewidth=0.5)
    ax.set_title('best case:\n equal # vertices', y = -0.3)
    # show one polyline with 10x vertices as the other
    n = 10
    feat_a = apsc.simplifiedLine(simp_table,min_pts=n*10) 
    feat_b = dp.simplify_by_numPts(orig_feat, n, errors, sorted_errors)
    ax = axes[1]
    x,y = zip(*feat_a)
    ax.plot(x,y,color=c1,linewidth=0.5)
    x,y = zip(*feat_b)
    ax.plot(x,y,color=c2,linewidth=0.5)
    ax.set_title('typical case:\n unequal # vertices', y = -0.3)
    # show worst case scenario - 2 zigzags in opposite directions    
    ax = axes[2]
    feat_a = zigzag(21)
    feat_b = zigzag(21,True)
    x,y = zip(*feat_b)
    ax.plot(x,y,color=c1,linewidth=0.5)
    x,y = zip(*feat_a)
    ax.plot(x,y,color=c2,linewidth=0.5)
    ax.set_title('worst case:\n orthogonal zigzags',y = -0.3)
    # display and save    
    
    
    folder = r"C:\CaGIS Board Dropbox\cantaloupe bob\Research\Projects\line difference metrics\Hausdorff\images"
    filename = "features_for_time_testing.png"
    plt.savefig(f"{folder}\\{filename}",dpi=300)
    plt.show()

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

def accuracy_check():
    # check exact method against approximate method with fine spacing
    # to check for possible errors
    # note that in previous rounds errors were in the range of 100+m
    feat = get_sample_feature("india_bangladesh")
    # create simplified feature
    vertex_ratio = 0.1
    simp_table=apsc.simplificationTable(feat) # create the simplification table 
    errors, sorted_errors = dp.get_errors_sortedErrors(feat) # get displacement distance for each point
    n = int(len(feat) * vertex_ratio)
    B = apsc.simplifiedLine(simp_table,min_pts=n) 

    # loop through segments
    spacing = 2
    tol = 0.1
    report_interval = 1000
    print("POSSIBLE ERRORS:")
    error_count = 0
    messages = []
    for seg in range(len(feat)-1):
        A = feat[seg:seg + 2]
        dense_poly = utils_geom.densify(A,spacing)
        # try to get region of about 1000 vertices around A
        pos = int(n*seg/len(feat))
        B2 = B[max(0,pos - 500):min(len(B)-1,pos + 500)]
        exact_max,exact_avgD,fromSeg = polyline_hausdorff.Hausdorff_average_distance(A,B2)
        approx_max,avgD,fromVertex,nearSeg = approx_polyline_distances(dense_poly,B2)
        # exact max should not be > sum of approx_max,spacing        
        if exact_max > approx_max + spacing + tol or exact_max < approx_max - spacing - tol:
            messages.append(f"seg\t{seg}\tmax\t{exact_max}\tapprox_max\t{approx_max}")
            error_count += 1
            print(f"{error_count} possible errors found...")
        if seg % report_interval == 0:
            print(f"{seg} segments processed")
    print("\n".join(messages))
    print(f"{error_count} possible errors found")
        
