from bird.meshing.block_rect_mesh import from_block_rect_to_seg
from bird.preprocess.dynamic_mixer.mixer import StaticMixer


def test_StaticMixer():
    geom = {
        "OverallDomain": {
            a: {"size_per_block": 1.0, "rescale": 2.76}
            for a in ("x", "y", "z")
        },
        "Fluids": [[[0, 0, 0], [9, 0, 0]]],
    }
    g = from_block_rect_to_seg(geom)

    # loop mode: radius is a fraction of the branch cross-section
    # (0.5 spans the whole tube)
    m = StaticMixer()
    m.update_from_loop_dict(
        {
            "branch_id": 0,
            "frac_space": 0.4,
            "radius": 0.5,
            "sign": "+",
            "swirl_sign": "+",
            "S": 0.35,
            "K": 0.5,
            "start_time": 3,
        },
        g,
    )
    assert m.ready
    assert m.normal_dir == 0
    assert abs(m.R - 0.5 * 2.76) < 1e-9  # frac * mean transverse block size
    assert (m.S, m.K) == (0.35, 0.5)
    assert m.sign == "+" and m.swirl_sign == "+"
    assert m.start_time == 3
    # position = segment start + frac*conn, block size = 2.76
    assert abs(m.x - (0.5 * 2.76 + 0.4 * 9 * 2.76)) < 1e-6
    assert abs(m.y - 0.5 * 2.76) < 1e-6

    # explicit mode: radius is absolute, defaults for S/K
    m2 = StaticMixer()
    m2.update_from_expl_dict(
        {
            "x": 0.1,
            "y": 0.2,
            "z": 0.3,
            "normal_dir": 1,
            "radius": 0.05,
            "sign": "-",
            "swirl_sign": "-",
        }
    )
    assert m2.ready and abs(m2.R - 0.05) < 1e-12 and m2.normal_dir == 1
    assert (m2.S, m2.K) == (0.35, 0.5)  # defaults
    assert m2.sign == "-" and m2.swirl_sign == "-"

    # missing sign leaves the mixer not ready
    m3 = StaticMixer()
    m3.update_from_expl_dict(
        {"x": 0.1, "y": 0.2, "z": 0.3, "normal_dir": 1, "radius": 0.05}
    )
    assert not m3.ready
