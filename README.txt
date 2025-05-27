This repository contains code for review, associated with a submission to the 
International Journal of Geographical Information Science. 
It is assumed that you already have python v.3x installed and know how to 
run basic python modules.

To run this code, you will first need to install the following python packages 
(you are recommended to first clone your python environment):
•	rtree (https://www.lfd.uci.edu/~gohlke/pythonlibs/#rtree)
    o	download the appropriate one of the following to your python scripts folder:
        o	Rtree-0.8.3-cp27-cp27m-win32.whl
        o	Rtree-0.8.3-cp27-cp27m-win_amd64.whl
    o	open a command-prompt as an administrator
    o	navigate to python scripts folder
    o	uninstall any previous version, just in case, by entering:
        o	pip uninstall rtree
    o	install by entering e.g.:
        o	pip install Rtree-0.8.3-cp27-cp27m-win32.whl
•	sortedcontainers (https://pypi.python.org/pypi/sortedcontainers)
•	pyshp (https://pypi.org/project/pyshp/)
•	numpy, scipy, matplotlib

Run the following modules to reconstruct figures and data in the submitted manuscript:
•	Figure 2: figure_2_hausdorff_comparison.py
•	Figures 6, 7 & 12: animation_creator.py
•	Figure 10: figure_10a_construct_images.py, figure_10b_tile_images.py
•	Figure 11: data are contained in the folder “sample_data”.
•	Figure 12 & Table 2: figure_12_table_2_timing_comparison.py
•	Figure 13: figure_13_computational_efficiency_analysis.py
