# -*- coding: utf-8 -*-
"""
Created on Wed Jun 12 10:56:55 2024

@author: Barry Kronenfeld
"""

import math
import utils_geom
import utils_hausdorff

def dist_btwn_rel_locs(loc1,loc2,seg_lens):
    """
    Calculates distance between two locations expressed as seg.k 

    Parameters
    ----------
    loc1 : float
        First relative position. Integer portion is segment #, decimal portion 
        is relative distance along a segment.
    loc2 : float
        Second relative position.
    seg_lens : list of floats
        Lengths of segments in polyline.

    Returns
    -------
    None.

    """
    if loc1 > loc2:
        loc1,loc2 = loc2,loc1
    s1 = math.ceil(loc1)
    s2 = math.floor(loc2)
    if s1 > s2:
        r = (loc2 - loc1) * seg_lens[s1]
    else:
        r = sum(seg_lens[s1 + 1:s2]) # in between segments
        r += (s1 - loc1) * seg_lens[s1-1] # first partial (or full) segment
        if loc2 > s2: # test this to allow loc = len(poly)
            r += (loc2 - s2) * seg_lens[s2]
    return r

def segDistTrans(dmin,ks,L,sin_theta):
    """
    Calculates the k-value(s) on a segment (a) at which the distance to    
    the nearest point on another segment (b) is equal to a minimum gap
    threshold

    Parameters
    ----------
    dmin : float
        minimum gap threshold.
    ks : float
        k-value on (a) of intersection of lines through (a) & (b).
    L : float
        length of (a).
    sin_theta : float
        sine of angle between (a) & (b).

    Returns
    -------
    list of floats
        k-values of transition points
    """
    # make sure that sin_theta is positive
    sin_theta = abs(sin_theta)
    if ks == None: # Segment Is Parallel; sin_theta is actually relative distance (q-value)
        return [sin_theta * L]
    elif sin_theta == 0:
        # this should never happen!
        raise Exception("Error in utils_discernability.segDistTrans(): \n" +
                        "Segment distance representation error: sin_theta == 0 but ks != None \n" +
                        "If sin_theta == 0 that means segment is parallel!")
    elif L == 0: 
        return []
    else:
        # two possible solutions on either side of intersection
        signed_term = dmin / (L * sin_theta)
        return [ks + signed_term, ks - signed_term]

def segDistPathLen(k,l_ab,beta1,beta2,L,cos_theta,kb0):
    """
    Computes length along polyline between relative position on one segment 
    and point across gap on the other segment

    Parameters
    ----------
    k : float
        relative position along a.
    l_ab : float
        path length between first vertices of (a) & (b).
    beta1 : int
        +1 if (b) < (a), -1 otherwise.
    beta2 : int
        +1 if (b > a) == (kb1 >= kb0), -1 otherwise.
    L : float
        length of (a).
    cos_theta : float
        cosine of angle between (a) & (b).
    kb0 : float
        k-value on (a) for which nearest point is at start of (b).

    Returns
    -------
    float.
    
    """
    return l_ab + beta1 * L * k + beta2 * L * abs(cos_theta) * (k - kb0)

def segDistPathLenTrans(lmin,l_ab,beta1,beta2,L,cos_theta,kb0):
    """
    Calculates the k-value on a segment (a) at which the path length to 
    the nearest point on another segment (b) equals a minimum path length 
    threshold.

    Parameters
    ----------
    lmin : float
        the minimum path length threshold.
    l_ab : float
        path length between first vertices of (a) & (b).
    beta1 : int
        +1 if (b) < (a), -1 otherwise.
    beta2 : int
        +1 if (b > a) == (kb1 >= kb0), -1 otherwise.
    L : float
        length of (a).
    cos_theta : float
        cosine of angle between (a) & (b).
    kb0 : float
        k-value on (a) for which nearest point is at start of (b).

    Returns
    -------
    list of floats
        k-value of path length transition, or empty list if none exists.

    """

    denominator = beta1 * L + beta2 * L * cos_theta
    if denominator != 0: 
        # denominator is zero when cosine theta is one and parameters are
        # -1 & +1
        # in this case the length does not change and so there is no transition
        numerator = lmin - l_ab + beta2 * L * cos_theta * kb0
        return [numerator / denominator]
    else:
        return []

