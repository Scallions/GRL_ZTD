# some common codes
import numpy as np
import pandas as pd

def read_sites():
    """read site meta data from csv file

    Returns:
        [site_metadata]: metadata of radio sites
    """
    sites = []
    with open("temp/wyoming_sites.csv", "r") as f:
        for line in f.readlines():
            data = line.split()
            sites.append(data)
    return sites


