import numpy as np

from bird import logger
from bird.utilities.ofio import read_cell_centers, read_field


def _weighted_average(
    quantity: float | np.ndarray, weights: float | np.ndarray
) -> float:
    """
    Weighted average of a quantity over the cells it was filtered to

    Parameters
    ----------
    quantity: float | np.ndarray
        Quantity to average, either per cell or uniform
    weights: float | np.ndarray
        Averaging weights, typically the cell volumes optionally scaled by a
        volume fraction

    Returns
    ----------
    average: float
        Weighted average of the quantity
    """
    return np.sum(quantity * weights) / np.sum(weights)


def _field_filter(
    field: float | np.ndarray, ind: np.ndarray | None, field_type: str
) -> float | np.ndarray:
    """
    Filter field by index. Handle uniform and non uniform fields

    Parameters
    ----------
    field: float | np.ndarray
        Field to filter
    ind: np.ndarray | None
        Cell indices to keep.
        None keeps the whole domain, see _get_ind_liq
    field_type : str
        Type of the field ("scalar" or "vector")

    Returns
    ----------
    filtered_field: float | np.ndarray
        Field filtered by cell indices

    """
    if field_type.lower() not in ["scalar", "vector"]:
        msg = f"Field type ({field_type}) not recognized"
        msg += " Supported field types are 'scalar' and 'vector'"
        raise NotImplementedError(msg)

    # No index means the selection covers the whole domain, so nothing is
    # filtered out
    if ind is None:
        return field

    if field_type.lower() == "scalar":
        if isinstance(field, np.ndarray):
            if len(field.shape) > 1:
                err_msg = f"Scalar field shape {field.shape} but expected a flat array"
                raise ValueError(err_msg)
            filtered_field = field[ind]
        elif isinstance(field, float):
            # Uniform field
            filtered_field = field
        else:
            err_msg = f"Got field type {type(field)}."
            err_msg += " Expected float or np.ndarray for scalar field"
            raise TypeError(err_msg)

    else:
        if isinstance(field, np.ndarray):
            if field.shape == (3,):
                # Uniform field
                filtered_field = field
            else:
                filtered_field = field[ind]
        else:
            err_msg = f"Got field type {type(field)}."
            err_msg += " Expected np.ndarray for vector field"
            raise TypeError(err_msg)

    return filtered_field


def _get_ind_liq(
    case_folder: str,
    time_folder: str,
    threshold: float = 0.5,
    n_cells: int | None = None,
    field_dict: dict | None = None,
) -> tuple[np.ndarray | None, dict]:
    """
    Get indices of pure liquid cells (where alpha.liquid > threshold)
    Threshold is 0.5 by default

    Parameters
    ----------
    case_folder: str
        Path to case folder
    time_folder: str
        Name of time folder to analyze
    threshold: float
        Liquid is when alpha_liq > threshold
        Assumes threshold = 0.5 by default
    n_cells : int | None
        Number of cells in the domain.
        If None, it will deduced from the field reading
    field_name: str
        Name of the field file to read
    field_dict : dict | None
        Dictionary of fields used to avoid rereading the same fields to calculate different quantities

    Returns
    ----------
    ind_liq : np.ndarray | None
        indices of pure liquid cells.
        None if the whole domain is liquid, see _field_filter
    field_dict : dict
        Dictionary of fields read
    """
    if field_dict is None:
        field_dict = {}

    assert threshold <= 1
    assert threshold >= 0

    logger.warning(
        f"Assuming that alpha_liq > {threshold} denotes pure liquid"
    )

    # Compute indices of pure liquid. Unlike the cached fields, None is a
    # meaningful value here, so only the absence of the key means "not read"
    if "ind_liq" not in field_dict:
        alpha_liq, field_dict = read_field(
            case_folder,
            time_folder,
            field_name="alpha.liquid",
            n_cells=n_cells,
            field_dict=field_dict,
        )
        # Uniform and non uniform fields are treated differently. A non
        # uniform field holds one value per cell and can be compared cell by
        # cell. A uniform field holds a single value for the whole domain, so
        # either every cell is liquid or none of them is
        if np.ndim(alpha_liq) > 0:
            ind_liq = np.argwhere(alpha_liq > threshold)[:, 0]
        elif alpha_liq > threshold:
            # Every cell is liquid, so no filtering is needed
            ind_liq = None
        else:
            # No cell is liquid
            ind_liq = np.array([], dtype=int)
        field_dict["ind_liq"] = ind_liq
    else:
        ind_liq = field_dict["ind_liq"]

    return ind_liq, field_dict


