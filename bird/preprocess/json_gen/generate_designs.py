import os
import pickle
import shutil
from pathlib import Path

import numpy as np

from bird import BIRD_CASE_DIR, BIRD_DIR, logger
from bird.meshing.block_rect_mesh import from_block_rect_to_seg
from bird.preprocess.dynamic_mixer.mixer import (
    ActuatorMixer,
    actuator_disk_power,
)
from bird.preprocess.json_gen.design_io import *


def id2simfolder(sim_id: int) -> str:
    """
    Generates simulation folder name from simulation index

    Parameters
    ----------
    sim_id: int
        Simulation index

    Returns
    ----------
    sim_folder : str
        Simulation folder name
    """
    sim_folder = f"Sim_{sim_id:04}"
    return sim_folder


def compare_config(config1, config2):
    same = True
    for key in config1:
        if np.linalg.norm(config1[key] - config2[key]) > 1e-6:
            same = False
            return same
    return same


def check_config(config):
    success = False
    inlet_exist = False
    for key in config:
        if len(np.argwhere(config[key] == 1)) > 0:
            inlet_exist = True
            break
    if inlet_exist:
        success = True
    else:
        success = False
    return success


def save_config_dict(filename, config_dict):
    with open(filename, "wb") as f:
        pickle.dump(config_dict, f)


def load_config_dict(filename):
    with open(filename, "rb") as f:
        config_dict = pickle.load(f)
    return config_dict


def write_script_start(filename, n):
    with open(filename, "w+") as f:
        for i in range(n):
            sim_folder = id2simfolder(i)
            f.write(f"cd {sim_folder}\n")
            f.write(f"sbatch script\n")
            f.write(f"cd ..\n")


def write_script_post(filename, n):
    with open(filename, "w+") as f:
        for i in range(n):
            sim_folder = id2simfolder(i)
            f.write(f"cd {sim_folder}\n")
            f.write(f"sbatch script_post\n")
            f.write(f"cd ..\n")


def write_prep(filename, n):
    with open(filename, "w+") as f:
        f.write("prep () {\n")
        f.write(f"\tcd $1\n")
        f.write(f"\treconstructPar -newTimes\n")
        f.write(f"\tcd ..\n")
        f.write("}\n")
        f.write(f"\n")
        f.write(
            f"source /projects/gas2fuels/ofoam_cray_mpich/OpenFOAM-dev/etc/bashrc\n"
        )
        for i in range(n):
            sim_folder = id2simfolder(i)
            f.write(f"prep {sim_folder}\n")


def overwrite_vvm(case_folder, vvm):
    list_dir = os.listdir(case_folder)
    if not "constant" in list_dir:
        error_msg = f"{case_folder} is likely not a case folder, could not find constant/"
        logger.error(error_msg)
        raise FileNotFoundError(error_msg)
    else:
        filename = os.path.join(case_folder, "constant", "globalVars_temp")
        filename_write = os.path.join(
            case_folder, "constant", "globalVars_temp2"
        )
        with open(filename, "r+") as f:
            lines = f.readlines()
        with open(filename_write, "w+") as f:
            for line in lines:
                if line.startswith("VVM"):
                    f.write(f"VVM\t{vvm};\n")
                else:
                    f.write(line)
        shutil.copy(
            os.path.join(case_folder, "constant", "globalVars_temp2"),
            os.path.join(case_folder, "constant", "globalVars_temp"),
        )
        os.remove(os.path.join(case_folder, "constant", "globalVars_temp2"))


def overwrite_bubble_size_model(case_folder, constantD=False):
    list_dir = os.listdir(case_folder)
    if not "constant" in list_dir:
        error_msg = f"{case_folder} is likely not a case folder, could not find constant/"
        logger.error(error_msg)
        raise FileNotFoundError(error_msg)
    else:
        filename = os.path.join(case_folder, "presteps.sh")
        filename_write = os.path.join(case_folder, "presteps2.sh")
        with open(filename, "r+") as f:
            lines = f.readlines()
        with open(filename_write, "w+") as f:
            for line in lines:
                if line.startswith("cp constant/phaseProperties"):
                    if constantD:
                        f.write(
                            "cp constant/phaseProperties_constantd constant/phaseProperties\n"
                        )
                    else:
                        f.write(
                            "cp constant/phaseProperties_pbe constant/phaseProperties\n"
                        )
                else:
                    f.write(line)
        shutil.copy(
            os.path.join(case_folder, "presteps2.sh"),
            os.path.join(case_folder, "presteps.sh"),
        )
        os.remove(os.path.join(case_folder, "presteps2.sh"))


