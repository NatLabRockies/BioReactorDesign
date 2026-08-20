import json
import os
import pickle
import shutil
import tempfile
from pathlib import Path

import numpy as np

from bird.preprocess.json_gen.design_io import *
from bird.preprocess.json_gen.generate_designs import *


def test_continuous_loop():

    BIRD_CASE_GEN_DATA_DIR = os.path.join(
        Path(__file__).parent,
        "..",
        "..",
        "bird",
        "preprocess",
        "data_case_gen",
    )
    # Output to temporary directory and delete when done
    with tempfile.TemporaryDirectory() as tmpdirname:
        generate_single_scaledup_reactor_sparger_cases(
            sparger_locs=[0.3, 0.5, 1.4],
            sim_id=0,
            vvm=0.4,
            study_folder=tmpdirname,
            template_folder=os.path.join(
                BIRD_CASE_GEN_DATA_DIR,
                "loop_reactor_pbe_dynmix_nonstat_headbranch_scaleup",
            ),
        )

    # Output to temporary directory and delete when done
    with tempfile.TemporaryDirectory() as tmpdirname:
        generate_single_scaledup_reactor_sparger_cases(
            sparger_locs=[0.3, 0.35],
            sim_id=0,
            vvm=0.4,
            study_folder=tmpdirname,
            template_folder=os.path.join(
                BIRD_CASE_GEN_DATA_DIR,
                "loop_reactor_pbe_dynmix_nonstat_headbranch_scaleup",
            ),
            bypass_sparger_spacing=True,
        )


def test_discrete_loop():

    BIRD_CASE_GEN_DATA_DIR = os.path.join(
        Path(__file__).parent,
        "..",
        "..",
        "bird",
        "preprocess",
        "data_case_gen",
    )

    def optimization_setup():
        # spots on the branches where we can place sparger or mixers
        branchcom_spots = {}
        branchcom_spots[0] = np.linspace(0.2, 0.8, 4)
        branchcom_spots[1] = np.linspace(0.2, 0.8, 3)
        branchcom_spots[2] = np.linspace(0.2, 0.8, 4)
        # branches where the sparger and mixers are placed
        branches_com = [0, 1, 2]
        return branchcom_spots, branches_com

    def random_sample(branches_com, branchcom_spots, config_dict={}):
        config = {}
        # choices = ["mix", "sparger", "none"]
        choices_com = [0, 1, 2]
        for branch in branches_com:
            config[branch] = np.random.choice(
                choices_com, size=len(branchcom_spots[branch])
            )

        existing = False
        new_config_key = 0
        for old_key_conf in config_dict:
            if compare_config(config_dict[old_key_conf], config):
                existing = True
                print("FOUND SAME CONFIG")
                return config_dict
            new_config_key = old_key_conf + 1

        if check_config(config):
            config_dict[new_config_key] = config

        return config_dict

    branchcom_spots, branches_com = optimization_setup()
    n_sim = 20
    config_dict = {}
    for i in range(n_sim):
        config_dict = random_sample(
            branches_com, branchcom_spots, config_dict=config_dict
        )

    vvm_l = [0.1, 0.4]
    pow_l = [3000, 6000]

    for vvm_v in vvm_l:
        vvm_str = str(vvm_v).replace(".", "_")
        for pow_v in pow_l:
            # Output to temporary directory and delete when done
            with tempfile.TemporaryDirectory() as tmpdirname:
                # study_folder = f"study_scaleup_{vvm_str}vvm_{pow_v}W"
                study_folder = tmpdirname
                generate_scaledup_reactor_cases(
                    config_dict,
                    branchcom_spots,
                    vvm=vvm_v,
                    power=pow_v,
                    constantD=True,
                    study_folder=study_folder,
                    template_folder=os.path.join(
                        BIRD_CASE_GEN_DATA_DIR,
                        "loop_reactor_pbe_dynmix_nonstat_headbranch_scaleup",
                    ),
                )
                write_script_start(f"{study_folder}/many_scripts_start", n_sim)
                write_script_post(f"{study_folder}/many_scripts_post", n_sim)
                write_prep(f"{study_folder}/prep.sh", n_sim)
                save_config_dict(f"{study_folder}/configs.pkl", config_dict)
                save_config_dict(
                    f"{study_folder}/branchcom_spots.pkl", branchcom_spots
                )


