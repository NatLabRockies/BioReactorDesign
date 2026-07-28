import os

import numpy as np

from bird import logger

from .case_times import (
    _get_mesh_time,
    _get_volume_time,
    get_case_times,
)
from .foam_dict_io import read_openfoam_dict
from .foam_field_io import read_field


def _read_mesh(filename: str) -> np.ndarray:
    """
    Reads cell center location from meshCellCentres_X.obj

    Parameters
    ----------
    filename: str
        meshCellCentres_X.obj filename

    Returns
    -------
    cell_centers: np.ndarray
        Array (N,3) representing the cell centers (N is number of cells)
    """

    assert "meshCellCentres" in filename
    assert ".obj" in filename
    cell_centers = np.loadtxt(filename, usecols=(1, 2, 3))
    return cell_centers


def read_cell_centers(
    case_folder: str,
    cell_centers_file: str | None = None,
    field_dict: dict | None = None,
) -> tuple[np.ndarray, dict]:
    """
    Read field of cell centers and store it in dictionary for later reuse

    Parameters
    ----------
    case_folder: str
        Path to case folder
    cell_centers_file : str
        Filename of cell center data
        If None, find the cell center file automoatically
    field_dict : dict | None
        Dictionary of fields used to avoid rereading the same fields to calculate different quantities

    Returns
    ----------
    cell_centers : np.ndarray
        cell centers read from file
    field_dict : dict
        Dictionary of fields read
    """
    if field_dict is None:
        field_dict = {}

    if (
        not ("cell_centers" in field_dict)
        or field_dict["cell_centers"] is None
    ):
        if cell_centers_file is None:
            # try to find the mesh time
            mesh_time = _get_mesh_time(case_folder)
            if mesh_time is not None:
                cell_centers_file = f"meshCellCentres_{mesh_time}.obj"

        try:
            cell_centers = _read_mesh(
                os.path.join(case_folder, cell_centers_file)
            )
            field_dict["cell_centers"] = cell_centers

        except FileNotFoundError:

            error_msg = f"Could not find {cell_centers_file}"
            error_msg += "You can generate it with\n\t"
            error_msg += f"`writeMeshObj -case {case_folder}`\n"
            time_float, time_str = get_case_times(case_folder)
            correct_path = f"meshCellCentres_{time_str[0]}.obj"
            if not correct_path == cell_centers_file:
                error_msg += (
                    f"And adjust the cell center file path to {correct_path}"
                )
            logger.error(error_msg)
            raise FileNotFoundError(error_msg)
    else:
        cell_centers = field_dict["cell_centers"]

    return cell_centers, field_dict


def read_cell_volumes(
    case_folder: str,
    time_folder: str | None = None,
    n_cells: int | None = None,
    field_dict: dict | None = None,
) -> tuple[np.ndarray | float, dict]:
    """
    Read volume at a given time and store it in dictionary for later reuse

    Parameters
    ----------
    case_folder: str
        Path to case folder
    time_folder: str | None
        Name of time folder to analyze.
        If None, it will be found automatically
    n_cells : int | None
        Number of cells in the domain.
        If None, it will deduced from the field reading
    field_dict : dict | None
        Dictionary of fields used to avoid rereading the same fields to calculate different quantities

    Returns
    ----------
    cell_volumes : np.ndarray | float
        Field of cell volumes
    field_dict : dict
        Dictionary of fields read
    """
    if field_dict is None:
        field_dict = {}

    kwargs_vol = {
        "case_folder": case_folder,
        "time_folder": time_folder,
        "n_cells": n_cells,
    }

    if not ("V" in field_dict) or field_dict["V"] is None:
        if time_folder is None:
            # Find the time at which the volume was printed
            time_folder = _get_volume_time(case_folder)
            kwargs_vol["time_folder"] = time_folder
        try:
            cell_volumes, field_dict = read_field(
                field_name="V", field_dict=field_dict, **kwargs_vol
            )

        except FileNotFoundError:
            error_msg = f"Could not find {os.path.join(case_folder, time_folder, 'V')}\n"
            time_float, time_str = get_case_times(case_folder)
            error_msg += "You can generate V with\n\t"
            error_msg += f"`postProcess -func writeCellVolumes -time {time_str[0]} -case {case_folder}`"
            logger.error(error_msg)
            raise FileNotFoundError(error_msg)
    else:
        # Get field from dict if it has been read before
        cell_volumes = field_dict["V"]

    return cell_volumes, field_dict