def generate_small_reactor_cases(
    config_dict,
    branchcom_spots,
    vvm,
    power,
    constantD,
    study_folder,
    template_folder="loop_reactor_pbe_dynmix_nonstat_headbranch",
):
    if not os.path.isabs(template_folder):

        template_folder = os.path.join(
            f"{BIRD_CASE_DIR}", f"{template_folder}"
        )

    geom_dict = make_default_geom_dict_from_file(
        os.path.join(f"{template_folder}", "system", "mesh.json"),
        rescale=0.05,
    )
    try:
        shutil.rmtree(study_folder)
    except:
        pass
    Path(study_folder).mkdir(parents=True, exist_ok=True)
    for sim_id in config_dict:
        sim_folder = id2simfolder(sim_id)
        shutil.copytree(
            f"{template_folder}",
            os.path.join(f"{study_folder}", sim_folder),
        )
        bc_dict = {}
        bc_dict["inlets"] = []
        bc_dict["outlets"] = []
        bc_dict["outlets"].append(
            {
                "branch_id": 6,
                "type": "circle",
                "frac_space": 1,
                "normal_dir": 1,
                "radius": 0.4,
                "nelements": 50,
                "block_pos": "top",
            }
        )
        bc_dict["outlets"].append(
            {
                "branch_id": 4,
                "type": "circle",
                "frac_space": 1,
                "normal_dir": 1,
                "radius": 0.4,
                "nelements": 50,
                "block_pos": "top",
            }
        )
        for branch in config_dict:
            if branch in [0, 1, 2]:
                ind = np.argwhere(config_dict[sim_id][branch] == 1)
                if len(ind) > 0:
                    ind = list(ind[:, 0])
                    for iind in ind:
                        bc_dict["inlets"].append(
                            {
                                "branch_id": branch,
                                "type": "circle",
                                "frac_space": branchcom_spots[branch][iind],
                                "normal_dir": 1,
                                "radius": 0.4,
                                "nelements": 50,
                                "block_pos": "bottom",
                            }
                        )
        generate_stl_patch(
            os.path.join(
                study_folder, sim_folder, "system", "inlets_outlets.json"
            ),
            bc_dict,
            geom_dict,
        )

        mix_list = []
        for branch in config_dict:
            if branch in [0, 1, 2]:
                ind = np.argwhere(config_dict[sim_id][branch] == 0)
                if len(ind) > 0:
                    ind = list(ind[:, 0])
                    for iind in ind:
                        if branch == 0:
                            sign = "+"
                        else:
                            sign = "-"
                        mix_list.append(
                            {
                                "branch_id": branch,
                                "frac_space": branchcom_spots[branch][iind],
                                "start_time": 1,
                                "power": power,
                                "sign": sign,
                            }
                        )
        generate_dynamic_mixer(
            os.path.join(study_folder, sim_folder, "system", "mixers.json"),
            mix_list,
            geom_dict,
        )
        overwrite_vvm(
            case_folder=os.path.join(study_folder, sim_folder), vvm=vvm
        )
        overwrite_bubble_size_model(
            case_folder=os.path.join(study_folder, sim_folder),
            constantD=constantD,
        )

    geom_dict = make_default_geom_dict_from_file(
        os.path.join(f"{template_folder}", "system", "mesh.json"),
        rescale=0.05,
    )


