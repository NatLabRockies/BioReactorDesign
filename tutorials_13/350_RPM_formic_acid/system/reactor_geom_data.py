import math
from functools import reduce
from types import SimpleNamespace

import numpy as np

def process(data: str | None):
    pass

# Default parameters
# DEFAULT_N_FINS_PER_IMPELLER = [6, 4]  # listed from bottom to top impeller
DEFAULT_N_FINS_PER_IMPELLER = [6, 6]
# DEFAULT_BLADE_PITCH = [0.0, 15.0]  # listed from bottom to top impeller
DEFAULT_BLADE_PITCH = [0, 0]
# DEFAULT_IMP_SCALE = [18.0 / 22.0, 1.0]  # listed from bottom to top impeller
DEFAULT_IMP_SCALE = [1, 1]
DEFAULT_BLADE_LENGTH_FACTOR = 25
DEFAULT_BLADE_WIDTH_FACTOR = 20
# DEFAULT_IMP_CENTERS = [13.025, 36.025]
DEFAULT_IMP_CENTERS = [15, 65, 115]
DEFAULT_ASPECT_RATIO = 1.63
DEFAULT_TANK_VOLUME = 2000

CUBIC_IN_TO_L = 0.016387064  # 1 in^3 = 0.016387064 L


def cylinder_volume_L(diameter_in: float, height_in: float) -> float:
    return (math.pi * (diameter_in / 2.0) ** 2 * height_in) * CUBIC_IN_TO_L


def solve_cylinder(
    target_volume_L: float,
    aspect_ratio: float | None = None,  # AR = H/D
    tank_diameter: float | None = None,  # inches
    reactor_height: float | None = None,  # inches
):
    """
    Solves for the cylinder geometry using the aspect ratio, tank diameter, or height.
    """
    volume_in3 = target_volume_L / CUBIC_IN_TO_L

    if tank_diameter is not None and reactor_height is not None:
        raise ValueError(
            "Provide only one of tank_diameter or reactor_height (or neither)."
        )

    if tank_diameter is not None:
        tank_diameter_final = float(tank_diameter)
        reactor_height_final = 4.0 * volume_in3 / (math.pi * tank_diameter_final**2)
    elif reactor_height is not None:
        reactor_height_final = float(reactor_height)
        tank_diameter_final = math.sqrt(
            4.0 * volume_in3 / (math.pi * reactor_height_final)
        )
    else:
        if aspect_ratio is None:
            raise ValueError(
                "If neither diameter nor height is provided, aspect_ratio is required."
            )
        aspect_ratio_final = float(aspect_ratio)
        tank_diameter_final = (4.0 * volume_in3 / (math.pi * aspect_ratio_final)) ** (
            1.0 / 3.0
        )
        reactor_height_final = aspect_ratio_final * tank_diameter_final

    aspect_ratio_final = reactor_height_final / tank_diameter_final
    final_volume_L = (
        math.pi * (tank_diameter_final / 2.0) ** 2 * reactor_height_final
    ) * CUBIC_IN_TO_L
    return tank_diameter_final, reactor_height_final, aspect_ratio_final, final_volume_L


