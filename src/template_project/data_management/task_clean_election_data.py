"""Tasks for managing the data."""

import pandas as pd

from template_project.config import BLD, SRC


def task_clean_elec_data(
    data=SRC / "data" / "Data_Elections.dta",
    produces=BLD / "data" / "election_results.pkl",
):
    """Clean the election data set."""
    raw = pd.read_stata(data, convert_categoricals=False)
    raw_metadata = pd.io.stata.StataReader(data)
    clean = clean_data(raw, raw_metadata)
    clean.to_pickle(produces)
import pandas as pd


def clean_data(raw, metadata):
    df = pd.DataFrame(index=raw.index)
    df["country"] = clean_category(raw["Country"])
    df["nuts_id"] = clean_category(raw["Nuts_id"])
    df["nuts_name"] = clean_category(raw["Name"])
    df["year"] = clean_year(raw["Year"])
    df["election_type"] = clean_election_type(sr = raw["ElectionType"], metadata = metadata)
    df["number_eligible_voters"] = clean_number(raw["EligibleVoters"])
    df["number_valid_votes"] = clean_number(raw["Valid"])
    df["number_parties_effective"] = clean_number(raw["HHI"])
    df["number_votes_far_right"] = clean_number(raw["Far_Right"])
    df["number_votes_far_left"] = clean_number(raw["Far_Left"])
    df["share_votes_far_right"] = clean_share(raw["Far_Right_share"])
    df["share_votes_far_left"] = clean_share(raw["Far_Left_share"])
    df["share_votes_far_any"] = clean_share(raw["Far_share"])
    df["share_voter_turnout"] = clean_share(raw["Turnout"])
    df["number_votes_far_any_incumbent"] = clean_number(raw["F0Far_Incumbent"])
    df["pm_party_orientation"] = clean_pm_party_orientation(raw["left"])
    return df


def clean_category(sr):
    sr = sr.astype(pd.CategoricalDtype())
    return sr


def clean_year(sr):
    sr = sr.astype(pd.Int16Dtype())
    return sr


def clean_election_type(sr, metadata):
    labels = metadata.value_labels()["ElectionType"]
    elec_categories = labels.copy()
    for i, to_append in (5, " A"), (7, " B"):
        elec_categories[i] += to_append
    sr = sr.astype(pd.Int8Dtype()).astype(pd.CategoricalDtype())
    sr = sr.cat.rename_categories(elec_categories)    
    return sr


def clean_number(sr):
    sr = sr.round().astype(pd.UInt32Dtype())
    return sr


def clean_share(sr):
    sr = sr.astype(pd.Float32Dtype())
    return sr


def clean_pm_party_orientation(sr):
    sr = sr.astype(pd.Int8Dtype()).astype(pd.CategoricalDtype())
    sr = sr.cat.rename_categories({0: "Other", 1: "Left-leaning"})
    return sr