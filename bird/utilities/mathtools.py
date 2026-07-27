from typing import Callable

import numpy as np

from bird import logger


def conditional_average(
    x: np.ndarray, y: np.ndarray, nbins: int = 32
) -> tuple[np.ndarray, np.ndarray]:
    """
    Compute a 1D conditional average of y with respect to x
    The conditional average is distributed to neighbors of the binned array when needed

    Parameters
    ----------
    x: np.ndarray
        1D array with respect to which conditional averaged is performed
    y : np.ndarray
        1D array conditioned
    nbins: int
        Number of bins through x

    Returns
    ----------
    x_cond: np.ndarray
        The binned array of values conditioned againsts
    y_cond: np.ndarray
        The conditional averages at each bin.
        Bins that received no sample are NaN
    """
    # Check the shape of input arrays
    try:
        assert len(x.shape) <= 2
        assert len(y.shape) <= 2
        if len(x.shape) == 2:
            assert x.shape[1] == 1
        if len(y.shape) == 2:
            assert y.shape[1] == 1
    except AssertionError:
        error_msg = "conditional average of tensors is ambiguous"
        error_msg += f"\nx shape =  {x.shape}"
        error_msg += f"\ny shape =  {y.shape}"
        logger.error(error_msg)
        raise AssertionError(error_msg)
    if len(x.shape) == 2:
        x = x[:, 0]
    if len(y.shape) == 2:
        y = y[:, 0]
    try:
        assert len(x) == len(y)
    except AssertionError:
        error_msg = "conditional average x and y have different dimension"
        error_msg += f"\ndim x =  {len(x)}"
        error_msg += f"\ndim y =  {len(y)}"
        logger.error(error_msg)
        raise AssertionError(error_msg)

    # Bin conditional space
    mag = np.amax(x) - np.amin(x)
    if mag == 0:
        error_msg = "conditional average needs x to span a finite range"
        error_msg += f"\nall {len(x)} values of x equal {np.amax(x):.4g}"
        logger.error(error_msg)
        raise ValueError(error_msg)
    x_bin = np.linspace(
        np.amin(x) - mag / (2 * nbins), np.amax(x) + mag / (2 * nbins), nbins
    )
    inds = np.digitize(x, x_bin)

    # Linear weights splitting each sample between its two neighboring bins,
    # based on where x falls between the bin edges that bracket it
    a = abs(x - x_bin[inds - 1])
    b = abs(x - x_bin[inds])
    c = a + b
    a = a / c
    b = b / c

    # Accumulate the weights and the weighted values into the bins. Samples in
    # bin `inds` contribute `a` to bin `inds` and `b` to bin `inds - 1`
    n_edges = nbins + 1
    weight = (
        np.bincount(inds, weights=a, minlength=n_edges)[:nbins]
        + np.bincount(inds, weights=b, minlength=n_edges)[1:n_edges]
    )
    weightVal = (
        np.bincount(inds, weights=a * y, minlength=n_edges)[:nbins]
        + np.bincount(inds, weights=b * y, minlength=n_edges)[1:n_edges]
    )

    # Assemble output, leaving bins that received no sample as NaN
    x_cond = x_bin
    y_cond = np.full(nbins, np.nan)
    np.divide(weightVal, weight, out=y_cond, where=weight > 0)

    return x_cond, y_cond


def bissection(
    fun_val: float,
    nonlin_fun: Callable,
    num_iter: int = 1000,
    x_min: float = 1e-6,
    x_max: float = 1e6,
) -> float:
    """
    Solve a 1D non linear equation with a bissection method
    This is useful for adjusting the mesh grading so that mesh size varies smoothly

    Parameters
    ----------
    fun_val:
        Target value for the non linear function
    nonlin_fun:
        Non linear function
    num_iter: int
        Number of bissection iterations
        Defaults to 1000
    x_min : float
        Lower bound of the search interval
        Defaults to 1e-6
    x_max : float
        Upper bound of the search interval
        Defaults to 1e6


    Returns
    ----------
    x_mid: float
        The argument that achieves the desired function value
    """

    # Make sure residual sign changes over the search interval
    residual_min = nonlin_fun(x_min) - fun_val
    residual_max = nonlin_fun(x_max) - fun_val
    if residual_min * residual_max > 0:
        error_msg = "No guaranteed bissection solution"
        error_msg += (
            f"\nSearch interval [{x_min:.4g}, {x_max:.4g}] may be too narrow"
        )
        raise ValueError(error_msg)

    # Do the bissection search
    for i in range(num_iter):
        x_mid = 0.5 * (x_max + x_min)
        residual_mid = nonlin_fun(x_mid) - fun_val
        if residual_mid * residual_max < 0:
            x_min = x_mid
            residual_min = residual_mid
        else:
            x_max = x_mid
            residual_max = residual_mid

    return x_mid
