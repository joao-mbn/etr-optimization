from typing import Any
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from visualization._excel import save_to_existing_excel
from helpers._common import create_sub_dataframe
import statsmodels.api as sm
from global_constants import MODEL_DEGREE, INTERACTION_ONLY


def get_regression(df: pd.DataFrame, degree: int = MODEL_DEGREE, dependent_variable_substring: str = 'cost',
                   independent_variables_substrings: list[str] = ['pHi', 'ao ratio', 'cell'],
                   get_score = False, interaction_only: bool = INTERACTION_ONLY) -> tuple[LinearRegression, float] | LinearRegression:

    regression, _, _, score = regression_aggregate(df, dependent_variable_substring, independent_variables_substrings, degree, interaction_only)
    return (regression, score) if get_score else regression


def predict(regression: LinearRegression, features: pd.DataFrame, grid_shape, degree: int = MODEL_DEGREE, interaction_only: bool = INTERACTION_ONLY) -> LinearRegression:
    return regression.predict(PolynomialFeatures(degree = degree, include_bias = False, interaction_only = interaction_only).fit_transform(features)).reshape(grid_shape)


def get_regression_coefficients_table(df: pd.DataFrame, degree: int = MODEL_DEGREE,
                                      dependent_variable_substring: str = 'cost',
                                      independent_variables_substrings: list[str] = ['pHi', 'ao ratio', 'cell'],
                                      interaction_only: bool = INTERACTION_ONLY) -> pd.DataFrame:

    regression, fitted_independent_variables, _, _ = regression_aggregate(df, dependent_variable_substring, independent_variables_substrings, degree, interaction_only)
    coefficients_table = link_coefficients_values_to_feature_names(regression, fitted_independent_variables.get_feature_names_out())
    return coefficients_table


def get_complete_regression_coefficients_table(dependent_variable: pd.DataFrame, independent_variables: pd.DataFrame,
                                               degree: int = MODEL_DEGREE, interaction_only: bool = INTERACTION_ONLY, print_summary: bool = True) -> tuple[Any, np.ndarray]:

    fitted_independent_variables = PolynomialFeatures(degree = degree, interaction_only = interaction_only).fit(independent_variables)
    coefficients_names = fitted_independent_variables.get_feature_names_out()
    transformed_independent_variables = fitted_independent_variables.transform(independent_variables)
    transformed_independent_variables = pd.DataFrame(data = transformed_independent_variables, columns = coefficients_names)

    dependent_variable.reset_index(drop = True, inplace = True)
    regression = sm.OLS(dependent_variable, transformed_independent_variables).fit()

    if print_summary:
        print(regression.summary(xname = coefficients_names.tolist()))

    return regression, coefficients_names


def save_regression_to_excel(df: pd.DataFrame, degree: int = MODEL_DEGREE,
                             dependent_variable_substring: str = 'cost',
                             independent_variables_substrings: list[str] = ['pHi', 'ao ratio', 'cell'],
                             interaction_only: bool = INTERACTION_ONLY) -> None:

    regression, fitted_independent_variables, transformed_independent_variables, _ = regression_aggregate(df, dependent_variable_substring,
                                                                                                          independent_variables_substrings, degree, interaction_only)
    coefficients_names = fitted_independent_variables.get_feature_names_out()
    coefficients_table = link_coefficients_values_to_feature_names(regression, coefficients_names)
    transformed_data = pd.DataFrame(data = transformed_independent_variables, columns = coefficients_names)

    save_to_existing_excel([
        {'df': transformed_data, 'name': 'Valores Transformados Regress??o'},
        {'df': coefficients_table, 'name': 'Coeficientes da Regress??o'}
    ])


def regression_aggregate(df: pd.DataFrame, dependent_variable_substring: str, independent_variables_substrings: list[str],
                         degree: int, interaction_only: bool) -> tuple[LinearRegression, PolynomialFeatures, np.ndarray, float]:

    independent_variables_df = create_sub_dataframe(df, white_list_substrings = independent_variables_substrings)
    dependent_variable_df = create_sub_dataframe(df, white_list_substrings = [dependent_variable_substring])

    fitted_independent_variables = PolynomialFeatures(degree = degree, include_bias = False, interaction_only = interaction_only).fit(independent_variables_df)
    transformed_independent_variables = fitted_independent_variables.transform(independent_variables_df)

    regression = LinearRegression().fit(transformed_independent_variables, dependent_variable_df)
    score: float = regression.score(transformed_independent_variables, dependent_variable_df)

    return regression, fitted_independent_variables, transformed_independent_variables, score


def get_columns_of_interest(df: pd.DataFrame, dependent_variable_substring: str,
                            independent_variables_substrings: list[str]) -> tuple[str, list[str]]:
    columns = df.columns.values.tolist()
    dependent_variable_column = next(column for column in columns if dependent_variable_substring in column)
    independent_variables_columns = [column for column in columns if any(match in column for match in independent_variables_substrings)]

    return dependent_variable_column, independent_variables_columns


def link_coefficients_values_to_feature_names(regression: LinearRegression, coefficients_names: np.ndarray) -> pd.DataFrame:
    coefficients = pd.DataFrame(data = zip(coefficients_names, regression.coef_.ravel()), columns = ['name', 'value'])
    coefficients.sort_values(by = 'value', ascending = False, key = abs, inplace = True)

    return coefficients




