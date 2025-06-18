# -*- coding: utf-8 -*-
"""
Created on Sat May 25 19:14:09 2024

@author: Administrator
"""
import discernability
import utils_discernability
import utils_data
import utils_hausdorff
import utils_geom

def test_discernability_score():
    rect = [(0,0),(10,0),(10,10),(0,10),(0,0)]
    poly = [(0,0),(10,0),(20,0),(30,0),(40,0)]
    conflicts = [(0.2,0.7),(1.0,1.5),(3.0,3.5)]
    print("TESTING INDIVIDUAL CONFLICT LENGTH CALCULATION")
    seg_lens = [10,10,10,10]
    x = utils_discernability.dist_btwn_rel_poss(0.2, 0.7, seg_lens)
    print(f'x: {x} (should be 5)')
    # total conflict length should equal 15
    dmin = 6
    # total poly buffer should equal 2 + 1.5 + 1.5 + 3 + 3 + 3 = 14
    # total rect buffer should equal 3 + 1.5 + 1.5 + 3 + 3 + 3 = 15
    print("TESTING TOTAL SCORE CALCULATION")
    score = discernability.discernability_score(rect, conflicts, dmin)
    print(f"Rectangle score: {score} (should be 29)")
    score = discernability.discernability_score(poly,conflicts,dmin)
    print(f"Polyline score: {score} (should be 29)")
    
def test_polyline_sections_to_shapefile():
    out_folder = r"C:\CaGIS Board Dropbox\cantaloupe bob\Barry\Research\Projects\polyline difference metrics\Hausdorff\data\temp"    
    out_file = f"{out_folder}\\manhattan_sections.shp"
    feat = utils_data.get_sample_feature("manhattan")
    print(len(feat))
    secs = [
            (100.5,120.5),
            (100.5,150.5),
            (250.1,260.7)
        ]
    feat_set = discernability.polyline_sections_to_features(feat, secs)
    utils_data.create_polyline_shapefile(feat_set, out_file)
    print("FINISHED")

def test_sin_theta():
    """Makes sure that sin_theta has the correct sign
        + if distance increases along (a)
        - if distance decreases along (b)
    """
    print("TESTING SIGN OF SINE THETA")
    poly = [(0,0),(10,0),(10,5),(0,10),(0,15),(10,10),(10,25),(0,20),(0,25),(10,30)]
    # wrt poly[0], sin_theta should be negative for poly[2],poly[4]
    # and positive for poly[6],poly[8]
    s1 = utils_hausdorff.segDistRep(poly,poly,0,2)[2]
    s2 = utils_hausdorff.segDistRep(poly,poly,0,4)[2]
    s3 = utils_hausdorff.segDistRep(poly,poly,0,6)[2]
    s4 = utils_hausdorff.segDistRep(poly,poly,0,8)[2]
    print(f's1: {s1} (exp: -)')
    print(f's2: {s2} (exp: -)')
    print(f's3: {s3} (exp: +)')
    print(f's4: {s4} (exp: +)')
    
def test_segDistance():
    print("TESTING SEGMENT GAP (utils_hausdorff)")
    s1 = utils_hausdorff.segDistance((True,-0.3,0.6), 0.5, 10)
    s2 = utils_hausdorff.segDistance((True,1.3,-0.6),0.5,10)
    print(f's1: {s1} (exp: {4.8})')
    print(f's2: {s2} (exp: {4.8})')
    
def test_segDistTrans():
    sin_theta = 0.6
    ks = -2
    L = 10
    gmin = 16.8
    k_trans = utils_discernability.segDistTrans(gmin, ks, L, sin_theta)
    # should be 0.8
    print("TESTING SEGMENT GAP TRANSITION")
    print(f'k_trans: {k_trans} (exp: 0.8)')

def test_segDistPathLen():    
    # test cases based on segments with following coordinates:
    # a: (0,0)-(10,0) 
    # b: (0,4)-(16,16)
    # with various topological possibilities
    b_gt_a = [1,1,-1,-1]
    kb1_gt_kb0 = [-1,1,-1,1]
    beta1 = [-x for x in b_gt_a]
    beta2 = [x * y for x,y in zip(b_gt_a,kb1_gt_kb0)]
    kb0 = [2.8,0.3,2.8,0.3]
    L = 10
    cos_theta = 0.8
    l_a0_b0 = 100
    k = 0.3
    answer = [117,97,83,103]
    lmin = [108,96,92,104]
    data = zip(beta1,beta2,kb0,answer,lmin)    
    print("TESTING SEGMENT PATH LENGTH")
    for beta1,beta2,kb0,answer,lmin in data:
        l_path = utils_discernability.segDistPathLen(
            k,l_a0_b0,beta1,beta2,L,cos_theta,kb0)
        print(f'l_path: {l_path} (exp: {answer})')