def generate_scaledup_reactor_cases(
    config_dict,
    branchcom_spots,
    vvm,
    power,
    constantD,
    study_folder,
    template_folder="loop_reactor_pbe_dynmix_nonstat_headbranch_scaleup",
):

    if not os.path.isabs(template_folder):
        template_folder = os.path.join(
            f"{BIRD_CASE_DIR}", f"{template_folder}"
        )

    geom_dict = make_default_geom_dict_from_file(
        os.path.join(f"{template_folder}", "system", "mesh.json")
    )
    try:
        shutil.rmtree(study_folder)
    except:
        pass
    Path(study_folder).mkdir(parents=True, exist_ok=True)
    for sim_id in config_dict:
        sim_folder = id2simfolder(sim_id)
        shutil.copytree(
            f"{template_folder}",
            os.path.join(f"{study_folder}", sim_folder),
        )
        bc_dict = {}
        bc_dict["inlets"] = []
        bc_dict["outlets"] = []
        bc_dict["outlets"].append(
            {
                "branch_id": 6,
                "type": "circle",
                "frac_space": 1,
                "normal_dir": 1,
                "radius": 0.4,
                "nelements": 50,
                "block_pos": "top",
            }
        )
        bc_dict["outlets"].append(
            {
                "branch_id": 4,
                "type": "circle",
                "frac_space": 1,
                "normal_dir": 1,
                "radius": 0.4,
                "nelements": 50,
                "block_pos": "top",
            }
        )
        for branch in config_dict:
            if branch in [0, 1, 2]:
                ind = np.argwhere(config_dict[sim_id][branch] == 1)
                if len(ind) > 0:
                    ind = list(ind[:, 0])
                    for iind in ind:
                        bc_dict["inlets"].append(
                            {
                                "branch_id": branch,
                                "type": "circle",
                                "frac_space": branchcom_spots[branch][iind],
                                "normal_dir": 1,
                                "radius": 0.4,
                                "nelements": 50,
                                "block_pos": "bottom",
                            }
                        )
        generate_stl_patch(
            os.path.join(
                study_folder, sim_folder, "system", "inlets_outlets.json"
            ),
            bc_dict,
            geom_dict,
        )

        mix_list = []
        for branch in config_dict:
            if branch in [0, 1, 2]:
                ind = np.argwhere(config_dict[sim_id][branch] == 0)
                if len(ind) > 0:
                    ind = list(ind[:, 0])
                    for iind in ind:
                        if branch == 0:
                            sign = "+"
                        else:
                            sign = "-"
                        mix_list.append(
                            {
                                "branch_id": branch,
                                "frac_space": branchcom_spots[branch][iind],
                                "start_time": 3,
                                "power": power,
                                "sign": sign,
                            }
                        )
        generate_dynamic_mixer(
            os.path.join(study_folder, sim_folder, "system", "mixers.json"),
            mix_list,
            geom_dict,
        )
        overwrite_vvm(
            case_folder=os.path.join(study_folder, sim_folder), vvm=vvm
        )
        overwrite_bubble_size_model(
            case_folder=os.path.join(study_folder, sim_folder),
            constantD=constantD,
        )


def check_sparger_config(
    sparger_locs: list[float],
    n_spargers: int | None,
    sparger_spacing: float,
    edge_spacing: float,
    n_branches: int,
    bypass_sparger_spacing: bool,
) -> None:
    """
    Check realizability of the sparger placement configuration

    Parameters
    ----------
    sparger_locs : list[float]
        Location of every sparger along the loop reactor coordinate [-]
        There are 3 branches. Spargers can be placed anywhere
        between edge_spacing and (1-edge_spacing) fractions of the branch
        Each sparger locations must be between 0 and 3*1=3
    n_spargers : int|None
        Number of spargers
    sparger_spacing : float
        Spacing between two spargers [-]
    edge_spacing : float
        Spacing required between any sparger and the edges of the branches [-]
    n_branches : int
        Number of loop reactor branches
    bypass_sparger_spacing: bool
        If true, allow an overlap of spargers
    """

    # Check that number of spargers is consistent
    if n_spargers is None:
        n_spargers = len(sparger_locs)
    else:
        assert n_spargers == len(sparger_locs)
    assert n_spargers >= 1

    # Basis check on the number of branches
    assert n_branches > 0

    # Check that locations of spargers is consistent
    # There are n_branches branches. Spargers can be placed anywhere
    # between edge_spacing and (1-edge_spacing) fractions of the branch
    # Each sparger locations must be between 0 and n_branches*1=n_branches
    assert edge_spacing > 0
    assert edge_spacing < 1
    assert all(np.array(sparger_locs) >= 0)
    assert all(np.array(sparger_locs) <= float(n_branches))
    for ibranch in range(n_branches):
        if ibranch == 0:
            assert not np.any(np.array(sparger_locs) < edge_spacing)
        if ibranch == n_branches - 1:
            assert not np.any(
                np.array(sparger_locs) > float(n_branches) - edge_spacing
            )
        assert not np.any(
            (np.array(sparger_locs) > float(ibranch) + 1.0 - edge_spacing)
            & (np.array(sparger_locs) < float(ibranch) + 1.0 + edge_spacing)
        )

    # Check that spargers are sufficiently spaced out
    assert sparger_spacing >= 0
    if not bypass_sparger_spacing:
        assert all(np.diff(np.sort(np.array(sparger_locs))) >= sparger_spacing)


