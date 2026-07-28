import pytest

from bird.meshing._mesh_tools import radialCoarsening, verticalCoarsening


def test_verticalCoarsening():
    """
    Test vertical coarsening scaling and the one-ratio-per-block guard
    """
    # Two vertical blocks, second one refined by a factor 2
    NVert = [4, 4]
    ratio_properties = [{"ratio": 1.0}, {"ratio": 2.0}]
    NVert_out, _, _, _ = verticalCoarsening(
        ratio_properties=ratio_properties,
        ref_block=0,
        NVert=NVert,
        L=[0.0, 10.0, 20.0],
        smooth=False,
    )
    assert NVert_out[0] == 4
    assert NVert_out[1] == 8

    # More coarsening entries than blocks is rejected with a clear error
    # rather than an IndexError deep in the scaling loop
    with pytest.raises(ValueError):
        verticalCoarsening(
            ratio_properties=[{"ratio": 1.0}] * 3,
            ref_block=0,
            NVert=[4, 4],
            L=[0.0, 10.0, 20.0],
            smooth=False,
        )


def test_radialCoarsening():
    """
    Test radial coarsening scaling and the one-ratio-per-block guard
    """
    NR = [4, 4]
    ratio_properties = [{"ratio": 1.0}, {"ratio": 2.0}]
    NR_out, _, _, _ = radialCoarsening(
        ratio_properties=ratio_properties,
        ref_block=0,
        NR=NR,
        R=[1.0, 2.0],
        smooth=False,
    )
    assert NR_out[0] == 4
    assert NR_out[1] == 8

    with pytest.raises(ValueError):
        radialCoarsening(
            ratio_properties=[{"ratio": 1.0}] * 3,
            ref_block=0,
            NR=[4, 4],
            R=[1.0, 2.0],
            smooth=False,
        )
