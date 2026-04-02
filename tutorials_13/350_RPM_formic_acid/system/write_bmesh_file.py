import argparse

import numpy as np

import reactor_geom_data as geom_module


def write_ofoam_preamble(outfile):

    outfile.write(
        "/*--------------------------------*- C++ -*----------------------------------*\\\n"
    )
    outfile.write(
        "| =========                 |                                                 |\n"
    )
    outfile.write(
        "| \\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox           |\n"
    )
    outfile.write(
        "|  \\    /   O peration     | Version:  5                                     |\n"
    )
    outfile.write(
        "|   \\  /    A nd           | Web:      www.OpenFOAM.org                      |\n"
    )
    outfile.write(
        "|    \\/     M anipulation  |                                                 |\n"
    )
    outfile.write(
        "\*---------------------------------------------------------------------------*/\n"
    )
    outfile.write("FoamFile\n")
    outfile.write("{\n")
    outfile.write("\tversion     2.0;\n")
    outfile.write("\tformat      ascii;\n")
    outfile.write("\tclass       dictionary;\n")
    outfile.write("\tobject      blockMeshDict;\n")
    outfile.write("}\n\n")
    outfile.write(
        "// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //\n\n"
    )
    outfile.write("convertToMeters 1.0;\n\n")
    outfile.write(
        "// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //\n\n"
    )


def write_vertices(outfile, geom):

    outfile.write(
        "\n// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //\n"
    )
    outfile.write("vertices\n(\n")
    counter = 0
    for repeat in range(2):

        outfile.write("\n//section " + str(0) + "\n")
        outfile.write("\n//center\n")
        if geom.round_bottom:
            z = geom.curved_bottom_center[2] - geom.curved_bottom_radius
        else:
            z = geom.reactor_bottom
        outfile.write(f"(0.0 0.0 {z}) // {counter}\n")
        counter = counter + 1

        # polygon section
        outfile.write("\n//polygon\n")
        for i in range(geom.nsplits):
            ang = i * geom.dangle
            azang = np.pi / 2 - np.arccos(geom.polyrad / geom.curved_bottom_radius)
            x = geom.polyrad * np.cos(ang)
            y = geom.polyrad * np.sin(ang)
            # outfile.write(
            #     "( "
            #     + str(x)
            #     + " "
            #     + str(y)
            #     + " "
            #     + str(
            #         geom.curved_bottom_center[2]
            #         - geom.curved_bottom_radius * np.cos(azang)
            #     )
            #     + " ) // "
            #     + str(counter)
            #     + "\n"
            # )
            if geom.round_bottom:
                z = geom.curved_bottom_center[2] - geom.curved_bottom_radius * np.cos(
                    azang
                )
            else:
                z = geom.reactor_bottom
            outfile.write(f"({x} {y} {z}) // {counter}\n")
            counter = counter + 1

            outfile.write("\n//circles\n")

        for ci in range(geom.ncirc):
            for i in range(geom.nsplits):
                ang = i * geom.dangle
                azang = np.pi / 2 - np.arccos(
                    geom.circradii[0][ci] / geom.curved_bottom_radius
                )
                x = geom.circradii[0][ci] * np.cos(ang)
                y = geom.circradii[0][ci] * np.sin(ang)
                # outfile.write(
                #     "( "
                #     + str(x)
                #     + " "
                #     + str(y)
                #     + " "
                #     + str(
                #         geom.curved_bottom_center[2]
                #         - geom.curved_bottom_radius * np.cos(azang)
                #     )
                #     + " ) //"
                #     + str(counter)
                #     + "\n"
                # )
                if geom.round_bottom:
                    z = geom.curved_bottom_center[
                        2
                    ] - geom.curved_bottom_radius * np.cos(azang)
                else:
                    z = geom.reactor_bottom
                outfile.write(f"({x} {y} {z}) // {counter}\n")
                counter = counter + 1

        for zi in range(1, geom.nsections):

            outfile.write("\n//section " + str(zi) + "\n")
            outfile.write("\n//center\n")
            outfile.write(
                "(0.0 0.0 " + str(geom.reacthts[zi]) + ") // " + str(counter) + "\n"
            )
            counter = counter + 1

            # polygon section
            outfile.write("\n//polygon\n")
            for i in range(geom.nsplits):
                ang = i * geom.dangle
                x = geom.polyrad * np.cos(ang)
                y = geom.polyrad * np.sin(ang)
                outfile.write(
                    "( "
                    + str(x)
                    + " "
                    + str(y)
                    + " "
                    + str(geom.reacthts[zi])
                    + " ) // "
                    + str(counter)
                    + "\n"
                )
                counter = counter + 1

            outfile.write("\n//circles\n")

            for ci in range(geom.ncirc):

                outfile.write("\n//circle " + str(ci) + "\n")
                offsetang = 0.0
                if ci >= 0 and ci <= 2:
                    offsetang = geom.angle_offsets[zi]

                for i in range(geom.nsplits):
                    ang = i * geom.dangle + offsetang
                    x = geom.circradii[zi][ci] * np.cos(ang)
                    y = geom.circradii[zi][ci] * np.sin(ang)
                    outfile.write(
                        "( "
                        + str(x)
                        + " "
                        + str(y)
                        + " "
                        + str(geom.reacthts[zi])
                        + " ) //"
                        + str(counter)
                        + "\n"
                    )
                    counter = counter + 1

    outfile.write(");\n")


