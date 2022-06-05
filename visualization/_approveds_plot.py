import matplotlib.pyplot as plt
import matplotlib.colors as mpl_colors
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from templates._models import Condition
from helpers._common import transform_conditions_to_dataframe

def cost_relationship_curve(conditions: list[Condition] = None):

    # Get data source
    path = 'C:/Users/joao.batista/Desktop/My Repos/etr-optimization/aprovados.xlsx'
    df = transform_conditions_to_dataframe(conditions) if conditions else pd.read_excel(path, 'Condições Aprovadas')

    # Generates layers of smooth curves using the model, on a valid area of investigation.
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Creates regression and plots the resulting surfaces
    regression(df.query('extractant == "D2EHPA" and `extractant concentration` == 0.02'), ax)
    regression(df.query('extractant == "D2EHPA" and `extractant concentration` == 0.06'), ax)
    regression(df.query('extractant == "D2EHPA" and `extractant concentration` == 0.10'), ax)
    regression(df.query('extractant == "P507" and `extractant concentration` == 0.02'), ax)
    regression(df.query('extractant == "P507" and `extractant concentration` == 0.06'), ax)
    regression(df.query('extractant == "P507" and `extractant concentration` == 0.10'), ax)
    regression(df.query('extractant == "Cyanex 572" and `extractant concentration` == 0.02'), ax)
    regression(df.query('extractant == "Cyanex 572" and `extractant concentration` == 0.06'), ax)
    regression(df.query('extractant == "Cyanex 572" and `extractant concentration` == 0.10'), ax)

    # Plot the real points as a scatter plot
    generate_scatter_plot(df, ax)

    ax.set_xlabel('Nº Células')
    ax.set_ylabel('Razão A/O')
    ax.set_zlabel('Custo (USD)')
    plt.legend(loc='lower center', bbox_to_anchor=(0.5, 1), ncol=3, fancybox=True)
    plt.show()

def regression(df: pd.DataFrame, ax):

    # Extract independent and dependent variables from dataframe through column matching
    columns = df.columns.values.tolist()
    cost_column = next(column for column in columns if 'cost' in column)
    independent_variables_columns = [column for column in columns if any(match in column for match in ['pHi', 'ao ratio', 'cell'])]

    dependent_variable = df[cost_column].values
    independent_variables = df[independent_variables_columns].values

    # Create a model on polynomial regression
    independent_variables_ = PolynomialFeatures(degree = 3).fit_transform(independent_variables)
    regression = LinearRegression()
    regression.fit(independent_variables_, dependent_variable)

    generate_surfaces(ax, regression, df)

def generate_surfaces(ax, regression: LinearRegression, df: pd.DataFrame):

    # Creates data for surface, predicting results from the model
    n_cells, ao_ratio = np.meshgrid(df['n cells'].unique(), df['ao ratio'].unique())
    pHi, extractant, extractant_concentration = df[['pHi', 'extractant', 'extractant concentration']].mode().values[0]

    exog = pd.DataFrame({'n cells': n_cells.ravel(), 'ao ratio': ao_ratio.ravel()})
    exog['pHi'] = pHi

    out = regression.predict(PolynomialFeatures(degree = 3).fit_transform(exog))

    plot = ax.plot_surface(n_cells, ao_ratio, out.reshape(n_cells.shape),
                           rstride = 1, cstride = 1, alpha = 0.25,
                           label=f'pH = {round(pHi, 1)}, {extractant} {round(extractant_concentration * 100)}%')
    plot._facecolors2d = plot._facecolor3d
    plot._edgecolors2d = plot._edgecolor3d

def generate_scatter_plot(df: pd.DataFrame, ax):
    colors, transparencies, marker_sizes = get_scatter_plot_configs(df)
    ax.scatter(df['n cells'], df['ao ratio'], df['cost (usd)'], color = colors, alpha = transparencies, s = marker_sizes)

def get_scatter_plot_configs(df: pd.DataFrame):
    colors = get_colors(df)
    transparency = get_transparencies(df)
    marker_size = get_marker_sizes(df)
    return colors, transparency, marker_size

def get_colors(df: pd.DataFrame):
    values = df['extractant'].unique().tolist()
    hues = [np.random.random() for _ in values]
    rgb_colors = [mpl_colors.hsv_to_rgb([hue, 1, 0.5]) for hue in hues]

    df['colors'] = df['extractant'].apply(lambda x: rgb_colors[values.index(x)])
    return df['colors']

def get_transparencies(df: pd.DataFrame):
    values = np.flip(df['extractant concentration'].unique()).tolist()
    transparencies = np.linspace(0.1, 1, len(values))

    df['transparency'] = df['extractant concentration'].apply(lambda x: transparencies[values.index(x)])
    return df['transparency']

def get_marker_sizes(df: pd.DataFrame):
    values = np.flip(df['pHi'].unique()).tolist()
    marker_sizes = np.logspace(1, 1.5, len(values))

    df['marker_size'] = df['pHi'].apply(lambda x: marker_sizes[values.index(x)])
    return df['marker_size']