def test_segDistPathLenTrans():    
    # test cases based on segments with following coordinates:
    # a: (0,0)-(10,0) 
    # b: (0,4)-(16,16)
    # with various topological possibilities
    b_gt_a = [1,1,-1,-1]
    kb1_gt_kb0 = [-1,1,-1,1]
    beta1 = [-x for x in b_gt_a]
    beta2 = [x * y for x,y in zip(b_gt_a,kb1_gt_kb0)]
    kb0 = [2.8,0.3,2.8,0.3]
    L = 10
    cos_theta = 0.8
    l_a0_b0 = 100
    lmin = [108,96,92,104]
    answer = 0.8
    data = zip(beta1,beta2,kb0,lmin)    
    print("TESTING SEGMENT PATH LENGTH TRANSITION")
    for beta1,beta2,kb0,lmin in data:
        k_trans = utils_discernability.segDistPathLenTrans(
            lmin,l_a0_b0,beta1,beta2,L,cos_theta,kb0)
        print(f'k_trans: {k_trans} (exp: {answer})')

def test_segDistRatioTrans():
    # test based on going from first to last segment of following polyline:
    # [(12,0),(32,0),(32,24),(19.2,14.4),(12,9)]
    print("TESTING SEGMENT RATIO TRANSITION")
    minr = 0.2
    kb0 = 0.9
    l_ab = 60
    beta1 = -1
    beta2 = -1
    L = 20
    ks = -0.6
    sin_theta = 0.6
    cos_theta = 0.8
    r_trans = utils_discernability.segDistRatioTrans(minr,kb0,l_ab,beta1,beta2,L,ks,sin_theta,cos_theta)
    print(f'r_trans: {r_trans} (exp: 0.4,-4.6)')

def test_seg_conflict_region():
    # start = [(0,0),(10,0)]
    # finish = [(16,16),(0,4)]
    # middle = [(53,0),(53,4),(0,4)]
    # poly = start + middle + finish
    # lmin = [108,96,92,104]
    # gmin = 7
    # seg_lens = [utils_geom.distance(poly[v],poly[v+1]) for v in range(len(poly)-1)]
    # secs = utils_discernability.seg_conflict_region(poly,0,len(poly)-2,gmin,lmin[0]-7,seg_lens)
    # print(f'secs: {secs}')

    # minimum gap: 500, minimum path length: 1500
    print("Simple Example With Rectangular Segments")
    gmin = 500
    lmin = 1500
    # square polyline with three segments, 2nd short
    poly = [(0,0.00),(2000,0),(2000,300),(0,300)]
    seg_lens = [utils_geom.distance(poly[v],poly[v+1]) for v in range(len(poly)-1)]
    conflicts = utils_discernability.seg_conflict_region(poly, 0, 2, gmin, lmin, seg_lens, verbose = True)
    print("Expected: (0.0,0.7)")
    print(f'Actual: {conflicts}')

def test_vrtDistance():
    print("TESTING VERTEX GAP (utils_hausdorff)")
    kv = 0.6
    q = 0.4
    L = 10
    s1 = utils_hausdorff.vertDistance((False,kv,q),0.6,L)
    s2 = utils_hausdorff.vertDistance((False,kv,q),0.3,L)
    s3 = utils_hausdorff.vertDistance((False,kv,q),0.9,L)
    print(f's1: {s1} (exp: {4.0})')
    print(f's2: {s2} (exp: {5.0})')
    print(f's3: {s3} (exp: {5.0})')
    
def test_vrtDistPathLen():
    print("TESTING VERTEX PATH LENGTH")
    k = 0.5
    l_ab = 20
    L = 10
    s1 = utils_discernability.vrtDistPathLen(k,l_ab,1,L)
    s2 = utils_discernability.vrtDistPathLen(k,l_ab,-1,L)
    print(f's1: {s1} (exp: {25.0})')
    print(f's2: {s2} (exp: {15.0})')

def test_vrtDistTrans():
    print("TESTING VERTEX GAP TRANSITION")
    gmin = 5
    L = 10
    q = 0.3
    kv = -0.1
    s1 = utils_discernability.vrtDistTrans(gmin,kv,q,L)
    print(f's1: {s1} (exp: {0.3})')
    kv = 0.5
    s2 = utils_discernability.vrtDistTrans(gmin,kv,q,L)
    print(f's2: {s2} (exp: {[0.1,0.9]})')

def test_vrtDistPathLenTrans():
    print("TESTING VERTEX PATH LENGTH TRANSITION")
    lmin = 25
    l_ab = 20
    L = 10
    beta = -1 # b > a, solution = -0.5
    s1 = utils_discernability.vrtDistPathLenTrans(lmin,l_ab,beta,L)
    beta = 1 #b < a, solution = 0.5
    s2 = utils_discernability.vrtDistPathLenTrans(lmin,l_ab,beta,L)
    print(f's1: {s1} (exp: {-0.5})')
    print(f's2: {s2} (exp: {0.5})')

def test_vrtDistRatioTrans():
    print("TESTING VERTEX RATIO TRANSITION")
    minr = 0.2
    kv = -0.2
    q = 0.3
    L = 10
    l_ab = 27
    beta = -1 # b > a
    s1 = utils_discernability.vrtDistRatioTrans(minr,kv,q,L,l_ab,beta)
    print(f's1: {s1} (exp: {0.2})')
    beta = 1 #b < a
    l_ab = 23
    s2 = utils_discernability.vrtDistRatioTrans(minr,kv,q,L,l_ab,beta)
    print(f's2: {s2} (exp: {0.2})')

