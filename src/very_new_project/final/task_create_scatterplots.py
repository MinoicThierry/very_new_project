import pandas as pd

pd.options.mode.copy_on_write = True
pd.options.future.infer_string = False
pd.options.plotting.backend = "plotly"

from very_new_project.config import BLD


products = {
    ("share_votes_far_right", "raw_deficit"): BLD / "figures" / "scatterplot_share_far_right_raw_deficit.svg",
    ("share_votes_far_right", "primary_deficit"): BLD / "figures" / "scatterplot_share_far_right_primary_deficit.svg",  
    ("share_votes_far_left", "raw_deficit"): BLD / "figures" / "scatterplot_share_far_left_raw_deficit.svg",
    ("share_votes_far_left", "primary_deficit"): BLD / "figures" / "scatterplot_share_far_left_primary_deficit.svg",
    ("share_votes_far_any", "raw_deficit"): BLD / "figures" / "scatterplot_share_far_any_raw_deficit.svg",
    ("share_votes_far_any", "primary_deficit"): BLD / "figures" / "scatterplot_share_far_any_primary_deficit.svg",
}


def task_create_scatterplots(merged_data = BLD / "data" / "merged_data.pkl", produces = products):
    fig_data = pd.read_pickle(merged_data)
    keys = products.keys()
    for key in keys:
        key1, key2 = key
        fig = _plot_deficit_vote_share(fig_data = fig_data, key1 = key1, key2 = key2)
        fig.write_image(products[key])


def _plot_deficit_vote_share(fig_data, key1, key2):
    only_elections = fig_data[fig_data["election_type"].notna()]
    return only_elections.plot.scatter(x=key2, y=key1, color="nuts_name")