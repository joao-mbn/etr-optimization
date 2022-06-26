import math as m

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from helpers._common import create_sub_dataframe
from helpers._utils import format_to_currency
from global_constants import CHARTS_RESULTS_FOLDER_PATH


def detailed_cost_chart(df: pd.DataFrame, save_fig: bool = False) -> None:

    label, relative_detailed_cost, accumulated_relative_detailed_cost, total_cost = get_detailed_cost_info_for_chart(df)

    category_colors = get_colors(relative_detailed_cost)
    different_costs = relative_detailed_cost.columns.values

    fig = plt.figure(figsize=(14, 8))

    ax = fig.add_axes([0.25, 0.1, 0.6, 0.8])
    ax.xaxis.set_visible(False)
    ax.set_xlim(0, 100)  # 0 to 100%

    plt.yticks(fontsize=8, rotation=0)

    for colname, color in zip(different_costs, category_colors):

        widths = relative_detailed_cost[colname]
        starts = accumulated_relative_detailed_cost[colname] - widths
        bar = ax.barh(label, widths, left = starts, height = 0.5, label = colname, color = color)

        r, g, b, _ = color
        text_color = 'white' if r * g * b < 0.5 else 'black'
        bar_labels = [x if x > 3 else '' for x in widths.values] # Ignore value's label if it represents less then 3% of total.
        ax.bar_label(bar, label_type = 'center', color = text_color, labels = bar_labels)

    ax2 = ax.twinx()
    ax2.barh(total_cost.apply(format_to_currency), np.zeros(len(total_cost)), height = 0.5)

    ax.legend(ncol = m.ceil(len(different_costs) / 2), bbox_to_anchor = (0, 1), loc = 'lower left', fontsize = 'small')
    plt.show() if not save_fig else plt.savefig(f'{CHARTS_RESULTS_FOLDER_PATH}Custos Detalhados.png', bbox_inches='tight')


def get_detailed_cost_info_for_chart(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:

    df_size = len(df)
    one_tenth_interval = m.ceil(df_size * 0.1)
    evenly_spaced_results = df[::one_tenth_interval]

    if df_size % one_tenth_interval != 0: evenly_spaced_results.loc[len(evenly_spaced_results)] = df.iloc[-1]

    total_cost = evenly_spaced_results['total cost (usd)']
    raw_total_cost = evenly_spaced_results['raw total cost (usd)']
    detailed_cost = create_sub_dataframe(evenly_spaced_results, white_list_substrings = ['cost', 'loss', 'interest'],
                                         black_list_substrings=['interest on capital', 'operating cost', 'total cost'])

    evenly_spaced_results['label'] = evenly_spaced_results.apply(create_label, axis=1)
    relative_detailed_cost = (detailed_cost.div(raw_total_cost, axis=0) * 100).round(2)
    accumulated_relative_detailed_cost = relative_detailed_cost.cumsum(axis=1)

    return evenly_spaced_results['label'], relative_detailed_cost, accumulated_relative_detailed_cost, total_cost


def create_label(row: pd.Series) -> str:
    return  f'{row["n cells"]} Células, Razão A/O = {round(row["ao ratio"], 1)}, pHi = {round(row["pHi"], 2)}, ' + \
            f'{row["extractant"]} {round(row["extractant concentration"] * 100)}%'


def get_colors(df: pd.DataFrame) -> dict:

    # To be improved with a better color scheme, if necessary.

    interest_on_capital_related_costs = df.columns.values[df.columns.str.contains('interest')]
    ree_acid_costs = df.columns.values[df.columns.str.contains('ree|acid')]
    extractant_solvent_costs = df.columns.values[df.columns.str.contains('extractant|solvent')]
    energy_operators_costs = df.columns.values[df.columns.str.contains('energy|operators')]

    interest_on_capital_colors = plt.colormaps['RdYlBu'](np.linspace(0.8, 1, len(interest_on_capital_related_costs)))
    ree_acid_colors = plt.colormaps['RdYlBu'](np.linspace(0.1, 0.3, len(ree_acid_costs)))
    extractant_solvent_costs = plt.colormaps['PiYG'](np.linspace(0.8, 1, len(ree_acid_costs)))
    energy_operators_costs = plt.colormaps['PiYG'](np.linspace(0.1, 0.3, len(ree_acid_costs)))

    return np.concatenate((interest_on_capital_colors, ree_acid_colors, extractant_solvent_costs, energy_operators_costs))

