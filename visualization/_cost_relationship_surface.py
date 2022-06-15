from matplotlib.cm import ScalarMappable
import matplotlib.pyplot as plt
import matplotlib.colors as mpl_colors
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from visualization._regression import get_regression, predict
from global_constants import CHARTS_RESULTS_FOLDER_PATH
from templates._types import Number

def cost_relationship_surface(df_slice: pd.DataFrame, save_fig: bool = False):

    regression = get_regression(df_slice)
    extractant_name, extractant_concentration = df_slice[['extractant', 'extractant concentration']].mode().values[0]

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    mappable = plt.cm.ScalarMappable(cmap='Spectral')

    create_surface(ax, regression, df_slice, mappable)
    create_scatter_plot(df_slice, ax)

    ax.set_xlabel('Nº Células')
    ax.set_ylabel('Razão A/O')
    ax.set_zlabel('Custo (USD)')
    ax.view_init(elev=35, azim=45)
    plt.legend(loc='lower center', bbox_to_anchor=(0.5, 1))
    plt.colorbar(mappable)
    plt.tight_layout()

    plt.show() if not save_fig else plt.savefig(f'{CHARTS_RESULTS_FOLDER_PATH}Superfície {extractant_name} {round(extractant_concentration * 100)}%.png',
                                                bbox_inches='tight')

def create_surface(ax, regression: LinearRegression, df: pd.DataFrame, mappable: ScalarMappable):

    # Creates data for surface, predicting results from the model
    n_cells, ao_ratio = np.meshgrid(np.sort(df['n cells'].unique()), np.sort(df['ao ratio'].unique()))
    pHi, extractant, extractant_concentration = df[['pHi', 'extractant', 'extractant concentration']].mode().values[0]

    features = pd.DataFrame({'n cells': n_cells.ravel(), 'ao ratio': ao_ratio.ravel()})
    features['pHi'] = pHi

    out = predict(regression, features, n_cells.shape)

    mappable.set_array(out)
    plot = ax.plot_surface(n_cells, ao_ratio, out,
                           rstride = 1, cstride = 1, alpha = 0.4, cmap = mappable.cmap, norm = mappable.norm,
                           label=f'pH = {round(pHi, 1)}, {extractant} {round(extractant_concentration * 100)}%')
    plot._facecolors2d = plot._facecolor3d
    plot._edgecolors2d = plot._edgecolor3d

def create_scatter_plot(df: pd.DataFrame, ax):
    transparencies = create_property_scale(df, 'pHi', (0.3, 1))
    marker_sizes = create_property_scale(df, 'pHi', (0.5, 1), False)
    colors = create_property_scale(df, 'extractant').apply(lambda hue: mpl_colors.hsv_to_rgb((hue, 0, 0)))

    ax.scatter(df['n cells'], df['ao ratio'], df['total cost (usd)'], color = colors, alpha = transparencies, s = marker_sizes)

def create_property_scale(df: pd.DataFrame, reference_column: str,
                          scale_range: tuple[Number, Number] = (0, 1),
                          use_linear_scale: bool = True,
                          reverse_reference_column: bool = False) -> pd.Series:

    values = np.flip(df[reference_column].unique()).tolist() if reverse_reference_column else df[reference_column].unique().tolist()
    property = np.linspace(*scale_range, len(values)) if use_linear_scale else np.logspace(*scale_range, len(values))

    return df[reference_column].apply(lambda x: property[values.index(x)])
