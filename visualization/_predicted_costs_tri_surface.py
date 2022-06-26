import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.ticker import StrMethodFormatter

from global_constants import TRI_SURFACES_FOLDER
from visualization._regression import get_regression, predict


def predicted_costs_tri_surface(df_slice: pd.DataFrame, save_fig: bool = False):

    df_slice_copy = df_slice.copy()
    df_slice_copy['total cost (1000 usd)'] = df_slice_copy['total cost (usd)'] / 1000
    df_slice_copy.drop('total cost (usd)', axis = 1, inplace = True)

    extractant_name, extractant_concentration = df_slice_copy[['extractant', 'extractant concentration']].mode().values[0]
    df = predict_values(df_slice_copy)

    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection='3d')

    create_tri_surfaces(df, ax)

    ax.set_xlabel('Nº Células')
    ax.set_ylabel('Razão A/O')
    ax.set_zlabel('Custo Total (mil USD)', labelpad = 14)
    ax.view_init(elev=35, azim=45)

    ax.zaxis.set_major_formatter(StrMethodFormatter('${x:,.0f}'))
    ax.set_title(f'{extractant_name} {round(extractant_concentration * 100)}%')

    plt.xticks(np.arange(2, 21, 2))
    plt.tight_layout()
    plt.show() if not save_fig else plt.savefig(f'{TRI_SURFACES_FOLDER}Custos Previstos {extractant_name} {round(extractant_concentration * 100)}%.png',
                                                bbox_inches='tight')


def predict_values(df: pd.DataFrame) -> pd.DataFrame:
    n_cells, ao_ratio, pHi = np.meshgrid(np.linspace(2, 20, 19), np.linspace(0.5, 2.5, 100), np.linspace(1, 2, 11))
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
    if len(df) > 3:
        ax.plot_trisurf(df['n cells'], df['ao ratio'], df['cost'], color = color, alpha = alpha)