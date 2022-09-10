import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from global_constants import CHARTS_RESULTS_FOLDER_PATH
from matplotlib.ticker import StrMethodFormatter
from sklearn.linear_model import LinearRegression

from visualization._regression import get_regression, predict


def compare_surfaces(df_slices: tuple[pd.DataFrame, pd.DataFrame], save_fig: bool = False):

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    for df_slice, color in zip(df_slices, ('red', 'blue')):
        df_slice['total cost (1000 usd)'] = df_slice['total cost (usd)'] / 1000
        df_slice.drop('total cost (usd)', axis = 1, inplace = True)
        pHi = df_slice['pHi'].mode().values[0]
        df_scatter = df_slice.query(f'pHi == {pHi}')
        ax.plot_trisurf(df_scatter['n cells'], df_scatter['ao ratio'], df_scatter['total cost (1000 usd)'], color = color, alpha = 0.5)

    plt.suptitle('Efeito da concentração da corrente no custo', fontsize = 12)
    ax.set_title('Concentrado 2x (azul) e concentração original (vermelho) para D2EHPA 10%', fontsize = 9)
    ax.set_xlabel('Nº Células')
    ax.set_ylabel('Razão A/O')
    ax.set_zlabel('Custo Total (mil USD)', labelpad = 14)
    ax.view_init(elev=35, azim=45)
    ax.zaxis.set_major_formatter(StrMethodFormatter('${x:,.0f}'))
    plt.tight_layout()

    plt.show() if not save_fig else plt.savefig(f'{CHARTS_RESULTS_FOLDER_PATH}Efeito da concentração no custo.png', bbox_inches='tight')
