import os

import numpy as np

from bird import logger


def get_case_times(
    case_folder: str, remove_zero: bool = False
) -> tuple[list[float], list[str]]:
    """
    Get list of all time folders from an OpenFOAM case

    Parameters
    ----------
    case_folder: str
        Path to case folder
    remove_zero : bool
        Whether to remove zero from the time folder list

    Returns
    -------
    time_float_sorted: list[float]
        List of time folder values in ascending order
    time_str_sorted: list[str]
        List of time folder names in ascending order

    """
    # Read Time
    times_tmp = os.listdir(case_folder)
    # remove non floats
    for i, entry in reversed(list(enumerate(times_tmp))):
        try:
            a = float(entry)
            if remove_zero:
                if abs(a) < 1e-12:
                    _ = times_tmp.pop(i)
        except ValueError:
            logger.debug(f"{entry} not a time folder, removing")
            a = times_tmp.pop(i)
            # print('removed ', a)
    time_float = [float(entry) for entry in times_tmp]
    time_str = [entry for entry in times_tmp]
    index_sort = np.argsort(time_float)
    time_float_sorted = [time_float[i] for i in list(index_sort)]
    time_str_sorted = [time_str[i] for i in list(index_sort)]

    return time_float_sorted, time_str_sorted


def _get_mesh_time(case_folder: str) -> str | None:
    """
    Get the time at which the mesh was printed

    Parameters
    ----------
    case_folder: str
        Path to case folder

    Returns
    ----------
    time_mesh: str | None
        The name of the time at which "meshCellCentresXXX" was created
        If None, nothing was found
    """

    files_tmp = os.listdir(case_folder)
    time_mesh = None
    for entry in files_tmp:
        if "meshCellCentres" in entry:
            time_mesh = entry[16:-4]

    return time_mesh


def _get_volume_time(case_folder: str) -> str | None:
    """
    Get the time at which the volume was printed

    Parameters
    ----------
    case_folder: str
        Path to case folder

    Returns
    ----------
    time_volume: str | None
        The name of the time at which "V" was created
        If None, nothing was found
    """

    time_float, time_str = get_case_times(case_folder)
    time_volume = None
    for entry in time_str:
        if os.path.exists(os.path.join(case_folder, entry, "V")):
            logger.debug(f"Volume time found to be {entry}")
            time_volume = entry
            break

    return time_volume
