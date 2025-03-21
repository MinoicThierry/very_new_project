import pandas as pd
import pytask

from very_new_project.config import BLD, SRC


@pytask.mark.filterwarnings("ignore:.*:UserWarning")
def task_clean_ales_data(
    data=SRC / "data" / "Alesina.xlsx",
    produces=BLD / "data" / "deficits.pkl",
):
    """Clean the Alesina data set."""
    raw = pd.read_excel(data, sheet_name="MacroData",)
    clean = _clean_data(raw)
    clean.to_pickle(produces)


def _clean_data(raw):
    df = pd.DataFrame(index=raw.index)
    df["country"] = raw["Unnamed: 1"]
    df["year"] = raw["Year"]
    df["raw_deficit"] = raw["deficit"]
    df["primary_deficit"] = raw["primary_def"]
    return df