def segDistRatioTrans(minr,kb0,l_ab,beta1,beta2,L,ks,sin_theta,cos_theta,tol = 0.000001):
    """
    Computes k-value on a segment (a) at which ratio of (gap/path length) 
    to a second segment (b) is equal to designated minimum (minr)

    Parameters
    ----------
    minr : float
        Minimum discernible ratio of gap over path length.
    kb0 : float
        intersection of perpendicular line through first vertex of (b) with (a).
    l_ab : float
        path length between start vertices of (a) & (b).
    beta1 : int
        sequence parameter, -1 if b > a | +1 if b < a.
    beta2 : int
        direction parameter, +1 if (b > a) == (kb1 >= kb0), -1 otherwise.
    L : float
        length of segment (a).
    ks : float
        k-value on (a) of intersection with line through (b).
    sin_theta : float
        sine of angle between (a) & (b), +/- if gap increases/decreases with k.
    cos_theta : float
        cosine of angle between (a) & (b).

    Returns
    -------
    list
        list of k-value of transition points.

    """    
    if ks == None:
        # Segment is parallel so gap is fixed; look for path length transition
        gap = sin_theta
        lmin = gap / minr
        return segDistPathLenTrans(lmin,l_ab,beta1,beta2,L,cos_theta,kb0)
    else:
        r = []
        sin_theta = abs(sin_theta)
        cos_theta = abs(cos_theta)
        numerator1 = minr * (beta2 * cos_theta * L * kb0 - l_ab + tol)
        numerator2 = ks * L * sin_theta
        denominator1 = L * minr * (beta1 + beta2 * cos_theta)
        denominator2 = L * sin_theta
        # situations in which denominator could be zero
        # - (b) parallel to (a) : should be caught by ks == None
        # - segment length is zero : no transitions
        # - dg/dl = minr : no transitions 
        if denominator1 + denominator2 != 0:
            k1 = (numerator1 + numerator2) / (denominator1 + denominator2)
            if k1 < ks:
                r.append(k1)
        if denominator1 - denominator2 != 0:
            k2 = (numerator1 - numerator2) / (denominator1 - denominator2)
            if k2 > ks:
                r.append(k2)
        return r

def vrt_conflict_region(poly,a,b,dmin,lmin,minr,seg_lens,verbose = False):
    
    # Get effective interval and make sure it is valid
    ei = utils_hausdorff.vertEffectiveInterval(poly, poly, a, b, 0.0000000000001)
    ei = utils_hausdorff.withinUnitInterval(ei[0], ei[1])
    if verbose:
        print(f'ei: {ei}')
    if ei[0] == float("-inf"):
        return []
    else:
        # calculate parameters
        if b > a:
            beta = -1
            l_ab = sum(seg_lens[a:b])
        else:
            beta = 1
            l_ab = sum(seg_lens[b:a])
        L = seg_lens[a]
        dr = utils_hausdorff.vertDistRep(poly,poly,a,b)
        kv,q = dr[1],dr[2]

        if verbose:
            print("*** Thresholds ***")
            print(f'dmin: {dmin}')
            print(f'lmin: {lmin}')
            print(f'minr: {minr}')
            print("*** Parameters ***")
            print(f'beta: {beta}')
            print(f'L: {L}')
            print(f'l_ab: {l_ab}')
            print(f'dr: {dr}')
            print(f'kv: {kv}')
            print(f'q: {q}')

        # find potential boundaries of conflict regions
        zone_bounds = [ei[0],ei[1]]
        dt = []
        plt = []
        rt = []
        if dmin > 0:
            dt = vrtDistTrans(dmin,kv,q,L)
            zone_bounds += dt
        if lmin > 0:
            plt = vrtDistPathLenTrans(lmin,l_ab,beta,L)
            zone_bounds += plt
        if minr > 0:
            rt = vrtDistRatioTrans(minr,kv,q,L,l_ab,beta)
            zone_bounds += rt
        zone_bounds = sorted([b for b in zone_bounds if ei[0] <= b <= ei[1]])
        if verbose:
            print("*** Potential Transitions ***")
            print(f'dt: {dt}')
            print(f'plt: {plt}')
            print(f'rt: {rt}')

        # check each region's midpoint to see if it is a conflict or not
        r = []
        if verbose:
            print("*** Section Checks ***")
        for i in range(len(zone_bounds)-1):
            k = (zone_bounds[i]+zone_bounds[i+1])/2
            d = utils_hausdorff.vertDistance(dr,k,L)
            if verbose:
                print(f'k: {k}')
                print(f'd: {d}')
            if d <= dmin:
                l_path = vrtDistPathLen(k,l_ab,beta,L)
                if verbose:
                    print(f"dmin threshold met!")
                    print(f'l_path: {l_path}')
                    print(f"ratio: {d / l_path}")
                if l_path > lmin:
                    # outer conflict
                    r.append((a + zone_bounds[i],a + zone_bounds[i+1]))
                    if verbose:
                        print("lmin threshold met!")
                        print(f"d/l_path: {d/l_path}")
                elif d / l_path <= minr:
                    # inner conflict
                    if b > a:
                        r.append((a + zone_bounds[i],b))
                    else:
                        r.append((b,a + zone_bounds[i + 1]))
                    # r.append((a + zone_bounds[i],a + zone_bounds[i+1]))
                    if verbose:
                        print("minr threshold met")
                        print(f"adding section {(a + zone_bounds[i],a + zone_bounds[i+1])} to results")
        return r
        
