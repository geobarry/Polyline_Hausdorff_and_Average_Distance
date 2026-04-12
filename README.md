This repository contains code for review, associated with a submission to the 
International Journal of Geographical Information Science. 
It is assumed that you already have python v.3x installed and know how to 
run basic python modules.

To run this code, you will first need to install the following python packages 
(you are recommended to first clone your python environment):
- rtree (https://www.lfd.uci.edu/~gohlke/pythonlibs/#rtree)
    - download the appropriate one of the following to your python scripts folder:
        - Rtree-0.8.3-cp27-cp27m-win32.whl
        - Rtree-0.8.3-cp27-cp27m-win_amd64.whl
    - open a command-prompt as an administrator
    - navigate to python scripts folder
    - uninstall any previous version, just in case, by entering:
        - pip uninstall rtree
    - install by entering e.g.:
        - pip install Rtree-0.8.3-cp27-cp27m-win32.whl
- sortedcontainers (https://pypi.python.org/pypi/sortedcontainers)
- pyshp (https://pypi.org/project/pyshp/)
- numpy, scipy, matplotlib (these come with most python installations already)

Run the following modules to reconstruct figures and data in the submitted manuscript. 
You should be able to just run each module without altering anything, but explanations 
and optional parameters to modify (e.g. folders to save results to) are at the top
of each module:
- Figure 1: figure_1_hausdorff_comparison.py
- Figure 8: figure_8a_construct_images.py, figure_8b_tile_images.py
- Figure 9: data are contained in the folder “sample_data”.
- Figure 10: figure_10_computational_efficiency_analysis.py
- Figure 11 & Table 3: figure_11_table_3_discrete_comparison.py

You can also view sample animations contained in the animations folder.