def _get_ind_gas(
    case_folder: str,
    time_folder: str,
    threshold: float = 0.5,
    n_cells: int | None = None,
    field_dict: dict | None = None,
) -> tuple[np.ndarray | None, dict]:
    """
    Get indices of pure gas cells (where alpha.liquid <= threshold)
    Threshold is 0.5 by default

    Parameters
    ----------
    case_folder: str
        Path to case folder
    time_folder: str
        Name of time folder to analyze
    threshold: float
        Gas is when alpha_liq <= threshold
        Assumes threshold = 0.5 by default
    n_cells : int | None
        Number of cells in the domain.
        If None, it will deduced from the field reading
    field_name: str
        Name of the field file to read
    field_dict : dict | None
        Dictionary of fields used to avoid rereading the same fields to calculate different quantities

    Returns
    ----------
    ind_gas : np.ndarray | None
        indices of pure gas cells.
        None if the whole domain is gas, see _field_filter
    field_dict : dict
        Dictionary of fields read
    """
    if field_dict is None:
        field_dict = {}

    assert threshold <= 1
    assert threshold >= 0

    logger.warning(f"Assuming that alpha_liq <= {threshold} denotes pure gas")

    # Compute indices of pure gas. Unlike the cached fields, None is a
    # meaningful value here, so only the absence of the key means "not read"
    if "ind_gas" not in field_dict:
        alpha_liq, field_dict = read_field(
            case_folder,
            time_folder,
            field_name="alpha.liquid",
            n_cells=n_cells,
            field_dict=field_dict,
        )
        # Uniform and non uniform fields are treated differently. A non
        # uniform field holds one value per cell and can be compared cell by
        # cell. A uniform field holds a single value for the whole domain, so
        # either every cell is gas or none of them is
        if np.ndim(alpha_liq) > 0:
            ind_gas = np.argwhere(alpha_liq <= threshold)[:, 0]
        elif alpha_liq <= threshold:
            # Every cell is gas, so no filtering is needed
            ind_gas = None
        else:
            # No cell is gas
            ind_gas = np.array([], dtype=int)
        field_dict["ind_gas"] = ind_gas
    else:
        ind_gas = field_dict["ind_gas"]

    return ind_gas, field_dict


def _get_ind_slice(
    case_folder: str,
    location: float,
    direction: int | None = None,
    tolerance: float | None = None,
    cell_centers_file: str | None = None,
    field_dict: dict | None = None,
) -> tuple[np.ndarray | float, dict]:
    """
    Get indices of cells along a slice given by a direction and a location

    Parameters
    ----------
    case_folder: str
        Path to case folder
    location: float
        Axial location where to pick the cells
        If outside mesh bounds, will raise an error
    direction :  int
        Direction along which to calculate the superficial velocity.
        Must be in [0, 1, 2].
        If None, assume y direction
    tolerance : float
        Include cells where location is in [location - tolerance , location + tolerance].
        If None, it will be 2 times the axial mesh size
    cell_centers_file : str | None
        Filename of cell center data
        If None, finds cell center file automatically
    field_dict : dict
        Dictionary of fields used to avoid rereading the same fields to calculate different quantities

    Returns
    ----------
    ind_location : np.ndarray
        indices of cells along the desired slice
    field_dict : dict
        Dictionary of fields read
    """
    if field_dict is None:
        field_dict = {}

    if not (f"ind_location_{location:.2g}" in field_dict):

        cell_centers, field_dict = read_cell_centers(
            case_folder=case_folder,
            cell_centers_file=cell_centers_file,
            field_dict=field_dict,
        )

        if direction is None:
            logger.warning(
                "Assuming that axial direction is along the y direction"
            )
            direction = 1

        assert direction in [0, 1, 2]

        axial_cell_centers = np.sort(np.unique(cell_centers[:, direction]))
        if (
            location < axial_cell_centers.min()
            or location > axial_cell_centers.max()
        ):
            raise ValueError(
                f"Location {location:.2g} outside the mesh [{axial_cell_centers.min()}, {axial_cell_centers.max()}]"
            )

        if tolerance is None:
            ind_location_unique = np.argmin(abs(axial_cell_centers - location))
            if ind_location_unique == 0:
                tolerance = 2 * (axial_cell_centers[1] - axial_cell_centers[0])
            elif ind_location_unique == len(axial_cell_centers) - 1:
                tolerance = 2 * (
                    axial_cell_centers[-1] - axial_cell_centers[-2]
                )
            else:
                tolerance = (
                    axial_cell_centers[ind_location_unique + 1]
                    - axial_cell_centers[ind_location_unique - 1]
                )
            logger.debug(
                f"Tolerance for slice location not set, assuming {tolerance:.2g}"
            )

        # Do the actual filtering
        ind_location = np.argwhere(
            abs(cell_centers[:, direction] - location) <= tolerance
        )

        n_cells_location = len(ind_location)

        if n_cells_location == 0:
            raise ValueError(
                f"No cell found for location {location:.2g}, increase tolerance or check if location {location:.2g} is valid"
            )

        logger.debug(
            f"Found {n_cells_location} cells around location {location:.2g}"
        )
        field_dict[f"ind_location_{location:.2g}"] = ind_location

    else:
        ind_location = field_dict[f"ind_location_{location:.2g}"]

    return ind_location, field_dict
