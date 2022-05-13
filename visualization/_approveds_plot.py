import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from templates._models import Condition
from helpers._common import transform_conditions_to_dataframe

def cost_relationship_curve(conditions: list[Condition] | None):

    # Choose data source
    if conditions:
        df = transform_conditions_to_dataframe(conditions)
    else:
        df = pd.read_excel('C:/Users/joao.batista/Desktop/aprovados.xlsx', 'Condições Aprovadas')

    # Extract independent and dependent variables from dataframe through column matching
    columns = df.columns.values.tolist()
    cost_column = next(column for column in columns if 'cost' in column)
    phi_column = next(column for column in columns if 'pHi' in column)
    ao_ratio_column = next(column for column in columns if 'ratio' in column)
    n_cells_column = next(column for column in columns if 'cell' in column)

    cost = df[cost_column].values
    independent_variables = df[[n_cells_column, ao_ratio_column, phi_column]].values

    # Create a cubic model on polynomial regression
    independent_variables_ = PolynomialFeatures(degree = 3, include_bias = False).fit_transform(independent_variables)
    regression = LinearRegression()
    regression.fit(independent_variables_, cost)
    intercept, coefficients = regression.intercept_, regression.coef_

    # Generates layers of smooth curves using the model, on a valid area of investigation.
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    for pHi in np.linspace(1, 2, 6):
        n_cells, ao_ratio = np.meshgrid(np.arange(2, 11, 1), np.linspace(0.5, 2.0, 21))
        cost = curves_model(intercept, coefficients, (n_cells, ao_ratio), pHi)

        plot = ax.plot_surface(n_cells, ao_ratio, cost,
                               rstride = 4, cstride = 4, alpha = 0.5,
                               label = f'pHi = {round(pHi, 3)}')

        plot._facecolors2d = plot._facecolor3d
        plot._edgecolors2d = plot._edgecolor3d

    ax.scatter(df[n_cells_column].values, df[ao_ratio_column].values, df[cost_column].values, color = 'r', s = 2)

    ax.set_xlabel('Nº Células')
    ax.set_ylabel('Razão A/O')
    ax.set_zlabel('Custo (USD)')
    plt.legend(loc='lower center', bbox_to_anchor=(0.5, 1),
               ncol=3, fancybox=True, shadow=True)
    plt.show()

def curves_model(intercept, coefficients, moving_independent_variables, fixed_independent_variable):
    x1, x2 = moving_independent_variables
    x3 = fixed_independent_variable

    return intercept                                                                                           + \
           coefficients[0]  * x1           + coefficients[1]  * x2           + coefficients[2]  * x3           + \
           coefficients[3]  * x1 ** 2      + coefficients[4]  * x1 * x2      + coefficients[5]  * x1 * x3      + \
           coefficients[6]  * x2 ** 2      + coefficients[7]  * x2 * x3      + coefficients[8]  * x3 ** 2      + \
           coefficients[9]  * x1 ** 3      + coefficients[10] * x1 ** 2 * x2 + coefficients[11] * x1 ** 2 * x3 + \
           coefficients[12] * x1 * x2 ** 2 + coefficients[13] * x1 * x2 * x3 + coefficients[14] * x1 * x3 ** 2 + \
           coefficients[15] * x2 ** 3      + coefficients[16] * x2 ** 2 * x3 + coefficients[17] * x2 * x3 ** 2 + \
           coefficients[18] * x3 ** 3
