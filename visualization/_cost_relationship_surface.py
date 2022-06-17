import matplotlib.colors as mpl_colors
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from global_constants import CHARTS_RESULTS_FOLDER_PATH
from matplotlib.cm import ScalarMappable
from matplotlib.ticker import StrMethodFormatter
from sklearn.linear_model import LinearRegression
from templates._types import Number

from visualization._regression import get_regression, predict


def cost_relationship_surface(df_slice: pd.DataFrame, save_fig: bool = False):

    df_slice_copy = df_slice.copy()
    df_slice_copy['total cost (1000 usd)'] = df_slice_copy['total cost (usd)'] / 1000
    df_slice_copy.drop('total cost (usd)', axis = 1, inplace = True)

    regression = get_regression(df_slice_copy)
    extractant_name, extractant_concentration = df_slice_copy[['extractant', 'extractant concentration']].mode().values[0]

    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection='3d')
    mappable = plt.cm.ScalarMappable(cmap='Spectral')

    create_surface(ax, regression, df_slice_copy, mappable)
    create_scatter_plot(df_slice_copy, ax)

    ax.set_xlabel('Nº Células')
    ax.set_ylabel('Razão A/O')
    ax.set_zlabel('Custo Total (mil USD)', labelpad = 14)
    ax.view_init(elev=35, azim=45)
    ax.zaxis.set_major_formatter(StrMethodFormatter('${x:,.0f}'))
    plt.legend()
    plt.colorbar(mappable, shrink = 0.5)
    plt.tight_layout()

    plt.show() if not save_fig else plt.savefig(f'{CHARTS_RESULTS_FOLDER_PATH}Superfície {extractant_name} {round(extractant_concentration * 100)}%.png',
                                                bbox_inches='tight')

def create_surface(ax, regression: LinearRegression, df: pd.DataFrame, mappable: ScalarMappable):
    n_cells, ao_ratio = np.meshgrid(np.linspace(df['n cells'].min(), df['n cells'].max(), 100), np.linspace(df['ao ratio'].min(), df['ao ratio'].max(), 100))
    pHi, extractant, extractant_concentration = df[['pHi', 'extractant', 'extractant concentration']].mode().values[0]

    features = pd.DataFrame({'n cells': n_cells.ravel(), 'ao ratio': ao_ratio.ravel()})
    features['pHi'] = pHi

    out = predict(regression, features, n_cells.shape)

    mappable.set_array(out)
    plot = ax.plot_surface(n_cells, ao_ratio, out,
                           rstride = 1, cstride = 1, alpha = 0.8, cmap = mappable.cmap, norm = mappable.norm,
                           label=f'{extractant} {round(extractant_concentration * 100)}%')
    plot._facecolors2d = plot._facecolor3d
    plot._edgecolors2d = plot._edgecolor3d

def create_scatter_plot(df: pd.DataFrame, ax):
    transparencies = create_property_scale(df, 'pHi', (0, 0))
    marker_sizes = create_property_scale(df, 'pHi', (0.5, 1), False)
    colors = create_property_scale(df, 'extractant').apply(lambda hue: mpl_colors.hsv_to_rgb((hue, 0, 0)))

    ax.scatter(df['n cells'], df['ao ratio'], df['total cost (1000 usd)'], color = colors, alpha = transparencies, s = marker_sizes)

def create_property_scale(df: pd.DataFrame, reference_column: str,
                          scale_range: tuple[Number, Number] = (0, 1),
                          use_linear_scale: bool = True,
                          reverse_reference_column: bool = False) -> pd.Series:

    values = np.flip(df[reference_column].unique()).tolist() if reverse_reference_column else df[reference_column].unique().tolist()
    property = np.linspace(*scale_range, len(values)) if use_linear_scale else np.logspace(*scale_range, len(values))

    return df[reference_column].apply(lambda x: property[values.index(x)])
