import sys
import os

#import hsgconv folder - this is in case you clone the repo
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from hsgconv import GridParams, ConvertToOSBG, ConvertToLocalGrid

# Example for a scheme near Stevenage, Hertfordshire, England.
# Highway A1, scheme at junctions 6-8.

# Let's take the coordinate of a point in both local and British National grid
pt_loc = (17573.0093, 398330.8085, 99.425508)
pt_nat = (522569.0642, 227241.3843)

# Retrieve transformation parameters
gp = GridParams(gridID="A20", mean_z=96.98)
#NOTE: meanZ is from the centre bounding box of the scheme (not the average of all the points!)
print(gp)

to_nat = ConvertToOSBG(gp, pt_loc[0], pt_loc[1])
print("\nlocal => national: ",to_nat)
to_loc = ConvertToLocalGrid(gp, pt_nat[0], pt_nat[1])
print("national => local: ",to_loc)

#test accuracy. The operation is performed 1000 times
from copy import deepcopy
tmp_loc = deepcopy(pt_loc)
for i in range(1000):
    tmp_nat = ConvertToOSBG(gp, tmp_loc[0], tmp_loc[1])
    tmp_loc = ConvertToLocalGrid(gp, tmp_nat[0], tmp_nat[1])

print  ("\nTotal error on [x,y]: {} (metres)".format([coord[1]-coord[0] for coord in (zip(tmp_loc, pt_loc))]))

# For large dataset, we recommend to implement the functions parallely
