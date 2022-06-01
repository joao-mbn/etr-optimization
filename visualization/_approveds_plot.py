from cProfile import label
from itertools import combinations
import matplotlib.pyplot as plt
import matplotlib.colors as mpl_colors
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from templates._models import Condition
from helpers._common import transform_conditions_to_dataframe

def cost_relationship_curve(conditions: list[Condition] = None):

    # Choose data source
    if conditions:
        df = transform_conditions_to_dataframe(conditions)
    else:
        df = pd.read_excel('C:/Users/joao.batista/Desktop/My Repos/etr-optimization/aprovados.xlsx', 'Condições Aprovadas')

    # Generates layers of smooth curves using the model, on a valid area of investigation.
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Plot the real points as a scatter plot
    colors, transparencies, marker_sizes = get_scatter_plot_configs(df)
    ax.scatter(df['n cells'], df['ao ratio'], df['cost (usd)'], color = colors, alpha = transparencies, s = marker_sizes)

    """
    set a reference point where to put the legend box at halfway through the chart width and on top of its height,
    starting from the chart's lower left corner, a legend box using this reference point as the lower center of it is created.
    """
    ax.set_xlabel('Nº Células')
    ax.set_ylabel('Razão A/O')
    ax.set_zlabel('Custo (USD)')

    plt.legend(loc='lower center', bbox_to_anchor=(0.5, 1), ncol=3, fancybox=True, shadow=True)
    plt.show()

def get_scatter_plot_configs(df: pd.DataFrame):

    colors = get_colors(df)
    transparency = get_transparencies(df)
    marker_size = get_marker_sizes(df)
    return colors, transparency, marker_size

def get_colors(df: pd.DataFrame):

    values = df['extractant'].unique().tolist()
    hues = [np.random.random() for _ in values]
    rgb_colors = [mpl_colors.hsv_to_rgb([hue, 1, 1]) for hue in hues]

    df['colors'] = df['extractant'].apply(lambda x: rgb_colors[values.index(x)])
    return df['colors']

def get_transparencies(df: pd.DataFrame):

    values = np.flip(df['extractant concentration'].unique()).tolist()
    transparencies = np.linspace(0.1, 1, len(values))

    df['transparency'] = df['extractant concentration'].apply(lambda x: transparencies[values.index(x)])
    return df['transparency']

def get_marker_sizes(df: pd.DataFrame):

    values = np.flip(df['pHi'].unique()).tolist()
    marker_sizes = np.logspace(0, 1, len(values))

    df['marker_size'] = df['pHi'].apply(lambda x: marker_sizes[values.index(x)])
    return df['marker_size']


def regression(df: pd.DataFrame, ax):

    add_extractants_dummy_columns(df)

    # Extract independent and dependent variables from dataframe through column matching
    columns = df.columns.values.tolist()
    cost_column = next(column for column in columns if 'cost' in column)
    independent_variables_columns = [column for column in columns
                                     if any(match in column
                                            for match in ['pHi', 'ao ratio', 'cell', 'extractant concentration', 'dummy'])]

    dependent_variable = df[cost_column].values
    independent_variables = df[independent_variables_columns].values
    n_vars = len(independent_variables_columns)

    # Create a model on polynomial regression
    independent_variables_ = PolynomialFeatures(degree = n_vars).fit_transform(independent_variables)
    regression = LinearRegression()
    regression.fit(independent_variables_, dependent_variable)

    generate_surfaces(ax, regression, n_vars)

def add_extractants_dummy_columns(df: pd.DataFrame):
    extractants = df['extractant'].unique()
    for extractant in extractants:
        df[f'{extractant}_dummy'] = df['extractant'].apply(lambda x: 1 if x == extractant else 0)

def generate_surfaces(ax, regression, n_vars):

    # Creates data for surface, predicting results from the model
    N_CELLS, AO_RATIO = np.meshgrid(np.arange(2, 11), np.linspace(0.5, 2, 16), sparse = False)
    exog = pd.DataFrame({'n cells': N_CELLS.ravel(), 'x2': AO_RATIO.ravel()})
    exog['extractant volume'] = 0.02
    exog['Is D2EHPA'] = 1
    exog['Is P507'] = 0
    exog['Is Cyanex 572'] = 0

    for pH in np.linspace(1.5, 2.5, 6):
        exog['pHi'] = pH
        out = regression.predict(PolynomialFeatures(degree = n_vars).fit_transform(exog))

        plot = ax.plot_surface(N_CELLS, AO_RATIO, out.reshape(N_CELLS.shape), rstride = 1, cstride = 1, alpha = 0.5, label=f'pH = {pH}')
        plot._facecolors2d = plot._facecolor3d
        plot._edgecolors2d = plot._edgecolor3d