def generate_single_scaledup_reactor_sparger_cases(
    sparger_locs: list[float],
    n_spargers: int | None = None,
    sparger_spacing: float = 0.15,
    edge_spacing: float = 0.2,
    n_branches: int = 3,
    sim_id: int = 0,
    constantD: bool = True,
    vvm: float = 0.4,
    study_folder: str = ".",
    template_folder: str = "loop_reactor_pbe_dynmix_nonstat_headbranch_scaleup",
    bypass_sparger_spacing: bool = False,
):
    """
    Generates loop reactor case with desired sparger placement configuration

    Parameters
    ----------
    sparger_locs : list[float]
        Location of every sparger along the loop reactor coordinate [-]
    n_spargers : int|None
        Number of spargers
    sparger_spacing : float
        Spacing between two spargers [-]
    edge_spacing : float
        Spacing required between any sparger and the edges of the branches [-]
    n_branches : int
        Number of loop reactor branches
    sim_id : int
        Index identifier of the simulation
    constantD : bool
        If true, use constant bubble diameter
        If false, use population balance
    vvm : float
        VVM value [-]
    study_folder : str
        Where to generate the case
    template_folder: str
        The case template to start from
    bypass_sparger_spacing: bool
        If true, allow an overlap of spargers
    """

    # Sanity checks
    check_sparger_config(
        sparger_locs=sparger_locs,
        n_spargers=n_spargers,
        sparger_spacing=sparger_spacing,
        edge_spacing=edge_spacing,
        n_branches=n_branches,
        bypass_sparger_spacing=bypass_sparger_spacing,
    )

    # Find on which branch is each sparger
    branch_id = [int(entry) for entry in sparger_locs]

    # Case generation
    if not os.path.isabs(template_folder):

        template_folder = os.path.join(
            f"{BIRD_CASE_DIR}", f"{template_folder}"
        )
    geom_dict = make_default_geom_dict_from_file(
        os.path.join(f"{template_folder}", "system", "mesh.json")
    )

    # Start from template
    sim_folder = id2simfolder(sim_id)
    shutil.copytree(
        f"{template_folder}",
        os.path.join(f"{study_folder}", sim_folder),
    )

    bc_dict = {}
    bc_dict["inlets"] = []
    bc_dict["outlets"] = []
    bc_dict["outlets"].append(
        {
            "branch_id": 6,
            "type": "circle",
            "frac_space": 1,
            "normal_dir": 1,
            "radius": 0.4,
            "nelements": 50,
            "block_pos": "top",
        }
    )
    bc_dict["outlets"].append(
        {
            "branch_id": 4,
            "type": "circle",
            "frac_space": 1,
            "normal_dir": 1,
            "radius": 0.4,
            "nelements": 50,
            "block_pos": "top",
        }
    )

    for branch, loc in zip(branch_id, sparger_locs):
        bc_dict["inlets"].append(
            {
                "branch_id": branch,
                "type": "circle",
                "frac_space": loc - branch,
                "normal_dir": 1,
                "radius": 0.4,
                "nelements": 50,
                "block_pos": "bottom",
            }
        )

    generate_stl_patch(
        os.path.join(
            study_folder, sim_folder, "system", "inlets_outlets.json"
        ),
        bc_dict,
        geom_dict,
    )

    mix_list = []
    generate_dynamic_mixer(
        os.path.join(study_folder, sim_folder, "system", "mixers.json"),
        mix_list,
        geom_dict,
    )
    overwrite_vvm(case_folder=os.path.join(study_folder, sim_folder), vvm=vvm)
    overwrite_bubble_size_model(
        case_folder=os.path.join(study_folder, sim_folder),
        constantD=constantD,
    )


def overwrite_scale(case_folder, scale):
    """Rewrite the ``transformPoints`` scale in presteps.sh to `scale`."""
    filename = os.path.join(case_folder, "presteps.sh")
    with open(filename, "r+") as f:
        lines = f.readlines()
    with open(filename, "w+") as f:
        for line in lines:
            if line.strip().startswith("transformPoints"):
                f.write(f'transformPoints "scale=({scale} {scale} {scale})"\n')
            else:
                f.write(line)


def overwrite_ncores(case_folder, n):
    """Rewrite ``numberOfSubdomains`` in system/decomposeParDict to `n`."""
    filename = os.path.join(case_folder, "system", "decomposeParDict")
    with open(filename, "r+") as f:
        lines = f.readlines()
    with open(filename, "w+") as f:
        for line in lines:
            if line.strip().startswith("numberOfSubdomains"):
                f.write(f"numberOfSubdomains {n};\n")
            else:
                f.write(line)


