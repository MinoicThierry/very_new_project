# Create a file `task_merge_data.py`, which contains a task function that reads in the two
# cleaned datasets, keeps the `election_cols` from above, and saves the resulting
# DataFrame in a file `merged_data.pkl` in the `bld` directory.

# Verify that this task is being run if you start pytask from the command line and that
# the result is the same as the merged data from Task 8.

import pandas as pd

from very_new_project.config import BLD

def task_merge_data(election_results = BLD / "data" / "election_results.pkl",
                    deficits = BLD / "data" / "deficits.pkl",
                    produces = BLD / "data" / "merged_data.pkl"):
    election = pd.read_pickle(election_results)
    deficits = pd.read_pickle(deficits)

    election_cols = [
    "country",
    "year",
    "nuts_name",
    "election_type",
    "share_votes_far_right",
    "share_votes_far_left",
    "share_votes_far_any",
    ]

    merged_data = election[election_cols].merge(right=deficits,
                                             how="inner",
                                             on=["country", "year"],)
    
    merged_data.to_pickle(produces)
