import argparse
import os

import numpy as np
from utils import read_raw_data

from bird import logger
from bird.postprocess.kla_utils import compute_kla, print_res_dict

raw_data = read_raw_data()
scfh_list = [1, 2, 3]
ind_start_list = [2, 2, 2]

for ind_start, scfh in zip(ind_start_list, scfh_list):
    t_tot = None
    c_tot = None
    for idata, data in enumerate(raw_data[f"{scfh}_scfh"]):
        logger.info(f"{scfh} SCFH, curve {idata}")
        t = data["t_s"][ind_start:]
        c = data["c_mol_m3"][ind_start:]
        if t_tot is None:
            t_tot = t
            c_tot = c
        else:
            t_tot = np.hstack((t_tot, t))
            c_tot = np.hstack((c_tot, c))
    res_dict = compute_kla(t_tot, c_tot, bootstrap=False, do_chop=False)
    print_res_dict(res_dict)
