import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from visualization._regression import get_regression, predict
from global_constants import CHARTS_RESULTS_FOLDER_PATH

def compare_surfaces(df_slices: tuple[pd.DataFrame, pd.DataFrame], save_fig: bool = False):

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    for i, df_slice in enumerate(df_slices):
        regression = get_regression(df_slice)
        extractant_name, extractant_concentration = df_slice[['extractant', 'extractant concentration']].mode().values[0]
        create_surface(ax, regression, df_slice, i)

    plt.suptitle('Efeito da concentração da corrente no custo', fontsize = 12)
    ax.set_title('Concentrado 2x (azul) e concentração original (vermelho) para D2EHPA 2%', fontsize = 9)
    ax.set_xlabel('Nº Células')
    ax.set_ylabel('Razão A/O')
    ax.set_zlabel('Custo (USD)')
    ax.view_init(elev=35, azim=45)
    plt.tight_layout()

    plt.show() if not save_fig else plt.savefig(f'{CHARTS_RESULTS_FOLDER_PATH}Efeito da concentração no custo.png', bbox_inches='tight')

def create_surface(ax, regression: LinearRegression, df: pd.DataFrame, index: int):

    # Creates data for surface, predicting results from the model
    n_cells, ao_ratio = np.meshgrid(np.linspace(df['n cells'].min(), df['n cells'].max(), 100), np.linspace(df['ao ratio'].min(), df['ao ratio'].max(), 100))
    pHi = df['pHi'].mode().values[0]

    features = pd.DataFrame({'n cells': n_cells.ravel(), 'ao ratio': ao_ratio.ravel()})
    features['pHi'] = pHi

    out = predict(regression, features, n_cells.shape)

    plot = ax.plot_surface(n_cells, ao_ratio, out, alpha = 0.5, cmap = 'Blues' if index == 1 else 'Reds', vmin = 0.05)
    plot._facecolors2d = plot._facecolor3d
    plot._edgecolors2d = plot._edgecolor3d