def write_script_single(
    case_folder,
    account="gas2fuels",
    cores=4,
    solver="birdmultiphaseEulerFoam",
):
    """Write a per-case SLURM script (``script_single``) running one case."""
    ofbashrc = "/projects/gas2fuels/ofoam_cray_mpich/OpenFOAM-dev/etc/bashrc"
    with open(os.path.join(case_folder, "script_single"), "w+") as f:
        f.write("#!/bin/bash\n")
        f.write("#SBATCH --job-name=lev_single\n")
        f.write("#SBATCH --nodes=1\n")
        f.write(f"#SBATCH --ntasks-per-node={cores}\n")
        f.write("#SBATCH --time=07:59:00\n")
        f.write(f"#SBATCH --account={account}\n\n")
        f.write("bash presteps.sh\n")
        f.write(f"source {ofbashrc}\n")
        f.write("decomposePar -fileHandler collated\n")
        f.write(f"srun -n {cores} {solver} -parallel -fileHandler collated\n")
        f.write("reconstructPar -newTimes\n")


def write_script_post_single(case_folder, account="gas2fuels"):
    """Write a per-case post-processing SLURM script (``script_post_single``)."""
    with open(os.path.join(case_folder, "script_post_single"), "w+") as f:
        f.write("#!/bin/bash\n")
        f.write("#SBATCH --job-name=lev_post\n")
        f.write("#SBATCH --nodes=1\n")
        f.write("#SBATCH --ntasks-per-node=1\n")
        f.write("#SBATCH --time=00:59:00\n")
        f.write(f"#SBATCH --account={account}\n\n")
        f.write("bash computeQOI.sh\n")


def write_pack_scripts(
    study_folder,
    sim_ids,
    sims_per_node=26,
    cores_per_sim=4,
    account="gas2fuels",
    solver="birdmultiphaseEulerFoam",
):
    """Write node-packing scripts (Option A): pack_XXX bundles + submit_all.sh.

    Each bundle runs up to `sims_per_node` cases concurrently on one node, each
    via ``srun --exclusive -n cores_per_sim`` (so `sims_per_node*cores_per_sim`
    cores are used per node).
    """
    ofbashrc = "/projects/gas2fuels/ofoam_cray_mpich/OpenFOAM-dev/etc/bashrc"
    bundles = [
        sim_ids[i : i + sims_per_node]
        for i in range(0, len(sim_ids), sims_per_node)
    ]
    pack_names = []
    for b, bundle in enumerate(bundles):
        pack_name = f"pack_{b:03}"
        pack_names.append(pack_name)
        with open(os.path.join(study_folder, pack_name), "w+") as f:
            f.write("#!/bin/bash\n")
            f.write(f"#SBATCH --job-name=lev_{pack_name}\n")
            f.write("#SBATCH --nodes=1\n")
            f.write("#SBATCH --exclusive\n")
            f.write("#SBATCH --time=07:59:00\n")
            f.write(f"#SBATCH --account={account}\n\n")
            f.write(f"source {ofbashrc}\n\n")
            f.write("run_sim () {\n")
            f.write('\tcd "$1"\n')
            f.write("\tbash presteps.sh > log.presteps 2>&1\n")
            f.write(
                "\tdecomposePar -fileHandler collated > log.decompose 2>&1\n"
            )
            f.write(
                f"\tsrun --exclusive -n {cores_per_sim} {solver} -parallel"
                " -fileHandler collated > log.solve 2>&1\n"
            )
            f.write("\treconstructPar -newTimes > log.reconstruct 2>&1\n")
            f.write("\tcd ..\n")
            f.write("}\n\n")
            for sim_id in bundle:
                f.write(f"run_sim {id2simfolder(sim_id)} &\n")
            f.write("wait\n")
    with open(os.path.join(study_folder, "submit_all.sh"), "w+") as f:
        for pack_name in pack_names:
            f.write(f"sbatch {pack_name}\n")