def build_geom(
    n_fins_per_impeller=None,
    blade_pitch=None,
    blade_length_factor=None,
    blade_width_factor=None,
    imp_scale=None,
    imp_centers=None,
    round_bottom=True,
    aspect_ratio: float | None = None,  # height/diameter
    target_volume_L: float | None = None,  # target volume in Liters
    **overrides,
):
    """
    Build and return geometry object using defaults or overrides.
    """
    n_fins_per_impeller = n_fins_per_impeller or DEFAULT_N_FINS_PER_IMPELLER
    blade_pitch = blade_pitch or DEFAULT_BLADE_PITCH
    blade_length_factor = blade_length_factor or DEFAULT_BLADE_LENGTH_FACTOR
    blade_width_factor = blade_width_factor or DEFAULT_BLADE_WIDTH_FACTOR
    imp_scale = imp_scale or DEFAULT_IMP_SCALE
    imp_centers = imp_centers or DEFAULT_IMP_CENTERS
    aspect_ratio = aspect_ratio or DEFAULT_ASPECT_RATIO
    target_volume_L = target_volume_L or DEFAULT_TANK_VOLUME

    # convert degrees to radians for blade_pitch
    blade_pitch = [angle * np.pi / 180.0 for angle in blade_pitch]

    # geometry ========
    # # tank_diameter = 42.0
    # # impeller_tip_diameter = 22.0
    # # reactor_height = 68.525

    tank_diameter, reactor_height, ar_final, volume_final = solve_cylinder(
        target_volume_L=target_volume_L,
        aspect_ratio=aspect_ratio,
        tank_diameter=None,
        reactor_height=None,
    )
    print(
        f"Tank diameter: {tank_diameter}, reactor height: {reactor_height}, AR: {ar_final}, volume: {volume_final}"
    )
    impeller_tip_diameter = 0.4 * tank_diameter
    baffle_width = 0.075 * tank_diameter
    polyrad = 1.0

    impeller_centers = imp_centers

    nimpellers = len(impeller_centers)  # number of impellers along the rotating shaft
    nbaffles = 2  # number of baffles on the tank wall

    # n_fins_per_impeller = [6, 4]  # listed from bottom to top impeller
    assert len(n_fins_per_impeller) == nimpellers  # must be length of nimpellers

    # compute least common multiple of n_fins_per_impeller using greatest common divisor
    def _lcm(a, b):
        return a * b // math.gcd(a, b)

    base_counts = [nbaffles] + n_fins_per_impeller
    n_base = reduce(_lcm, base_counts)
    print(f"Least common multiple of baffles and fins: {n_base}")

    # blade_width = base_length / 10  # NOT SURE estimate -- impeller blade width
    blade_width = impeller_tip_diameter / 3
    # blade_width = base_length / blade_width_factor
    # NOT SURE estimate -- impeller blade length (beyond the hub)
    # blade_width = impeller_tip_diameter/5, blade_length = impeller_tip_diameter/4
    # blade_length = base_length / 20
    blade_length = 5
    # blade_length = base_length / blade_length_factor
    hub_diameter = impeller_tip_diameter - 2 * blade_length  # NOT SURE -- Hub Diameter
    inner_blade_length = (
        blade_length  # NOT SURE -- impeller blade length (inside the hub)
    )
    # baffle_width = base_length / 10  # Baffle Width
    baffle_width = tank_diameter /80
    hub_height_width = blade_width / 10  # NOT SURE -- Hub height (Width)
    # polyrad = base_length / 30  # NOT SURE -- Stem radius (R_shaft)
    # polyrad = 1.0
    # imp_scale = [1.5, 0.8]

    reactor_bottom = 0.0  # bottom of reactor
    mrf_region_diameter = (
        impeller_tip_diameter + tank_diameter - 2 * baffle_width
    ) / 2  # MRF region Diameter

    # mesh ========
    mesh_nr = 1  # 50  # 120	      # mesh points per unit radial length
    mesh_nz = 1  # 100  # 240       # mesh points per unit axial length
    n_poly = 2  # 4  # mesh points in the polygon at the axis
    n_azimuth = 3  # mesh points in the azimuthal direction

    # nsplits = 2 * nbaffles  # we need twice the number of splits
    nsplits = 2 * n_base  # we need twice the number of splits
    dangle = 2.0 * np.pi / float(nsplits)  # delta angle between splits

    # blade_pitch = [0.0, 10.0 * np.pi / 180.0]  # blade pitch angles for each impeller

    # if round_bottom:
    # curved bottom params
    curved_bottom_center = [0.0, 0.0, reactor_bottom + 100*reactor_height / 3]
    curved_bottom_edge = [tank_diameter / 2, 0.0, reactor_bottom]
    curved_bottom_radius = np.sqrt(
        (curved_bottom_edge[0] - curved_bottom_center[0]) ** 2
        + (curved_bottom_edge[1] - curved_bottom_center[1]) ** 2
        + (curved_bottom_edge[2] - curved_bottom_center[2]) ** 2
    )

    circradii = np.array(
        [
            imp_scale[0] * (hub_diameter / 2 - inner_blade_length),
            imp_scale[0] * hub_diameter / 2,
            imp_scale[0] * impeller_tip_diameter / 2,
            mrf_region_diameter / 2,
            tank_diameter / 2 - baffle_width,
            tank_diameter / 2,
        ]
    )
    ncirc = len(circradii)
    hub_circ = 1
    inhub_circ = hub_circ - 1  # circle inside hub
    rot_circ = hub_circ + 1
    mrf_circ = rot_circ + 1
    tank_circ = ncirc - 1

    reacthts = [reactor_bottom]
    baff_sections = []
    baff_volumes = []
    hub_volumes = []
    count = 1
    angle_offsets = [0.0]

    for n_imp in range(nimpellers):
        pitch = blade_pitch[n_imp]
        tmp_len = blade_width
        tip_rad = imp_scale[n_imp] * (impeller_tip_diameter / 2.0)
        dz = tmp_len * np.cos(pitch)
        dz_min = hub_height_width * 1.05  # prevents blade from going below rotor hub
        if dz < dz_min:
            dz = dz_min
        dtheta = (tmp_len * np.sin(pitch)) / max(tip_rad, 1e-12)
        zc = reactor_bottom + impeller_centers[n_imp]

        def theta_offset(z):
            return (z - zc) * dtheta / dz

        z0 = zc - dz / 2.0
        # reacthts.append(reactor_bottom + impeller_centers[n_imp] - dz / 2)
        reacthts.append(z0)
        circradii = np.append(
            circradii,
            np.array(
                [
                    imp_scale[n_imp] * (hub_diameter / 2 - inner_blade_length),
                    imp_scale[n_imp] * hub_diameter / 2,
                    imp_scale[n_imp] * impeller_tip_diameter / 2,
                    mrf_region_diameter / 2,
                    tank_diameter / 2 - baffle_width,
                    tank_diameter / 2,
                ]
            ),
        )

        baff_sections.append(count)
        baff_volumes.append(count)
        # angle_offsets.append(-blade_pitch[n_imp])
        angle_offsets.append(theta_offset(z0))
        count = count + 1

        z1 = zc - hub_height_width / 2.0
        # reacthts.append(reactor_bottom + impeller_centers[n_imp] - hub_height_width / 2)
        reacthts.append(z1)
        circradii = np.append(
            circradii,
            np.array(
                [
                    imp_scale[n_imp] * (hub_diameter / 2 - inner_blade_length),
                    imp_scale[n_imp] * hub_diameter / 2,
                    imp_scale[n_imp] * impeller_tip_diameter / 2,
                    mrf_region_diameter / 2,
                    tank_diameter / 2 - baffle_width,
                    tank_diameter / 2,
                ]
            ),
        )

        baff_sections.append(count)
        baff_volumes.append(count)
        hub_volumes.append(count)
        # angle_offsets.append(0.0)
        angle_offsets.append(theta_offset(z1))
        count = count + 1

        z2 = zc + hub_height_width / 2.0
        # reacthts.append(reactor_bottom + impeller_centers[n_imp] + hub_height_width / 2)
        reacthts.append(z2)
        circradii = np.append(
            circradii,
            np.array(
                [
                    imp_scale[n_imp] * (hub_diameter / 2 - inner_blade_length),
                    imp_scale[n_imp] * hub_diameter / 2,
                    imp_scale[n_imp] * impeller_tip_diameter / 2,
                    mrf_region_diameter / 2,
                    tank_diameter / 2 - baffle_width,
                    tank_diameter / 2,
                ]
            ),
        )

        baff_sections.append(count)
        baff_volumes.append(count)
        # angle_offsets.append(0.0)
        angle_offsets.append(theta_offset(z2))
        count = count + 1

        z3 = zc + dz / 2.0
        # reacthts.append(reactor_bottom + impeller_centers[n_imp] + dz / 2)
        reacthts.append(z3)
        circradii = np.append(
            circradii,
            np.array(
                [
                    imp_scale[n_imp] * (hub_diameter / 2 - inner_blade_length),
                    imp_scale[n_imp] * hub_diameter / 2,
                    imp_scale[n_imp] * impeller_tip_diameter / 2,
                    mrf_region_diameter / 2,
                    tank_diameter / 2 - baffle_width,
                    tank_diameter / 2,
                ]
            ),
        )
        baff_sections.append(count)
        # angle_offsets.append(0.5 * blade_pitch[n_imp])
        angle_offsets.append(theta_offset(z3))
        count = count + 1

    reacthts.append(reactor_bottom + reactor_height)
    circradii = np.append(
        circradii,
        np.array(
            [
                imp_scale[-1] * (hub_diameter / 2 - inner_blade_length),
                imp_scale[-1] * hub_diameter / 2,
                imp_scale[-1] * impeller_tip_diameter / 2,
                mrf_region_diameter / 2,
                tank_diameter / 2 - baffle_width,
                tank_diameter / 2,
            ]
        ),
    )
    angle_offsets.append(0.0)
    nsections = len(reacthts)
    circradii = circradii.reshape(nsections, 6)
    nvolumes = nsections - 1
    meshz = mesh_nz * np.diff(reacthts)
    meshz = meshz.astype(int) + 1  # avoid zero mesh elements

    # section to impeller mapping
    section2imp = -1 * np.ones(nsections, dtype=int)
    # index 0–3 -> impeller 0, 4–7 -> impeller 1, etc.
    for j, sec in enumerate(baff_sections):
        section2imp[sec] = j // 4

    all_volumes = range(nvolumes)
    nonbaff_volumes = [sec for sec in all_volumes if sec not in baff_volumes]
    nonstem_volumes = [0, 1]  # this is 0,1 no matter how many impellers are there

    # note: stem_volumes include hub volumes also
    # these are volumes where we miss out polygon block
    stem_volumes = [sec for sec in all_volumes if sec not in nonstem_volumes]

    # removes hub_volumes here for declaring patches
    only_stem_volumes = [sec for sec in stem_volumes if sec not in hub_volumes]

    # to define mrf region
    # not that [1] is not a stem volume but baffles are there
    mrf_volumes = [1] + stem_volumes

    # increase grid points in the impeller section
    for i in baff_volumes:
        meshz[i] *= 2

    avg_circradii = np.array(
        [
            np.mean(imp_scale) * (hub_diameter / 2 - inner_blade_length),
            np.mean(imp_scale) * hub_diameter / 2,
            np.mean(imp_scale) * impeller_tip_diameter / 2,
            mrf_region_diameter / 2,
            tank_diameter / 2 - baffle_width,
            tank_diameter / 2,
        ]
    )
    meshr = mesh_nr * np.diff(avg_circradii)

    # adding polygon to hub mesh resolution
    meshr = np.append(mesh_nr * polyrad, meshr)
    meshr = meshr.astype(int)
    meshr += 1  # to avoid being zero

    centeroffset = 1  # one point on the axis
    polyoffset = nsplits  # number of points on polygon
    npts_per_section = (
        centeroffset + polyoffset + ncirc * nsplits
    )  # center+polygon+circles

    # assemble into namespace
    geom = SimpleNamespace(
        tank_diameter=tank_diameter,
        impeller_tip_diameter=impeller_tip_diameter,
        reactor_height=reactor_height,
        nimpellers=nimpellers,
        nbaffles=nbaffles,
        n_fins_per_impeller=n_fins_per_impeller,
        hub_diameter=hub_diameter,
        blade_length=blade_length,
        inner_blade_length=inner_blade_length,
        baffle_width=baffle_width,
        hub_height_width=hub_height_width,
        polyrad=polyrad,
        mrf_region_diameter=mrf_region_diameter,
        mesh_nr=mesh_nr,
        mesh_nz=mesh_nz,
        n_poly=n_poly,
        n_azimuth=n_azimuth,
        nsplits=nsplits,
        dangle=dangle,
        curved_bottom_center=curved_bottom_center,
        curved_bottom_radius=curved_bottom_radius,
        circradii=circradii,
        ncirc=ncirc,
        hub_circ=hub_circ,
        inhub_circ=inhub_circ,
        rot_circ=rot_circ,
        mrf_circ=mrf_circ,
        tank_circ=tank_circ,
        reacthts=reacthts,
        baff_sections=baff_sections,
        baff_volumes=baff_volumes,
        hub_volumes=hub_volumes,
        angle_offsets=angle_offsets,
        nsections=nsections,
        nvolumes=nvolumes,
        meshz=meshz,
        meshr=meshr,
        section2imp=section2imp,
        nonbaff_volumes=nonbaff_volumes,
        nonstem_volumes=nonstem_volumes,
        stem_volumes=stem_volumes,
        only_stem_volumes=only_stem_volumes,
        mrf_volumes=mrf_volumes,
        npts_per_section=npts_per_section,
        centeroffset=centeroffset,
        polyoffset=polyoffset,
        round_bottom=round_bottom,
        reactor_bottom=reactor_bottom,
    )
    return geom


if __name__ == "__main__":
    geom = build_geom()
    for key, value in vars(geom).items():
        print(f"{key}: {value}")