def read_bubble_diameter(
    case_folder: str,
    time_folder: str | None = None,
    n_cells: int | None = None,
    field_dict: dict | None = None,
) -> tuple[np.ndarray | float, dict]:
    """
    Read bubble diameter at a given time and store it in dictionary for later reuse.
    A specific function is constructed so that if d.gas is not available, the bubble
    diameter is read from phaseProperties.

    Parameters
    ----------
    case_folder: str
        Path to case folder
    time_folder: str | None
        Name of time folder to analyze.
        If None, it will be found automatically
    n_cells : int | None
        Number of cells in the domain.
        If None, it will deduced from the field reading
    field_dict : dict | None
        Dictionary of fields used to avoid rereading the same fields to calculate different quantities

    Returns
    ----------
    d_gas : np.ndarray | float
        Field of bubble diameters
    field_dict : dict
        Dictionary of fields read
    """

    if field_dict is None:
        field_dict = {}

    kwargs = {
        "case_folder": case_folder,
        "time_folder": time_folder,
        "n_cells": n_cells,
    }

    if not ("d.gas" in field_dict) or field_dict["d.gas"] is None:
        try:
            d_gas, field_dict = read_field(
                field_name="d.gas", field_dict=field_dict, **kwargs
            )

        except FileNotFoundError as err:
            logger.debug(
                "Could not find d.gas, checking if bubble size model is constant"
            )
            # d.gas does not exist, it might be because a constant bubble diameter model is used
            phaseProperties_dict = read_openfoam_dict(
                os.path.join(case_folder, "constant", "phaseProperties")
            )
            # If the bubble size model is not constant, raise original error
            if (
                not phaseProperties_dict["gas"]["diameterModel"].lower()
                == "constant"
            ):
                logger.error(
                    f"Bubble size model is not constant ({phaseProperties_dict['gas']['diameterModel']}), yet could not find d.gas"
                )
                raise FileNotFoundError(err)
            else:
                # Get the constant bubble diameter
                logger.debug("Reading bubble diameter from phaseProperties")
                d_gas = float(
                    phaseProperties_dict["gas"]["constantCoeffs"]["d"]
                )
                field_dict["d.gas"] = d_gas
    else:
        # Get field from dict if it has been read before
        d_gas = field_dict["d.gas"]

    return d_gas, field_dict


def read_size_groups(case_folder: str) -> dict:
    """
    Get the bubble size groups represented by the number density fields (fX.gas)

    Parameters
    ----------
    case_folder: str
        Path to case folder

    Returns
    ----------
    ndf_groups: dict
        Dictionary describing the number density fields
        Key is the name of the number density field (fX)
        Value is a dictionary with keys 'diam' and 'bin_size'
        corresponding to the bubble diameter and the bin size in m
    """

    phaseProperties_file = os.path.join(
        case_folder, "constant", "phaseProperties"
    )
    phaseProperties = read_openfoam_dict(phaseProperties_file)

    # Make sure that population balance is used
    try:
        assert phaseProperties["populationBalances"] == ["bubbles"]
        assert phaseProperties["gas"]["diameterModel"] == "velocityGroup"
        assert (
            phaseProperties["gas"]["velocityGroupCoeffs"]["populationBalance"]
            == "bubbles"
        )
    except AssertionError:
        logger.warning(
            "Reading size groups for a case where population balance is not used"
        )

    size_grouptmp = phaseProperties["gas"]["velocityGroupCoeffs"]["sizeGroups"]
    logger.debug(f"Found {len(size_grouptmp)} number density fields")

    # Associate number density field to size
    size_group = {}
    for name in size_grouptmp:
        size_group[name] = float(size_grouptmp[name]["dSph"])

    # Sort by size in ascending order
    size_group = dict(sorted(size_group.items(), key=lambda item: item[1]))

    # Get the bin size
    bin_size_group = {}
    group_names = list(size_group.keys())
    logger.warning(
        "The bin sizes definition make assumption of uniformity and need to be revisited if used"
    )
    for igroup, name in enumerate(group_names):
        if igroup == 0:
            bin_size = (
                size_group[group_names[igroup + 1]]
                - size_group[group_names[igroup]]
            )
        elif igroup == len(group_names) - 1:
            bin_size = (
                size_group[group_names[igroup]]
                - size_group[group_names[igroup - 1]]
            )
        else:
            bin_size_p = (
                size_group[group_names[igroup + 1]]
                - size_group[group_names[igroup]]
            )
            bin_size_m = (
                size_group[group_names[igroup]]
                - size_group[group_names[igroup - 1]]
            )
            assert abs(bin_size_p - bin_size_m) < 1e-12
            bin_size = bin_size_m
        bin_size_group[name] = bin_size

    # Put size and bin size together
    ndf_groups = {}
    for name in group_names:
        ndf_groups[name] = {
            "diam": size_group[name],
            "bin_size": bin_size_group[name],
        }

    return ndf_groups


def read_surface_field_value(filename: str) -> float:
    """
    Read the first data row of an OpenFOAM surfaceFieldValue output file

    The leading '#' comment lines are skipped rather than assuming a fixed
    header length, so the parse stays correct when the number of comment lines
    changes across OpenFOAM versions.

    Parameters
    ----------
    filename: str
        Path to the surfaceFieldValue.dat file

    Returns
    ----------
    value: float
        Last column of the first data row
    """
    with open(filename, "r") as f:
        for line in f:
            if line.strip().startswith("#") or not line.strip():
                continue
            return float(line.split()[-1])
    raise ValueError(f"No data rows found in {filename}")
