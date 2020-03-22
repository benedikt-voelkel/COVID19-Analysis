import pandas as pd
from glob import glob
from os.path import basename
import numpy as np

def sum_col(df, col_name):
    if df.empty:
        return 0.
    return np.nansum(df[col_name].values)


def collect_from_dfs(dfs, group_by, groups, group_aliases, metrics):
    data = {v: {vc: [] for vc in metrics} for v in groups}
    # NOTE This is quite brute force...
    for df in dfs:
        for name, val_list in data.items():
            alias_list = group_aliases.get(name, [name])
            df_skim = df[df[group_by].isin(alias_list)]
            for met in metrics:
                val_list[met].append(sum_col(df_skim, met))
    return data


def make_dates(paths):
    return [basename(p).rstrip(".csv") for p in paths]


def collect_data(parent_dir, group_by, groups, metrics, **kwargs):
    paths = glob(f"{parent_dir}/**/*.csv", recursive=True)
    if not paths:
        print(f"Cannot find any data in {parent_dir}")
        exit(1)
    paths.sort()
    dates = make_dates(paths)
    dfs = [pd.read_csv(p) for p in paths]
    data = collect_from_dfs(dfs, group_by, groups, kwargs.get("group_aliases", {}), metrics)
    return dates, data
