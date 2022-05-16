from itertools import combinations
import matplotlib.pyplot as plt
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
        df = pd.read_excel('C:/Users/joao.batista/Desktop/aprovados.xlsx', 'Condições Aprovadas')

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

    # Creates data for surface, predicting results from the model
    N_CELLS, AO_RATIO = np.meshgrid(np.arange(2, 10), np.linspace(0.5, 2, 16), sparse = False)
    exog = pd.DataFrame({'n cells': N_CELLS.ravel(), 'x2': AO_RATIO.ravel()})
    exog['pHi'] = 2
    exog['extractant volume'] = 0.1
    exog['Is D2EHPA'] = 0
    exog['Is P507'] = 1
    exog['Is Cyanex 572'] = 0
    out = regression.predict(PolynomialFeatures(degree = n_vars).fit_transform(exog))

    # Generates layers of smooth curves using the model, on a valid area of investigation.
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    plot = ax.plot_surface(N_CELLS, AO_RATIO, out.reshape(N_CELLS.shape), rstride = 1, cstride = 1, alpha = 0.5)

    # Plot the real points as a scatter plot
    ax.scatter(df['n cells'], df['ao ratio'], df['cost (usd)'], color = 'r', s = 2)

    """
    set a reference point where to put the legend box at halfway through the chart width and on top of its height,
    starting from the chart's lower left corner, a legend box using this reference point as the lower center of it is created.
    """
    plt.legend(loc='lower center', bbox_to_anchor=(0.5, 1), ncol=3, fancybox=True, shadow=True)
    plot._facecolors2d = plot._facecolor3d
    plot._edgecolors2d = plot._edgecolor3d
    ax.set_xlabel('Nº Células')
    ax.set_ylabel('Razão A/O')
    ax.set_zlabel('Custo (USD)')
    plt.show()

def add_extractants_dummy_columns(df: pd.DataFrame):
    extractants = df['extractant'].unique()
    for extractant in extractants:
        df[f'{extractant}_dummy'] = df['extractant'].apply(lambda x: 1 if x == extractant else 0)