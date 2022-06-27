from matplotlib import projections
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.ticker import StrMethodFormatter

from global_constants import TRI_SURFACES_FOLDER
from visualization._regression import get_regression, predict


def create_multiple_costs_tri_surface(df: pd.DataFrame, save_fig: bool = False):

    extractants = df['extractant'].unique().tolist()
    extractant_concentrations = df['extractant concentration'].unique().tolist()

    only_one_slice = len(extractants) == 1 and len(extractant_concentrations) == 1

    fig, axs = plt.subplots(len(extractants), len(extractant_concentrations), figsize=(16, 16), subplot_kw = { 'projection': '3d' })

    for i, extractant_name in enumerate(extractants):
        for j, extractant_concentration in enumerate(extractant_concentrations):
            df_slice = df.query(f'extractant == "{extractant_name}" and `extractant concentration` == {extractant_concentration}')
            if len(df_slice) > 0: costs_tri_surface(df_slice, axs if only_one_slice else axs[i, j])

    plt.tight_layout()
    plt.subplots_adjust(hspace=0.2, wspace=0.2)

    file_name = 'Custos Previstos ' + (f'{extractant_name} {round(extractant_concentration * 100)}%' if only_one_slice else 'Agrupados')
    plt.show() if not save_fig else plt.savefig(f'{TRI_SURFACES_FOLDER}{file_name}.png', bbox_inches='tight')


def costs_tri_surface(df_slice: pd.DataFrame, ax: plt.Axes):

    df_slice_copy = df_slice.copy()
    df_slice_copy['total cost (1000 usd)'] = df_slice_copy['total cost (usd)'] / 1000
    df_slice_copy.drop('total cost (usd)', axis = 1, inplace = True)

    extractant_name, extractant_concentration = df_slice_copy[['extractant', 'extractant concentration']].mode().values[0]
    df = predict_values(df_slice_copy)

    create_tri_surfaces(df, ax)

    ax.set_xlabel('Nº Células')
    ax.set_ylabel('Razão A/O')
    ax.set_zlabel('Custo Total (mil USD)', labelpad = 14)
    ax.view_init(elev=35, azim=45)
    ax.set_xticks(np.arange(2, 21, 2))

    ax.zaxis.set_major_formatter(StrMethodFormatter('${x:,.0f}'))
    ax.set_title(f'{extractant_name} {round(extractant_concentration * 100)}%')


def predict_values(df: pd.DataFrame) -> pd.DataFrame:
    n_cells, ao_ratio, pHi = np.meshgrid(np.linspace(2, 20, 37), np.linspace(0.5, 2.5, 100), np.linspace(1, 2, 11))
    features = pd.DataFrame({'n cells': n_cells.ravel(), 'ao ratio': ao_ratio.ravel(), 'pHi': pHi.ravel()})
    cost_out = predict(get_regression(df, dependent_variable_substring = 'total cost (1000 usd)'), features, n_cells.ravel().shape)
    purity_out = predict(get_regression(df, dependent_variable_substring = 'purity'), features, n_cells.ravel().shape)
    features['cost'] = cost_out
    features['purity'] = purity_out

    return features


def create_tri_surfaces(df: pd.DataFrame, ax: plt.Axes):
    create_tri_surface(df.query('purity >= 0.995 and `n cells` <= 15 and `ao ratio` <= 2'), ax, 'blue', 0.3)
    create_tri_surface(df.query('purity < 0.995 and `n cells` <= 15 and `ao ratio` <= 2'), ax, 'red', 0.3)
    create_tri_surface(df.query('purity >= 0.995 and `n cells` <= 15 and `ao ratio` > 2'), ax, 'green', 0.3)
    create_tri_surface(df.query('purity < 0.995 and `n cells` <= 15 and `ao ratio` > 2'), ax, 'purple', 0.5)
    create_tri_surface(df.query('purity >= 0.995 and `n cells` >= 15'), ax, 'green', 0.3)
    create_tri_surface(df.query('purity < 0.995 and `n cells` >= 15'), ax, 'purple', 0.5)


def create_tri_surface(df: pd.DataFrame, ax: plt.Axes, color, alpha):
    if len(df) > 3 and len(df['n cells'].unique()) > 1 and len(df['ao ratio'].unique()) > 1:
        ax.plot_trisurf(df['n cells'], df['ao ratio'], df['cost'], color = color, alpha = alpha)