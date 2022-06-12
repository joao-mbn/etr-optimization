import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from visualization._excel import save_to_existing_excel
from helpers._common import create_sub_dataframe


def get_regression(df: pd.DataFrame, degree: int = 3,
                   dependent_variable_substring: str = 'cost',
                   independent_variables_substrings: list[str] = ['pHi', 'ao ratio', 'cell']) -> LinearRegression:

    regression, _, _ = regression_aggregate(df, dependent_variable_substring, independent_variables_substrings, degree)
    return regression


def predict(regression: LinearRegression, features: pd.DataFrame, grid_shape, degree: int = 3) -> LinearRegression:
    return regression.predict(PolynomialFeatures(degree = degree).fit_transform(features)).reshape(grid_shape)


def get_regression_coefficients_table(df: pd.DataFrame, degree: int = 3,
                                      dependent_variable_substring: str = 'cost',
                                      independent_variables_substrings: list[str] = ['pHi', 'ao ratio', 'cell']) -> pd.DataFrame:

    regression, fitted_independent_variables, _ = regression_aggregate(df, dependent_variable_substring, independent_variables_substrings, degree)
    coefficients_table = link_coefficients_values_to_feature_names(regression, fitted_independent_variables.get_feature_names_out())
    return coefficients_table


def save_regression_to_excel(df: pd.DataFrame, degree: int = 3,
                             dependent_variable_substring: str = 'cost',
                             independent_variables_substrings: list[str] = ['pHi', 'ao ratio', 'cell']) -> None:

    regression, fitted_independent_variables, transformed_independent_variables = regression_aggregate(df, dependent_variable_substring,
                                                                                                       independent_variables_substrings, degree)
    coefficients_names = fitted_independent_variables.get_feature_names_out()
    coefficients_table = link_coefficients_values_to_feature_names(regression, coefficients_names)
    transformed_data = pd.DataFrame(data = transformed_independent_variables, columns = coefficients_names)

    save_to_existing_excel([
        {'df': transformed_data, 'name': 'Valores Transformados Regressão'},
        {'df': coefficients_table, 'name': 'Coeficientes da Regressão'}
    ])


def regression_aggregate(df: pd.DataFrame, dependent_variable_substring: str, independent_variables_substrings: list[str],
                         degree: int) -> tuple[LinearRegression, PolynomialFeatures, np.ndarray]:

    independent_variables_df = create_sub_dataframe(df, white_list_substrings = independent_variables_substrings)
    dependent_variable_df = create_sub_dataframe(df, white_list_substrings = [dependent_variable_substring])

    fitted_independent_variables = PolynomialFeatures(degree = degree).fit(independent_variables_df)
    transformed_independent_variables = fitted_independent_variables.transform(independent_variables_df)

    regression = LinearRegression()
    regression.fit(transformed_independent_variables, dependent_variable_df)

    return regression, fitted_independent_variables, transformed_independent_variables


def get_columns_of_interest(df: pd.DataFrame, dependent_variable_substring: str,
                            independent_variables_substrings: list[str]) -> tuple[str, list[str]]:
    columns = df.columns.values.tolist()
    dependent_variable_column = next(column for column in columns if dependent_variable_substring in column)
    independent_variables_columns = [column for column in columns if any(match in column for match in independent_variables_substrings)]

    return dependent_variable_column, independent_variables_columns


def link_coefficients_values_to_feature_names(regression: LinearRegression, coefficients_names: np.ndarray) -> pd.DataFrame:
    coefficients = pd.DataFrame(data = zip(coefficients_names, regression.coef_), columns = ['name', 'value'])
    coefficients.drop(0, inplace = True) # Drop linear coefficient
    coefficients.sort_values(by = 'value', ascending = False, key = abs, inplace = True)

    return coefficients




