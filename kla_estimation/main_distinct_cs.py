import argparse
import os

import numpy as np
from utils import read_raw_data

from bird import logger
from bird.postprocess.kla_utils import compute_kla, print_res_dict

raw_data = read_raw_data()
scfh_list = [1, 2, 3]

for scfh in scfh_list:
    for idata, data in enumerate(raw_data[f"{scfh}_scfh"]):
        logger.info(f"{scfh} SCFH, curve {idata}")
        t = data["t_s"]
        c = data["c_mol_m3"]
        res_dict = compute_kla(
            t,
            c,
            bootstrap=True,
            num_bootstraps=10,
        )
        print_res_dict(res_dict)