def generate_leveled_reactor_cases(
    config_dict,
    branchcom_spots,
    scale,
    n_sim,
    study_folder,
    mixer_params,
    vvm=0.4,
    constantD=True,
    start_time=3,
    template_folder="loop_reactor_pbe_dynmix_nonstat_headbranch_scaleup",
    account="gas2fuels",
    cores_per_sim=4,
    sims_per_node=26,
):
    """Generate one scale level of the actuator-disk (ball) design sweep.

    One template drives every level; the level `scale` is applied both to the
    mixers.json rescale (mixer positions) and to presteps.sh transformPoints.
    Uses the first `n_sim` designs of `config_dict`, so ``Sim_i`` is the same
    design at every level. `mixer_params` holds Np/Vtip/sigma/radius/swirl_sign.
    """
    if not os.path.isabs(template_folder):
        template_folder = os.path.join(
            BIRD_DIR, "preprocess", "data_case_gen", template_folder
        )
    geom_dict = make_default_geom_dict_from_file(
        os.path.join(template_folder, "system", "mesh.json")
    )
    # mesh.json has no rescale; force the level scale (matched by transformPoints)
    for a in ("x", "y", "z"):
        geom_dict["Geometry"]["OverallDomain"][a]["rescale"] = scale
    seg_geom = from_block_rect_to_seg(geom_dict["Geometry"])
    model = {
        "volumetric_source": "ball",
        "power": "from_Np_Vtip",
        "momentum_source": "axial_and_swirl",
    }

    try:
        shutil.rmtree(study_folder)
    except FileNotFoundError:
        pass
    Path(study_folder).mkdir(parents=True, exist_ok=True)

    sim_ids = sorted(config_dict)[:n_sim]
    for sim_id in sim_ids:
        sim_folder = id2simfolder(sim_id)
        case = os.path.join(study_folder, sim_folder)
        shutil.copytree(template_folder, case)

        bc_dict = {"inlets": [], "outlets": []}
        for br in (6, 4):
            bc_dict["outlets"].append(
                {
                    "branch_id": br,
                    "type": "circle",
                    "frac_space": 1,
                    "normal_dir": 1,
                    "radius": 0.4,
                    "nelements": 50,
                    "block_pos": "top",
                }
            )
        for branch in (0, 1, 2):
            for iind in np.argwhere(config_dict[sim_id][branch] == 1)[:, 0]:
                bc_dict["inlets"].append(
                    {
                        "branch_id": branch,
                        "type": "circle",
                        "frac_space": branchcom_spots[branch][iind],
                        "normal_dir": 1,
                        "radius": 0.4,
                        "nelements": 50,
                        "block_pos": "bottom",
                    }
                )
        generate_stl_patch(
            os.path.join(case, "system", "inlets_outlets.json"),
            bc_dict,
            geom_dict,
        )

        mix_list = []
        for branch in (0, 1, 2):
            for iind in np.argwhere(config_dict[sim_id][branch] == 0)[:, 0]:
                sign = "+" if branch == 0 else "-"
                frac = branchcom_spots[branch][iind]
                # derive this mixer's power from Np/Vtip and its (scaled) radius
                probe = ActuatorMixer()
                probe.update_from_loop_dict(
                    {
                        "branch_id": branch,
                        "frac_space": frac,
                        "radius": mixer_params["radius"],
                    },
                    seg_geom,
                )
                power = actuator_disk_power(
                    mixer_params["Np"], mixer_params["Vtip"], probe.R
                )
                mix_list.append(
                    {
                        "branch_id": branch,
                        "frac_space": float(frac),
                        "start_time": start_time,
                        "sign": sign,
                        "swirl_sign": mixer_params["swirl_sign"],
                        "radius": mixer_params["radius"],
                        "Vtip": mixer_params["Vtip"],
                        "Np": mixer_params["Np"],
                        "sigma": mixer_params["sigma"],
                        "power": power,
                    }
                )
        generate_dynamic_mixer(
            os.path.join(case, "system", "mixers.json"),
            mix_list,
            geom_dict,
            model=model,
        )
        overwrite_vvm(case_folder=case, vvm=vvm)
        overwrite_scale(case_folder=case, scale=scale)
        overwrite_ncores(case_folder=case, n=cores_per_sim)
        overwrite_bubble_size_model(case_folder=case, constantD=constantD)
        write_script_single(case, account=account, cores=cores_per_sim)
        write_script_post_single(case, account=account)

    write_pack_scripts(
        study_folder,
        sim_ids,
        sims_per_node=sims_per_node,
        cores_per_sim=cores_per_sim,
        account=account,
    )
    write_prep(os.path.join(study_folder, "prep.sh"), n_sim)
    save_config_dict(os.path.join(study_folder, "configs.pkl"), config_dict)
    save_config_dict(
        os.path.join(study_folder, "branchcom_spots.pkl"), branchcom_spots
    )