def seg_conflict_region(poly,a,b,dmin,lmin,minr,seg_lens,verbose = False):
    # Get effective interval and make sure it is valid
    tol = 0.000001
    ei = utils_hausdorff.segEffectiveInterval(poly, poly, a, b, tol)
    ei = utils_hausdorff.withinUnitInterval(ei[0], ei[1])
    if verbose:
        print(f'ei: {ei}')
    if ei[0] == float("-inf"):
        return []
    else:
        # calculate parameters
        dr = utils_hausdorff.segDistRep(poly, poly, a, b)
        ks = dr[1]
        if ks == None:
            # segments are parallel
            q = dr[2]
            sin_theta = 0
            cos_theta = 1
        else:
            # segments are not parallel
            sin_theta = abs(dr[2])
            cos_theta = math.sqrt(1-sin_theta ** 2)
        L = seg_lens[a]
        if b > a:
            l_ab = sum(seg_lens[a:b])
        else:
            l_ab = sum(seg_lens[b:a])
        if b > a:
            beta1 = -1
        else:
            beta1 = 1
        # determine parameters based on direction of b wrt a
        p = utils_geom.project_pt_to_line(poly[b], poly[a], poly[a+1])
        kb0 = utils_geom.kvalue(p, poly[a], poly[a+1])
        p = utils_geom.project_pt_to_line(poly[b+1], poly[a], poly[a+1])
        kb1 = utils_geom.kvalue(p, poly[a], poly[a+1])
        
        if (b > a) == (kb1 >= kb0):
            beta2 = 1
        else:
            beta2 = -1
        kb0 = utils_geom.project_out(poly[a],poly[a+1],poly[b],poly[b+1])
        # find potential boundaries of conflict regions
        dt = []
        plt = []
        rt = []
        zone_bounds = [ei[0],ei[1]]       
        if dmin > 0:
            if ks != None: # can't have a distance transition if segments are parallel
                dt = segDistTrans(dmin,ks,L,sin_theta)
                zone_bounds += dt
        if lmin > 0:
            plt = segDistPathLenTrans(lmin,l_ab,beta1,beta2,L,cos_theta,kb0)
            zone_bounds += plt
        if minr > 0:
            rt = segDistRatioTrans(
                minr,kb0,l_ab,beta1,beta2,L,ks,sin_theta,cos_theta,tol)
            zone_bounds += rt

        zone_bounds = [b for b in zone_bounds if ei[0] <= b <= ei[1]]
        zone_bounds.sort()
        
        if verbose:
            print("PARAMETERS")
            print(f'ks: {ks}')
            print(f'L: {L}')
            print(f'sin_theta: {sin_theta}')
            print(f'cos_theta: {cos_theta}')
            print(f'l_ab: {l_ab}')
            print(f'beta1: {beta1}')
            print(f'beta2: {beta2}')
            print(f'kb0: {kb0}')
            print("TRANSITIONS")
            print(f'dt: {dt}')
            print(f'plt: {plt}')
            print(f'rt: {rt}')
        
        # check each region's midpoint to see if it is a conflict or not
        r = []
        for i in range(len(zone_bounds)-1):
            k = (zone_bounds[i]+zone_bounds[i+1])/2
            d = utils_hausdorff.segDistance(dr,k,L)
            if d <= dmin:
                l_path = segDistPathLen(k,l_ab,beta1,beta2,L,cos_theta,kb0) - tol
                if l_path > lmin:
                    # outer conflict
                    r.append((a + zone_bounds[i],a + zone_bounds[i+1]))
                elif l_path > tol:
                    ratio = d/l_path
                    if ratio < minr:
                        # inner conflict
                        # project out from each b vertex to segment a 
                        kb0 = utils_geom.project_out(poly[a],poly[a + 1],poly[b],poly[b + 1])
                        kb1 = utils_geom.project_out(poly[a],poly[a + 1],poly[b + 1],poly[b])
                        if b > a:
                            kb = (zone_bounds[i] - kb0) / (kb1 - kb0)
                            r.append((a + zone_bounds[i],b + kb))
                        else:
                            kb = (zone_bounds[i + 1] - kb0) / (kb1 - kb0)
                            r.append((b + kb,a + zone_bounds[i + 1]))
                        # r.append((a + zone_bounds[i],a + zone_bounds[i+1]))
                        if verbose:
                            print(f"conflict_zone: {(a + zone_bounds[i],a + zone_bounds[i+1])}")
                            print(f'k: {k}')
                            print(f'd: {d}')
                            print(f'l_path: {l_path}')
        return r
    
