# -*- coding: utf-8 -*-
"""
Created on Sat May 25 19:13:18 2024

@author: Barry Kronenfeld
"""
import math
import utils_discernability
import utils_geom
import utils_hausdorff

# FOR DEBUGGING ONLY
import pandas

def discernability_score(poly,conflicts,dmin):
    """
    Scores input polyline features according to discernability, ranging from 
    0% (indiscernible) to 100% (discernible).

    Parameters
    ----------
    poly : list of (x,y)
        The polyline.
    conflicts : list of (x,y)
        List of conflicts, computed from function discernability_conflicts.
    dmin : float
        Minimum discernible distance

    Returns
    -------
    float.

    """
    seg_lens = [utils_geom.distance(poly[v],poly[v+1]) for v in range(len(poly)-1)]
    # score is equal to sum of conflict zone lengths and buffers of dmin 
    # around each conflict zone, but removing overlaps
    # buffers are calculated by computing function of gaps between conflict zones
    # first tally length of conflict zones
    r = sum([utils_discernability.dist_btwn_rel_locs(x[0], x[1], seg_lens) for x in conflicts])
    gap_list = []
    # handle first and last gaps - this will need to be changed 
    # for handling sets of polylines
    gap = utils_discernability.dist_btwn_rel_locs(0, conflicts[0][0], seg_lens)
    if poly[0] == poly[-1]:
        gap += utils_discernability.dist_btwn_rel_locs(conflicts[-1][1], len(poly), seg_lens)
        gap_list.append(gap)
    else:
        gap_list.append(gap)
        gap = utils_discernability.dist_btwn_rel_locs(conflicts[-1][1], len(poly), seg_lens)        
        gap_list.append(gap)
    for idx in range(len(conflicts)-1):
        gap_list.append(utils_discernability.dist_btwn_rel_locs(
            conflicts[idx][1], conflicts[idx+1][0], seg_lens))
    # sum up gap contributions
    r += sum([min(x,dmin) for x in gap_list])
    r = r / sum(seg_lens)
    return 1-r

def discernability_conflicts(poly, dmin, lmin, verbose = False):
    """
    Identifies sections of the polyline that are within a minimum gap 
    distance from other sections of the same polyline located at least 
    a minimum path length away.

    Parameters
    ----------
    poly : list of (x,y) tuples
        the input polyline.
    dmin : float
        minimum distance, below which a conflict is detected.
    lmin : float
        minimum path length, above which a conflict is detected.

    Returns
    -------
    List of (float,float) sections. Each section is a pair of numerical values
            specifying start and end of each section. Integer
            portion of each float represents the segment id, while decimal portion
            represents position along segment.

    """
    report_interval = 100000
    minr = dmin / lmin
    # initialize result, work lists
    if verbose:
        print("initializing result list and work lists...")
    r = []
    sw,vw = conflict_work_lists(poly,dmin)
    seg_lens = [utils_geom.distance(poly[v],poly[v+1]) for v in range(len(poly)-1)]
    
    # process work lists
    if verbose:
        print(f"found {len(sw)} segment conflict candidates.")
        print("processing work lists to identify conflicts...")
        df=pandas.DataFrame(sw)
        df.to_clipboard(index=False,header=False)
    n = 0
    for fromSeg,toSeg in sw:
        n += 1
        if n % report_interval == 0:
            print(f"Processed {n} of {len(sw)} items in segment work list...")
        conflicts = utils_discernability.seg_conflict_region(
            poly,fromSeg,toSeg,dmin,lmin,minr,seg_lens)
        r += conflicts
    n = 0
    for seg,v in vw:
        n += 1
        if n % report_interval == 0:
            print(f"Processed {n} of {len(vw)} items in vertex work list...")
        conflicts = utils_discernability.vrt_conflict_region(
            poly, seg, v, dmin, lmin, minr, seg_lens)
        r += conflicts
    # code to process vertices to be added later
    # merge sections
    r = merge_sections(r)      
    if verbose:
        # print("AFTER MERGING SECTIONS:")
        # [print(sec) for sec in r]
        print(f"{len(r)} conflicts found.")
        
    return r

def conflict_work_lists(poly,dmin):
    sw = set() # work list of (seg->seg) pairs
    vw = set() # work list of (vertex->seg) pairs
    
    # create spatial index and calculate segment lengths
    poly_idx = utils_hausdorff.seg_idx(poly)

    # loop through polyline vertices
    for v in range(len(poly)):
        # identify all candidate segments within minimum distance
        x,y = poly[v][0],poly[v][1]
        square = (x - dmin,y - dmin,x + dmin,y + dmin)
        cands = list(poly_idx.intersection(square))
        # add to work lists
        for cand in cands:
            if v > 0:
                sw.add((cand,v - 1))
                sw.add((v - 1,cand))
            if v < len(poly) - 1:
                sw.add((cand,v))
                sw.add((v,cand))
                vw.add((cand,v))
            if v > 0 and v < len(poly) - 1:
                sw.add((v,v - 1))
                sw.add((v - 1,v))
    return sw,vw

def polyline_sections_to_features(poly,secs):
    """
    Creates polyline features from numerical values specifying 
    sections of the input polyline

    Parameters
    ----------
    poly : list of (x,y) tuples
        the input polyline (must be single part).
    secs : list of (float,float) tuples
        Numerical values specify start and end of each section. Integer
        portion of each float represents is segment id, while decimal portion
        represents position along segment.

    Returns
    -------
    List of list of (x,y) tuples representing polyline sections, in standard 
    format (i.e. ready to feed into utils_data.create_polyline_shapefile).

    """
    r = []
    for sec in secs:
        feat = []
        # get coordinates of section start
        v1 = int(sec[0])
        k1 = sec[0] - v1
        feat.append(utils_geom.location(poly,v1,k1))
        # get any intermediate vertices
        for v in range(math.ceil(sec[0]),math.floor(sec[1]+1)):
            feat.append(poly[v])
        # get coordinates of section end
        v2 = int(sec[1])
        if sec[1] > v2:
            k2 = sec[1] - v2
            feat.append(utils_geom.location(poly,v2,k2))
        # because standard polyline could be multipart, wrap in another list
        r.append([feat])
    return r        

def merge_sections(secs):
    """
    Merges each set of sections that overlap into a single section

    Parameters
    ----------
    secs : iterable of (float,float) tuples
        Numerical values specify start and end of each section. Integer
        portion of each float represents is segment id, while decimal portion
        represents position along segment.

    Returns
    -------
    list of (float,float) tuples.

    """
    if len(secs) == 0:
        return []
    # sort by first value
    secs = sorted(secs,key = lambda x: x[0])    
    
    # initialize
    r = []
    cur_sec = secs[0]
    # look through all remaining sections
    for sec in secs[1:]:
        # Compare start of this section with end of current section
        if sec[0] <= cur_sec[1]: # merge
            if sec[1] > cur_sec[1]:
                cur_sec = (cur_sec[0],sec[1])
        else: # turn in last section and create a new one
            r.append(cur_sec)
            cur_sec = sec
    # turn in final section
    r.append(cur_sec)
    return r
    
    
    
    
    
    
    
    
    
    
