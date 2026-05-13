import pandas as pd


def read_raw_data(
    filename: str = "/Users/mhassana/Desktop/GitHub/BioReactorDesign_may13/kla_estimation/oxygenConcentration_all.xlsx",
):
    raw_data = {}
    raw_data["1_scfh"] = []
    raw_data["2_scfh"] = []
    raw_data["3_scfh"] = []

    df = pd.read_excel(filename)
    for column in df.columns:
        if "1scfh" in column.lower():
            time = df.dropna(subset=[column])["t(seconds)"]
            conc = df.dropna(subset=[column])[column]
            assert time.size == conc.size
            raw_data["1_scfh"].append(
                {
                    "t_s": time.to_numpy().astype("float32"),
                    "c_mol_m3": conc.to_numpy().astype("float32"),
                }
            )
        elif "2scfh" in column.lower():
            time = df.dropna(subset=[column])["t(seconds)"]
            conc = df.dropna(subset=[column])[column]
            assert time.size == conc.size
            raw_data["2_scfh"].append(
                {
                    "t_s": time.to_numpy().astype("float32"),
                    "c_mol_m3": conc.to_numpy().astype("float32"),
                }
            )
        elif "3scfh" in column.lower():
            time = df.dropna(subset=[column])["t(seconds)"]
            conc = df.dropna(subset=[column])[column]
            assert time.size == conc.size
            raw_data["3_scfh"].append(
                {
                    "t_s": time.to_numpy().astype("float32"),
                    "c_mol_m3": conc.to_numpy().astype("float32"),
                }
            )

    assert len(raw_data["1_scfh"]) == 3
    assert len(raw_data["2_scfh"]) == 3
    assert len(raw_data["3_scfh"]) == 2

    return raw_data


if __name__ == "__main__":
    raw_data = read_raw_data()
    breakpoint()
