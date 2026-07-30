import numpy as np
import pytest

from bird.utilities.mathtools import bissection, conditional_average


def test_conditional_average():
    nbins = 32
    rng = np.random.default_rng(0)
    x = rng.uniform(0.0, 3.0, 5000)
    y = 2.0 * np.sin(x) + 0.5

    x_cond, y_cond = conditional_average(x, y, nbins=nbins)
    assert x_cond.shape == (nbins,)
    assert y_cond.shape == (nbins,)
    # Bin centers must be sorted and bracket the data
    assert np.all(np.diff(x_cond) > 0)
    assert x_cond[0] < np.amin(x)
    assert x_cond[-1] > np.amax(x)

    # A constant field averages to that constant in every populated bin
    _, y_const = conditional_average(x, np.full_like(x, 7.0), nbins=nbins)
    populated = ~np.isnan(y_const)
    assert np.all(populated)
    assert np.allclose(y_const[populated], 7.0)

    # The weights depend only on x, so shifting y shifts the conditional
    # average by the same constant. This is what pins the weights to x
    _, y_shift = conditional_average(x, y + 1000.0, nbins=nbins)
    assert np.allclose(y_shift, y_cond + 1000.0)

    # Scaling y scales the conditional average
    _, y_scale = conditional_average(x, 3.0 * y, nbins=nbins)
    assert np.allclose(y_scale, 3.0 * y_cond)

    # A smooth function is recovered at the bin centers
    interior = (x_cond > np.amin(x)) & (x_cond < np.amax(x))
    assert np.allclose(
        y_cond[interior], 2.0 * np.sin(x_cond[interior]) + 0.5, atol=2e-2
    )

    # Empty bins are NaN rather than raising or warning
    x_gap = np.concatenate([rng.uniform(0.0, 1.0, 500), [10.0]])
    y_gap = np.ones_like(x_gap)
    with np.errstate(all="raise"):
        _, y_cond_gap = conditional_average(x_gap, y_gap, nbins=nbins)
    assert np.any(np.isnan(y_cond_gap))
    assert np.allclose(y_cond_gap[~np.isnan(y_cond_gap)], 1.0)

    # A 2D column vector is accepted and gives the same answer as 1D
    _, y_col = conditional_average(
        x.reshape(-1, 1), y.reshape(-1, 1), nbins=nbins
    )
    assert np.allclose(y_col, y_cond, equal_nan=True)

    # x must span a finite range
    with pytest.raises(ValueError):
        conditional_average(np.full(50, 2.0), rng.normal(size=50))

    # Mismatched lengths are rejected
    with pytest.raises(AssertionError):
        conditional_average(x, y[:-1], nbins=nbins)


def test_bissection():
    # Recover the argument of a monotonically increasing function
    x_found = bissection(8.0, lambda x: x**3, x_min=1e-3, x_max=1e3)
    assert abs(x_found - 2.0) < 1e-6

    # Works for a decreasing function too
    x_found = bissection(0.25, lambda x: 1.0 / x, x_min=1e-3, x_max=1e3)
    assert abs(x_found - 4.0) < 1e-6

    # Fewer iterations gives a coarser answer
    x_coarse = bissection(8.0, lambda x: x**3, num_iter=5, x_min=1e-3)
    assert abs(x_coarse - 2.0) > 1e-6

    # A target outside the bracket has no guaranteed solution
    with pytest.raises(ValueError):
        bissection(8.0, lambda x: x**3, x_min=3.0, x_max=1e3)