def vrtDistTrans(dmin,kv,q,L):
    """
    Calculates the k-value(s) on a segment (a) at which the distance to    
    vertex (b) is equal to a minimum gap threshold

    Parameters
    ----------
    dmin : float
        minimum gap threshold.
    kv : float
        k-value (relative position on (a)) of projection of (b) onto (a).
    q : float
        relative distance of (b) from (a).
    L : float
        length ef (a).

    Returns
    -------
    r : list of floats
        k-values of transition points.

    """
    r = []
    root = (dmin ** 2) - (L ** 2) * (q ** 2)
    if root >= 0:
        signed_term = math.sqrt(root) / L
        s1 = kv + signed_term
        s2 = kv - signed_term
        if 0 < s1 < 1:
            r.append(s1)
        if 0 < s2 < 1:
            r.append(s2)
    return r

def vrtDistPathLen(k,l_ab,beta,L):
    """
    Computes length along polyline between relative position on a segment (a)
    and a vertex (b)

    Parameters
    ----------
    k : float
        relative position along (a).
    l_ab : float
        path length between first vertex of (a) & (b).
    beta : int
        +1 if (b) < (a), -1 otherwise.
    L : float
        length of (a).

    Returns
    -------
    float.
    
    """        
    return l_ab + beta * L * k
    
def vrtDistPathLenTrans(lmin,l_ab,beta,L):
    """
    Calculates the k-value on a segment (a) at which the path length to 
    vertex (b) equals a minimum path length threshold.

    Parameters
    ----------
    lmin : float
        the minimum path length threshold.
    l_ab : float
        distance between start vertex of (a) and (b).
    beta : float
        sequence parameter, -1 if b > a | +1 if b < a.
    L : float
        length of segment (a).

    Returns
    -------
    list of float
        k-value of transition point on (a).

    """    
    return [(lmin - l_ab) / (beta * L)]
    
def vrtDistRatioTrans(minr,kv,q,L,l_ab,beta):
    """
    Computes the k-value(s) on a segment (a) at which the ratio of gap to 
    path length to a vertex (b) equals a designated minimum ratio.

    Parameters
    ----------
    minr : float
        minimum ratio of gap to path length.
    kv : float
        k-value of projection of (b) onto (a).
    q : float
        relative distance from (b) to line through (a).
    L : float
        length of segment (a).
    l_ab : float
        path length from first vertex of (a) to (b).
    beta : float
        direction parameter, +1 if (b > a) == (kb1 >= kb0), -1 otherwise..

    Returns
    -------
    list of floats
        k-values of transition points

    """    
    r = []
    bracketed_term = (l_ab ** 2) + (2 * l_ab * beta * L * kv) + (
        (beta ** 2) * (L ** 2) * ((q ** 2) + (kv ** 2))                                                                   )
    root = bracketed_term * (minr ** 2) - ((L ** 2) * (q ** 2))
    if root >= 0:
        n1 = math.sqrt(root)
        n2 = -l_ab * beta * (minr ** 2) - kv * L
        denominator = L * ((beta ** 2) * (minr ** 2) - 1)        
        # denominator should never be zero, but you can never be too careful
        if denominator != 0:
            r.append((n1 + n2) / denominator)
            r.append((-n1 + n2) / denominator)
    return r
    
    
    
    
    
    
    
    
    
    
    
    