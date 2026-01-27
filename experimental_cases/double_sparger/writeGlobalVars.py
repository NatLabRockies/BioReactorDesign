import os

import numpy as np

from bird.utilities.ofio import *


def writeGvars(inletA, liqVol):
    filename_tmp = os.path.join("constant", "globalVars_temp")
    with open(filename_tmp, "r+") as f:
        lines = f.readlines()
    filename = os.path.join("constant", "globalVars")
    with open(filename, "w+") as f:
        for line in lines:
            if line.startswith("inletA"):
                f.write(f"inletA\t{inletA:g};\n")
            elif line.startswith("liqVol"):
                f.write(f"liqVol\t{liqVol:g};\n")
            else:
                f.write(line)


def readInletArea():
    filename_top = os.path.join(
        "postProcessing",
        "patchIntegrate(patch=inlet_sparger_top,field=alpha.gas)",
        "0",
        "surfaceFieldValue.dat",
    )
    filename_bottom = os.path.join(
        "postProcessing",
        "patchIntegrate(patch=inlet_sparger_bottom,field=alpha.gas)",
        "0",
        "surfaceFieldValue.dat",
    )
    with open(filename_top, "r+") as f:
        lines_top = f.readlines()
    with open(filename_bottom, "r+") as f:
        lines_bottom = f.readlines()
    return float(lines_top[4].split()[-1]) + float(lines_bottom[4].split()[-1])


def getLiqVol():
    volume_field, _ = read_cell_volumes(".")
    alpha_field, _ = read_field(".", "0", field_name="alpha.liquid")
    return np.sum(volume_field * alpha_field)


if __name__ == "__main__":
    A = readInletArea()
    V = getLiqVol()
    writeGvars(A, V)