def test_generate_leveled_reactor_cases():
    # Outlets must be template-driven (read from the template's
    # inlets_outlets.json), not hardcoded: a template carrying a distinctive
    # full-face rectangle outlet must reproduce that rectangle in every
    # generated case. Under the old hardcoded (branch 6 & 4 disks) path this
    # assertion fails.
    BIRD_CASE_GEN_DATA_DIR = os.path.join(
        Path(__file__).parent,
        "..",
        "..",
        "bird",
        "preprocess",
        "data_case_gen",
    )
    bundled = os.path.join(
        BIRD_CASE_GEN_DATA_DIR,
        "loop_reactor_pbe_dynmix_nonstat_headbranch_scaleup",
    )
    rectangle = {
        "type": "rectangle",
        "normal_dir": 1,
        "centx": 0.5,
        "centy": 11.0,
        "centz": 2.5,
        "width": 3.0,
        "height": 7.0,
    }

    branchcom_spots = {
        0: np.linspace(0.2, 0.8, 4),
        1: np.linspace(0.2, 0.8, 3),
        2: np.linspace(0.2, 0.8, 4),
    }
    branches_com = [0, 1, 2]
    config_dict = {}
    for _ in range(10):
        config = {
            b: np.random.choice([0, 1, 2], size=len(branchcom_spots[b]))
            for b in branches_com
        }
        if check_config(config):
            config_dict[len(config_dict)] = config
        if len(config_dict) >= 1:
            break
    mixer_params = {
        "Np": 6,
        "Vtip": 1.5,
        "sigma": 0.35,
        "radius": 0.4,
        "sign": {0: "+", 1: "+", 2: "-"},
        "swirl_sign": {0: "+", 1: "+", 2: "-"},
    }

    with tempfile.TemporaryDirectory() as tmpdirname:
        # a template whose outlet differs from the old hardcoded disks
        template = os.path.join(tmpdirname, "template")
        shutil.copytree(bundled, template)
        io_path = os.path.join(template, "system", "inlets_outlets.json")
        with open(io_path) as f:
            io = json.load(f)
        io["outlets"] = [rectangle]
        with open(io_path, "w") as f:
            json.dump(io, f)

        study = os.path.join(tmpdirname, "study")
        generate_leveled_reactor_cases(
            config_dict,
            branchcom_spots,
            scale=0.05,
            n_sim=1,
            study_folder=study,
            mixer_params=mixer_params,
            template_folder=template,
            constantD=True,
            start_time=1,
        )
        with open(
            os.path.join(study, "Sim_0000", "system", "inlets_outlets.json")
        ) as f:
            generated = json.load(f)
        assert generated["outlets"] == [rectangle]


def test_overwrite_controldict():

    template_control_dict = os.path.join(
        Path(__file__).parent,
        "..",
        "..",
        "bird",
        "preprocess",
        "data_case_gen",
        "loop_reactor_pbe_dynmix_nonstat_headbranch_scaleup",
        "system",
        "controlDict",
    )

    def read_scalars(control_dict_path):
        scalars = {}
        with open(control_dict_path, "r") as f:
            for line in f:
                tokens = line.strip().rstrip(";").split()
                if len(tokens) == 2 and tokens[0] in (
                    "deltaT",
                    "endTime",
                    "maxCo",
                    "maxDeltaT",
                ):
                    scalars[tokens[0]] = tokens[1]
        return scalars

    # a full params dict is applied verbatim to a fresh case copy
    params = {
        "maxCo": "0.25",
        "maxDeltaT": "0.00025",
        "deltaT": "1e-5",
        "endTime": "100",
    }
    with tempfile.TemporaryDirectory() as tmpdirname:
        case = os.path.join(tmpdirname, "case")
        os.makedirs(os.path.join(case, "system"))
        shutil.copy(
            template_control_dict,
            os.path.join(case, "system", "controlDict"),
        )
        overwrite_controldict(case, params)
        written = read_scalars(os.path.join(case, "system", "controlDict"))
        assert written == params

    # a partial params dict overwrites only the keys it names
    with tempfile.TemporaryDirectory() as tmpdirname:
        case = os.path.join(tmpdirname, "case")
        os.makedirs(os.path.join(case, "system"))
        shutil.copy(
            template_control_dict,
            os.path.join(case, "system", "controlDict"),
        )
        before = read_scalars(os.path.join(case, "system", "controlDict"))
        overwrite_controldict(case, {"endTime": "50"})
        after = read_scalars(os.path.join(case, "system", "controlDict"))
        assert after["endTime"] == "50"
        assert after["deltaT"] == before["deltaT"]
        assert after["maxCo"] == before["maxCo"]