def test_manhattan_segment_pair(s1,s2,dmin,lmin,minr):
    print("FUNCTION: test_manhattan_segment_pair")
    print(f"s1: {s1} | s2: {s2}")
    poly = utils_data.get_sample_feature("manhattan")
    seg_lens = [utils_geom.distance(poly[v],poly[v+1]) for v in range(len(poly)-1)]
    conflicts = utils_discernability.seg_conflict_region(
        poly, s1, s2, dmin, lmin, minr, seg_lens, verbose = True)    
    print("Finished Function: test_manhattan_segment_pair")

def test_manhattan_segment_vertex(seg,v,dmin,lmin,minr):
    print("FUNCTION: test_manhattan_segment_vertex")
    print(f"seg: {seg} | v: {v}")
    poly = utils_data.get_sample_feature("manhattan")
    seg_lens = [utils_geom.distance(poly[v],poly[v+1]) for v in range(len(poly)-1)]
    conflicts = utils_discernability.vrt_conflict_region(
                    poly, seg, v, dmin, lmin, minr, seg_lens,verbose = True)
    
def test_manhattan_segment(seg,dmin,lmin,minr):
    print("Specific pairs of components in manhattan data")    
    poly = utils_data.get_sample_feature("manhattan")
    print(f"Polyline has {len(poly)} vertices...")
    sw,vw = discernability.conflict_work_lists(poly,dmin)
    print("POTENTIAL SEGMENT CONFLICTS")
    cands = set()
    for fromSeg,toSeg in sw:
        if fromSeg == seg:
            cands.add(toSeg)
        if toSeg == seg:
            cands.add(fromSeg)
    cands = sorted(list(cands))
    print(f'segments: {cands}')
    seg_lens = [utils_geom.distance(poly[v],poly[v+1]) for v in range(len(poly)-1)]
    for cand in cands:      
        conflicts = utils_discernability.seg_conflict_region(poly, seg, cand, dmin, lmin, minr, seg_lens, verbose = False)
        if len(conflicts) > 0:
            print(f'cand: {cand}')
            print(f'conflicts: {conflicts}')
    pts = []
    for fromSeg,v in vw:
        if fromSeg == seg:
            pts.append(v)
    print(f'vertices: {pts}')
    for v in pts:
        conflicts = utils_discernability.vrt_conflict_region(
            poly, seg, v, dmin, lmin, minr, seg_lens)
        if len(conflicts) > 0:
            print(f"v: {v} conflicts: {conflicts}")

#    conflicts = utils_discernability.seg_conflict_region(poly, seg, 187, dmin, lmin, seg_lens, verbose = True)
#    print(f'seg_lens: {seg_lens[187:190]}')
#    print(f"Segment 190: {seg_lens[190]}")

    
def test_discernability_conflicts(feat,out_file,dmin,lmin):
    conflicts = discernability.discernability_conflicts(
        feat, dmin, lmin, verbose = True)
    if len(conflicts) == 0:
        print("No conflicts found!")
    else:
        out_feat = discernability.polyline_sections_to_features(feat,conflicts)
        utils_data.create_polyline_shapefile(out_feat, out_file)
        score = discernability.discernability_score(feat,conflicts,dmin)
        print(f'score: {score}')
    print("Finished.")

  
# test_polyline_sections_to_shapefile()
# test_sin_theta()
# test_segDistance()
# test_segDistTrans()
# test_segDistPathLen()
# test_segDistPathLenTrans()
# test_segDistRatioTrans()

# test_vrtDistance()
# test_vrtDistPathLen()
# test_vrtDistTrans()
# test_vrtDistPathLenTrans()
# test_vrtDistRatioTrans()

# test_seg_conflict_region()

# test_discernability_score()

# test_manhattan_segment(183,50,0,0.334)
# test_manhattan_segment_pair(183,184,50,0,0.334)
# test_manhattan_segment_vertex(43,41,200,0,0.2)

# for mapping at a scale of 1:250,000
# with the minimum gap of 2mm on map
# the minimum gap on earth should be 
# 0.2mm x 250,000 x 1m/1,000mm = 50m
# and we will arbitrarily set the minimum length to 3x that
feat_name = "India_Bangladesh"
dmin = 1600
lmin = dmin * 3
base_folder = r"C:\CaGIS Board Dropbox\cantaloupe bob\Barry\Research\Conferences\CEGIS\2024 Discernability Conflicts\figures"
out_file = f"{base_folder}\\{feat_name}\\conflicts_{dmin}_{lmin}.shp"

print(f"Calculating discernability conflicts for: {feat_name} (dmin = {dmin})")
feat = utils_data.get_sample_feature(feat_name)
print(f"Feature has {len(feat)} vertices...")
test_discernability_conflicts(feat,out_file,dmin,lmin)
