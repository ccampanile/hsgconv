import sys
import os

#import hsgconv folder
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from hsgconv import GridParams

gp = GridParams("A20",200)

print (gp)