def get_globalindex_of(geom, splti, ci, zi):

    # also works for ci=-1
    global_id = (
        zi * geom.npts_per_section
        + geom.centeroffset
        + geom.polyoffset
        + ci * geom.nsplits
        + splti % geom.nsplits
    )
    return global_id


def get_baffle_point_of(geom, splti, ci, zi):
    """
    Return the correct point index for (splti, ci, zi), including the extra
    ring used for impeller fins (hub_circ) and wall baffles (tank_circ).

    - nbaffles controls the number of baffles (on tank_circ).
    - n_fins_per_impeller[imp_idx] controls the fins for impeller set imp_idx.
    """

    baffle_id = get_globalindex_of(geom, splti, ci, zi)

    if zi not in geom.baff_sections:
        return baffle_id

    # half the splits – used as the “base” angular grid
    N = geom.nsplits // 2

    # ---------- impeller fins on the hub circle ----------
    if ci == geom.hub_circ:
        imp_idx = geom.section2imp[zi]  # from reactor_geom_data.py
        if imp_idx >= 0:
            n_fins = geom.n_fins_per_impeller[imp_idx]

            # we only allow fins on even splits: i = 2*j
            if splti % 2 == 0:
                j = (splti // 2) % N
                step_j = N // n_fins  # integer because n_fins | N
                if j % step_j == 0:
                    baffle_id += geom.nsections * geom.npts_per_section


    return baffle_id


def _is_duplicated_point(geom, splti: int, ci: int, zi: int) -> bool:
    """True if (splti, ci, zi) uses the duplicated "extra ring" point."""
    return get_baffle_point_of(geom, splti, ci, zi) != get_globalindex_of(
        geom, splti, ci, zi
    )


def write_edges(outfile, geom):

    outfile.write(
        "\n// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //\n"
    )
    outfile.write("edges\n(\n")
    outfile.write("\n//circles\n")

    outfile.write("\n//section " + str(0) + "\n")

    # polygon section
    outfile.write("\n//polygon\n")
    for i in range(geom.nsplits):
        ang = i * geom.dangle
        nextang = (i + 1) * geom.dangle
        midx = 0.5 * geom.polyrad * (np.cos(ang) + np.cos(nextang))
        midy = 0.5 * geom.polyrad * (np.sin(ang) + np.sin(nextang))
        azang = np.pi / 2 - np.arccos(
            np.sqrt(midx**2 + midy**2) / geom.curved_bottom_radius
        )
        outfile.write("arc " + str(i + 1) + " " + str((i + 1) % geom.nsplits + 1) + " ")
        # outfile.write(
        #     "( "
        #     + str(midx)
        #     + " "
        #     + str(midy)
        #     + " "
        #     + str(
        #         geom.curved_bottom_center[2] - geom.curved_bottom_radius * np.cos(azang)
        #     )
        #     + " )\n"
        # )
        if geom.round_bottom:
            z = geom.curved_bottom_center[2] - geom.curved_bottom_radius * np.cos(azang)
        else:
            z = geom.reactor_bottom
        outfile.write(f"({midx} {midy} {z})\n")

    for ci in range(geom.ncirc):
        outfile.write("\n//circle " + str(ci) + "\n")
        for i in range(geom.nsplits):
            ang = i * geom.dangle
            midx = geom.circradii[0][ci] * np.cos(ang + geom.dangle / 2)
            midy = geom.circradii[0][ci] * np.sin(ang + geom.dangle / 2)
            azang = np.pi / 2 - np.arccos(
                geom.circradii[0][ci] / geom.curved_bottom_radius
            )

            globalind1 = get_baffle_point_of(geom, i, ci, 0)
            globalind2 = get_globalindex_of(geom, i + 1, ci, 0)

            outfile.write("arc " + str(globalind1) + " " + str(globalind2) + " ")
            # outfile.write(
            #     "( "
            #     + str(midx)
            #     + " "
            #     + str(midy)
            #     + " "
            #     + str(
            #         geom.curved_bottom_center[2]
            #         - geom.curved_bottom_radius * np.cos(azang)
            #     )
            #     + " )\n"
            # )
            if geom.round_bottom:
                z = geom.curved_bottom_center[2] - geom.curved_bottom_radius * np.cos(
                    azang
                )
            else:
                z = geom.reactor_bottom
            outfile.write(f"({midx} {midy} {z})\n")

    for zi in range(1, geom.nsections):

        outfile.write("\n//section " + str(zi) + "\n")

        offset = 1 + geom.nsplits  # one for center and nsplits for polygon

        outfile.write("\n//circles\n")
        for ci in range(geom.ncirc):
            outfile.write("\n//circle " + str(ci) + "\n")
            for i in range(geom.nsplits):
                # add in offset angle to prevent degenerate issues when fins overlap
                offsetang = 0.0
                if 0 <= ci <= 2:
                    offsetang = geom.angle_offsets[zi]

                ang = i * geom.dangle + offsetang
                midx = geom.circradii[zi][ci] * np.cos(ang + geom.dangle / 2)
                midy = geom.circradii[zi][ci] * np.sin(ang + geom.dangle / 2)

                globalind1 = get_baffle_point_of(geom, i, ci, zi)
                globalind2 = get_globalindex_of(geom, i + 1, ci, zi)

                outfile.write("arc " + str(globalind1) + " " + str(globalind2) + " ")
                outfile.write(
                    "( "
                    + str(midx)
                    + " "
                    + str(midy)
                    + " "
                    + str(geom.reacthts[zi])
                    + " )\n"
                )

    outfile.write(");\n")


def write_this_block(outfile, comment, ids, mesh, zonename="none"):

    outfile.write("\n //" + comment + "\n")
    outfile.write("hex (")
    for i in range(len(ids)):
        outfile.write(str(ids[i]) + " ")
    outfile.write(")\n")

    if zonename != "none":
        outfile.write(zonename + "\n")

    outfile.write("( %d %d %d )\n" % (mesh[0], mesh[1], mesh[2]))
    outfile.write("SimpleGrading (1 1 1)\n")


def write_blocks(outfile, geom):

    outfile.write(
        "\n// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //\n"
    )
    outfile.write("blocks\n(\n")

    idarray = np.zeros(8, dtype=int)
    mesharray = np.zeros(3, dtype=int)

    for zi in range(geom.nvolumes):

        outfile.write("\n//section " + str(zi) + "-" + str(zi + 1) + "\n")

        offset0 = zi * geom.npts_per_section
        offset1 = (zi + 1) * geom.npts_per_section

        # polygon section
        center_id0 = offset0
        center_id1 = offset1

        # skip polygon blocks in stem sections
        if zi in geom.nonstem_volumes:
            for i in range(geom.nsplits):

                localind1 = geom.centeroffset + i % geom.nsplits
                localind2 = geom.centeroffset + (i + 1) % geom.nsplits

                idarray[0] = offset0 + localind1
                idarray[1] = offset1 + localind1
                idarray[2] = offset1 + localind2
                idarray[3] = offset0 + localind2
                idarray[4] = center_id0
                idarray[5] = center_id1
                idarray[6] = center_id1
                idarray[7] = center_id0

                mesharray[0] = geom.meshz[zi]
                mesharray[1] = geom.n_azimuth
                mesharray[2] = geom.n_poly

                zonename = "none"
                if zi in geom.mrf_volumes:
                    zonename = "rotor"

                write_this_block(
                    outfile, "block %d" % (i), idarray, mesharray, zonename
                )

        idarray[:] = 0
        mesharray[:] = 0
        outfile.write("\n//circles\n")

        for ci in range(geom.ncirc):

            zonename = "none"

            # skip blocks inside hub
            if ((ci == geom.inhub_circ) or (ci == geom.hub_circ)) and (
                zi in geom.hub_volumes
            ):
                continue

            outfile.write("\n//circle " + str(ci) + "\n")

            if (zi in geom.mrf_volumes) and (ci <= geom.mrf_circ):
                zonename = "rotor"

            for i in range(geom.nsplits):

                idarray[0] = get_baffle_point_of(geom, i, ci, zi)
                idarray[1] = get_baffle_point_of(geom, i, ci, zi + 1)
                idarray[2] = get_globalindex_of(geom, i + 1, ci, zi + 1)
                idarray[3] = get_globalindex_of(geom, i + 1, ci, zi)
                idarray[4] = get_baffle_point_of(geom, i, ci - 1, zi)
                idarray[5] = get_baffle_point_of(geom, i, ci - 1, zi + 1)
                idarray[6] = get_globalindex_of(geom, i + 1, ci - 1, zi + 1)
                idarray[7] = get_globalindex_of(geom, i + 1, ci - 1, zi)

                mesharray[0] = geom.meshz[zi]
                mesharray[1] = geom.n_azimuth
                mesharray[2] = geom.meshr[ci]
                write_this_block(
                    outfile, "block %d" % (i), idarray, mesharray, zonename
                )

    outfile.write(");\n")

    # print "meshz:",meshz
    # print "meshr:",meshr


def write_patches(outfile, geom):

    inhub_ci = geom.inhub_circ
    hub_ci = geom.hub_circ
    rot_ci = geom.rot_circ
    poly_ci = -1

    outfile.write(
        "\n// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //\n"
    )
    outfile.write("patches\n(\n")

    # outlet patch
    zi = geom.nsections - 1
    centerid = zi * geom.npts_per_section
    outfile.write("\n\tpatch outlet\n\t(\n")

    outfile.write("\n\t\t//circles\n")
    for ci in range(geom.ncirc):
        outfile.write("\n\t\t//circle " + str(ci) + " - " + str(ci - 1) + " \n")
        for i in range(geom.nsplits):
            outfile.write("\t\t( ")
            outfile.write(str(get_globalindex_of(geom, i, ci, zi)) + " ")
            outfile.write(str(get_globalindex_of(geom, i + 1, ci, zi)) + " ")
            outfile.write(str(get_globalindex_of(geom, i + 1, ci - 1, zi)) + " ")
            outfile.write(str(get_globalindex_of(geom, i, ci - 1, zi)) + ")\n")

    outfile.write("\t)\n")

    # propeller patch
    outfile.write("\n\twall propeller\n\t(\n")

    # need polygon patch at the first impeller
    zi = geom.hub_volumes[0]
    outfile.write("\n\t\t//polygon\n")
    centerid = zi * geom.npts_per_section
    # polygon
    for i in range(geom.nsplits):
        outfile.write("\t\t( ")
        outfile.write(str(get_globalindex_of(geom, i, poly_ci, zi)) + " ")
        outfile.write(str(get_globalindex_of(geom, i + 1, poly_ci, zi)) + " ")
        outfile.write(str(centerid) + " ")
        outfile.write(str(centerid) + ")\n")

    for n_imp in range(geom.nimpellers):
        zi_bottom = geom.hub_volumes[n_imp]  # bottom of impeller section
        zi_top = zi_bottom + 1  # bottom of impeller section

        for zi in [zi_bottom, zi_top]:

            outfile.write("\n\t\t//hub to blade circle\n")
            for i in range(geom.nsplits):
                outfile.write("\t\t( ")
                outfile.write(str(get_baffle_point_of(geom, i, hub_ci, zi)) + " ")
                outfile.write(str(get_globalindex_of(geom, i + 1, hub_ci, zi)) + " ")
                outfile.write(str(get_globalindex_of(geom, i + 1, inhub_ci, zi)) + " ")
                outfile.write(str(get_baffle_point_of(geom, i, inhub_ci, zi)) + ")\n")

            outfile.write("\n\t\t//blade to polygon\n")
            for i in range(geom.nsplits):
                outfile.write("\t\t( ")
                outfile.write(str(get_baffle_point_of(geom, i, inhub_ci, zi)) + " ")
                outfile.write(str(get_globalindex_of(geom, i + 1, inhub_ci, zi)) + " ")
                outfile.write(str(get_globalindex_of(geom, i + 1, poly_ci, zi)) + " ")
                outfile.write(str(get_baffle_point_of(geom, i, poly_ci, zi)) + ")\n")

        # sides
        outfile.write("\n\t\t//sides\n")
        for i in range(geom.nsplits):
            outfile.write("\t\t( ")
            outfile.write(str(get_baffle_point_of(geom, i, hub_ci, zi_bottom)) + " ")
            outfile.write(str(get_globalindex_of(geom, i + 1, hub_ci, zi_bottom)) + " ")
            outfile.write(str(get_globalindex_of(geom, i + 1, hub_ci, zi_top)) + " ")
            outfile.write(str(get_baffle_point_of(geom, i, hub_ci, zi_top)) + ")\n")

    # blades
    outfile.write("\n\t\t//blades\n")
    for zi in geom.baff_volumes:
        zi_bottom = zi
        zi_top = zi + 1

        for i in range(0, geom.nsplits, 2):  # even numbers: candidate fin planes
            # Only create blade faces where this split actually corresponds to a fin.
            # For non-fin splits, get_baffle_point_of == get_globalindex_of, so skip them.
            if get_baffle_point_of(geom, i, hub_ci, zi_bottom) == get_globalindex_of(
                geom, i, hub_ci, zi_bottom
            ):
                continue

            # outer blade surface (uses the extra "baffle" ring)
            outfile.write("\t\t( ")
            outfile.write(
                str(get_baffle_point_of(geom, i, hub_ci + 1, zi_bottom)) + " "
            )
            outfile.write(str(get_baffle_point_of(geom, i, hub_ci + 1, zi_top)) + " ")
            outfile.write(str(get_baffle_point_of(geom, i, hub_ci, zi_top)) + " ")
            outfile.write(str(get_baffle_point_of(geom, i, hub_ci, zi_bottom)) + ")\n")

            # matching inner surface on the original ring
            outfile.write("\t\t( ")
            outfile.write(str(get_globalindex_of(geom, i, hub_ci + 1, zi_bottom)) + " ")
            outfile.write(str(get_globalindex_of(geom, i, hub_ci + 1, zi_top)) + " ")
            outfile.write(str(get_globalindex_of(geom, i, hub_ci, zi_top)) + " ")
            outfile.write(str(get_globalindex_of(geom, i, hub_ci, zi_bottom)) + ")\n")

    # inside hub blades
    for n_imp in range(geom.nimpellers):
        hub_vol = geom.hub_volumes[n_imp]
        zi_pairs = [[hub_vol - 1, hub_vol], [hub_vol + 1, hub_vol + 2]]

        for zi_pair in zi_pairs:

            zi_below = zi_pair[0]
            zi_above = zi_pair[1]

            for i in range(0, geom.nsplits, 2):  # even numbers: candidate fin planes
                # Only create faces where this split actually corresponds to a fin.
                # For non-fin splits, get_baffle_point_of == get_globalindex_of, so skip.
                if get_baffle_point_of(geom, i, hub_ci, zi_below) == get_globalindex_of(
                    geom, i, hub_ci, zi_below
                ):
                    continue

                outfile.write("\t\t( ")
                outfile.write(str(get_baffle_point_of(geom, i, hub_ci, zi_below)) + " ")
                outfile.write(
                    str(get_baffle_point_of(geom, i, inhub_ci, zi_below)) + " "
                )
                outfile.write(
                    str(get_baffle_point_of(geom, i, inhub_ci, zi_above)) + " "
                )
                outfile.write(
                    str(get_baffle_point_of(geom, i, hub_ci, zi_above)) + ")\n"
                )

                outfile.write("\t\t( ")
                outfile.write(str(get_globalindex_of(geom, i, hub_ci, zi_below)) + " ")
                outfile.write(
                    str(get_globalindex_of(geom, i, inhub_ci, zi_below)) + " "
                )
                outfile.write(
                    str(get_globalindex_of(geom, i, inhub_ci, zi_above)) + " "
                )
                outfile.write(
                    str(get_globalindex_of(geom, i, hub_ci, zi_above)) + ")\n"
                )

    # stem
    outfile.write("\n\t\t//stem sides\n")
    for zi in geom.only_stem_volumes:
        zi_bottom = zi
        zi_top = zi + 1
        for i in range(geom.nsplits):
            outfile.write("\t\t( ")
            outfile.write(str(get_globalindex_of(geom, i, poly_ci, zi_bottom)) + " ")
            outfile.write(
                str(get_globalindex_of(geom, i + 1, poly_ci, zi_bottom)) + " "
            )
            outfile.write(str(get_globalindex_of(geom, i + 1, poly_ci, zi_top)) + " ")
            outfile.write(str(get_globalindex_of(geom, i, poly_ci, zi_top)) + ")\n")

    outfile.write("\t)\n")

    # stator and walls patch
    tank_ci = geom.ncirc - 1
    outfile.write("\n\twall walls\n\t(\n")

    # inlet patch
    zi = 0
    centerid = zi * geom.npts_per_section
    # polygon
    outfile.write("\n\t\t//polygon\n")
    for i in range(geom.nsplits):
        outfile.write("\t\t( ")
        outfile.write(str(get_globalindex_of(geom, i, poly_ci, zi)) + " ")
        outfile.write(str(get_globalindex_of(geom, i + 1, poly_ci, zi)) + " ")
        outfile.write(str(centerid) + " ")
        outfile.write(str(centerid) + ")\n")

    outfile.write("\n\t\t//inhub_circ to polygon\n")
    for i in range(geom.nsplits):
        outfile.write("\t\t( ")
        outfile.write(str(get_globalindex_of(geom, i, inhub_ci, zi)) + " ")
        outfile.write(str(get_globalindex_of(geom, i + 1, inhub_ci, zi)) + " ")
        outfile.write(str(get_globalindex_of(geom, i + 1, poly_ci, zi)) + " ")
        outfile.write(str(get_globalindex_of(geom, i, poly_ci, zi)) + ")\n")

    outfile.write("\n\t\t//hub to inhub_circ\n")
    for i in range(geom.nsplits):
        outfile.write("\t\t( ")
        outfile.write(str(get_globalindex_of(geom, i, hub_ci, zi)) + " ")
        outfile.write(str(get_globalindex_of(geom, i + 1, hub_ci, zi)) + " ")
        outfile.write(str(get_globalindex_of(geom, i + 1, inhub_ci, zi)) + " ")
        outfile.write(str(get_globalindex_of(geom, i, inhub_ci, zi)) + ")\n")

    outfile.write("\n\t\t//rotor to hub\n")
    for i in range(geom.nsplits):
        outfile.write("\t\t( ")
        outfile.write(str(get_globalindex_of(geom, i, rot_ci, zi)) + " ")
        outfile.write(str(get_globalindex_of(geom, i + 1, rot_ci, zi)) + " ")
        outfile.write(str(get_globalindex_of(geom, i + 1, hub_ci, zi)) + " ")
        outfile.write(str(get_globalindex_of(geom, i, hub_ci, zi)) + ")\n")

    for zi in range(geom.nsections - 1):
        outfile.write("\n\t\t//tank walls " + str(zi) + " - " + str(zi + 1) + "\n")

        for i in range(geom.nsplits):
            outfile.write("\t\t( ")
            outfile.write(str(get_baffle_point_of(geom, i, tank_ci, zi)) + " ")
            outfile.write(str(get_globalindex_of(geom, i + 1, tank_ci, zi)) + " ")
            outfile.write(str(get_globalindex_of(geom, i + 1, tank_ci, zi + 1)) + " ")
            outfile.write(str(get_baffle_point_of(geom, i, tank_ci, zi + 1)) + ")\n")



    # inlet wall patch
    # skip rotor to hub to inhub_circ to polygon region
    # which is covered in inflow
    zi = 0
    outfile.write("\n\t\t//circles\n")
    for ci in range(rot_ci + 1, geom.ncirc):  # start from rotor circle
        outfile.write("\n\t\t//circle " + str(ci) + " - " + str(ci - 1) + " \n")
        for i in range(geom.nsplits):
            outfile.write("\t\t( ")
            outfile.write(str(get_globalindex_of(geom, i, ci, zi)) + " ")
            outfile.write(str(get_globalindex_of(geom, i + 1, ci, zi)) + " ")
            outfile.write(str(get_globalindex_of(geom, i + 1, ci - 1, zi)) + " ")
            outfile.write(str(get_globalindex_of(geom, i, ci - 1, zi)) + ")\n")

    outfile.write("\t)\n")

    # stitch faces patches
    outfile.write("\n\tempty inside_to_hub\n\t(\n")

    zi_pairs = []
    for vols in geom.nonbaff_volumes:
        zi_pairs.append([vols, vols + 1])

    for zi_pair in zi_pairs:

        zi_below = zi_pair[0]
        zi_above = zi_pair[1]
        outfile.write("\n\t\t//pair :" + str(zi_below) + "-" + str(zi_above) + "\n")

        for i in range(0, geom.nsplits, 2):  # even numbers
            # skip the even splits that are not duplicated
            if not (
                _is_duplicated_point(geom, i, hub_ci, zi_below)
                or _is_duplicated_point(geom, i, hub_ci, zi_above)
            ):
                continue
            outfile.write("\t\t( ")
            outfile.write(str(get_baffle_point_of(geom, i, hub_ci, zi_below)) + " ")
            outfile.write(str(get_baffle_point_of(geom, i, inhub_ci, zi_below)) + " ")
            outfile.write(str(get_baffle_point_of(geom, i, inhub_ci, zi_above)) + " ")
            outfile.write(str(get_baffle_point_of(geom, i, hub_ci, zi_above)) + ")\n")

    outfile.write("\t)\n")

    outfile.write("\n\tempty inside_to_hub_copy\n\t(\n")

    for zi_pair in zi_pairs:

        zi_below = zi_pair[0]
        zi_above = zi_pair[1]
        outfile.write("\n\t\t//pair :" + str(zi_below) + "-" + str(zi_above) + "\n")

        for i in range(0, geom.nsplits, 2):  # even numbers
            if not (
                _is_duplicated_point(geom, i, hub_ci, zi_below)
                or _is_duplicated_point(geom, i, hub_ci, zi_above)
            ):
                continue
            outfile.write("\t\t( ")
            outfile.write(str(get_globalindex_of(geom, i, hub_ci, zi_below)) + " ")
            outfile.write(str(get_globalindex_of(geom, i, inhub_ci, zi_below)) + " ")
            outfile.write(str(get_globalindex_of(geom, i, inhub_ci, zi_above)) + " ")
            outfile.write(str(get_globalindex_of(geom, i, hub_ci, zi_above)) + ")\n")

    outfile.write("\t)\n")

    # stitch faces patches
    outfile.write("\n\tempty hub_to_rotor\n\t(\n")

    for zi_pair in zi_pairs:

        zi_below = zi_pair[0]
        zi_above = zi_pair[1]
        outfile.write("\n\t\t//pair :" + str(zi_below) + "-" + str(zi_above) + "\n")

        for i in range(0, geom.nsplits, 2):  # even numbers
            if not (
                _is_duplicated_point(geom, i, hub_ci, zi_below)
                or _is_duplicated_point(geom, i, hub_ci, zi_above)
            ):
                continue
            outfile.write("\t\t( ")
            outfile.write(str(get_baffle_point_of(geom, i, rot_ci, zi_below)) + " ")
            outfile.write(str(get_baffle_point_of(geom, i, hub_ci, zi_below)) + " ")
            outfile.write(str(get_baffle_point_of(geom, i, hub_ci, zi_above)) + " ")
            outfile.write(str(get_baffle_point_of(geom, i, rot_ci, zi_above)) + ")\n")

    outfile.write("\t)\n")
    outfile.write("\n\tempty hub_to_rotor_copy\n\t(\n")

    for zi_pair in zi_pairs:

        zi_below = zi_pair[0]
        zi_above = zi_pair[1]
        outfile.write("\n\t\t//pair :" + str(zi_below) + "-" + str(zi_above) + "\n")

        for i in range(0, geom.nsplits, 2):  # even numbers
            if not (
                _is_duplicated_point(geom, i, hub_ci, zi_below)
                or _is_duplicated_point(geom, i, hub_ci, zi_above)
            ):
                continue

            outfile.write("\t\t( ")
            outfile.write(str(get_globalindex_of(geom, i, rot_ci, zi_below)) + " ")
            outfile.write(str(get_globalindex_of(geom, i, hub_ci, zi_below)) + " ")
            outfile.write(str(get_globalindex_of(geom, i, hub_ci, zi_above)) + " ")
            outfile.write(str(get_globalindex_of(geom, i, rot_ci, zi_above)) + ")\n")

    outfile.write("\t)\n")

    outfile.write(");\n")


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--n_fins", nargs="+", type=int, help="Number of fins for each impeller"
    )
    parser.add_argument(
        "--blade_pitch",
        nargs="+",
        type=float,
        help="Blade pitch angle for each impeller",
    )
    parser.add_argument(
        "--length_factor",
        default=None,
        help="Blade length factor (1 / factor)",
    )
    parser.add_argument(
        "--width_factor",
        default=None,
        help="Blade width factor (1 / factor)",
    )
    parser.add_argument(
        "--imp_scale",
        nargs="+",
        type=float,
        help="Impeller scale to adjust the size of each impeller set",
    )
    parser.add_argument(
        "--imp_centers",
        nargs="+",
        type=float,
        help="Impeller centers list",
    )
    parser.add_argument(
        "--aspect_ratio",
        type=float,
        default=1.63,
        help="Aspect ratio of the cylinder reactor tank.",
    )
    parser.add_argument(
        "--tank_volume",
        type=float,
        default=1500,
        help="Volume of the reactor tank in Liters.",
    )
    parser.add_argument(
        "--round_bottom",
        action="store_true",
        help="Flag to enable a rounded bottom reactor.",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    n_fins = args.n_fins if args.n_fins is not None else None
    blade_pitch = args.blade_pitch if args.blade_pitch is not None else None
    blade_length_factor = args.length_factor if args.length_factor is not None else None
    blade_width_factor = args.width_factor if args.width_factor is not None else None
    imp_scale = args.imp_scale if args.imp_scale is not None else None
    imp_centers = args.imp_centers if args.imp_centers is not None else None
    aspect_ratio = args.aspect_ratio if args.aspect_ratio is not None else None
    tank_volume = args.tank_volume if args.tank_volume is not None else None

    # initialize geometry data
    geom = geom_module.build_geom(
        n_fins_per_impeller=n_fins,
        blade_pitch=blade_pitch,
        blade_length_factor=blade_length_factor,
        blade_width_factor=blade_width_factor,
        imp_scale=imp_scale,
        imp_centers=imp_centers,
        round_bottom=args.round_bottom,
        aspect_ratio=aspect_ratio,
        target_volume_L=tank_volume,
    )

    outfile = open("blockMeshDict_reactor", "w")
    write_ofoam_preamble(outfile)
    write_vertices(outfile, geom)
    write_edges(outfile, geom)
    write_blocks(outfile, geom)
    write_patches(outfile, geom)
    outfile.close()


if __name__ == "__main__":
    main()
