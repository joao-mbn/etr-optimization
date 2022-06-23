import matplotlib.pyplot as plt
import pandas as pd
from global_constants import CHARTS_RESULTS_FOLDER_PATH, MAX_P_VALUE
from matplotlib.ticker import PercentFormatter
from numpy import ndarray

from visualization._regression import get_complete_regression_coefficients_table


def pareto_chart(coefficients_df: pd.DataFrame, save_fig: bool = False, extractant_name: str = '', extractant_concentration: int = 0) -> None:

    fig, ax = plt.subplots(figsize=(16, 10))

    bars = ax.bar(coefficients_df['name'], coefficients_df['absolute value (%)'], color = '#6ddbfc')
    ax.set_title('Importância das Variáveis no Custo Total de Produção')
    ax.yaxis.set_major_formatter(PercentFormatter())
    ax.set_xlabel('Efeitos Padronizados')
    ax.set_ylabel('Importância Absoluta (%)')
    ax.bar_label(bars, labels = coefficients_df['value (%)'].apply(lambda x: f'{x:.0f}%'), label_type = 'center')

    _, caps, _ = plt.errorbar(coefficients_df['name'], coefficients_df['absolute value (%)'], yerr = coefficients_df['std error (%)'],
                 ecolor = 'black', ls = 'none', capsize = 5)
    _ = [cap.set_marker('_') for cap in caps]
    _ = [cap.set_markeredgewidth(1) for cap in caps]

    ax2 = ax.twinx()
    ax2.plot(coefficients_df['name'], coefficients_df['accumulated absolute value (%)'], color='red', marker='D', ms=7)
    ax2.axhline(80, color = 'orange', linestyle = 'dashed')
    ax2.yaxis.set_major_formatter(PercentFormatter())
    ax2.set_ylabel('Importância Absoluta Acumulada (%)')

    fig.autofmt_xdate(rotation=60)
    plt.show() if not save_fig else plt.savefig(f'{CHARTS_RESULTS_FOLDER_PATH}Pareto {extractant_name} {round(extractant_concentration * 100)}%.png',
                                                bbox_inches='tight')


def get_regression_comprehensive_coefficients_table(standardized_df: pd.DataFrame) -> pd.DataFrame:

    df_slice_copy = standardized_df.copy()
    df_slice_copy.columns = df_slice_copy.columns.str.replace(' ', '_')

    dependent_variable = df_slice_copy['total_cost']
    independent_variables = df_slice_copy[df_slice_copy.columns.difference(['total_cost', 'extractant', 'extractant_concentration'])]

    remove_invariants_from_independent_variables(independent_variables)

    regression, coefficients_names = get_complete_regression_coefficients_table(dependent_variable, independent_variables)

    coefficients_df = create_coefficients_df_from_regression(regression, coefficients_names)

    rank_importance(coefficients_df)
    add_values_relative_to_aggregate(coefficients_df)
    format_values_to_improve_readability(coefficients_df)

    return coefficients_df


def remove_invariants_from_independent_variables(independent_variables: pd.DataFrame) -> None:
    invariant_columns = independent_variables.columns[independent_variables.apply(lambda col: len(col.unique()) == 1)]
    independent_variables.drop(invariant_columns, axis=1, inplace = True)


def create_coefficients_df_from_regression(regression: pd.DataFrame, coefficients_names: ndarray) -> pd.DataFrame:
    return pd.DataFrame(data = { 'name': coefficients_names,
                                 'absolute value': regression.params.abs(),
                                 'value': regression.params,
                                 'p-value': regression.pvalues,
                                 'std error': regression.bse })


def add_values_relative_to_aggregate(coefficients_df: pd.DataFrame) -> None:
    coefficients_df['value (%)'] = (coefficients_df['value'] * 100 / coefficients_df['absolute value'].sum())
    coefficients_df['absolute value (%)'] = coefficients_df['value (%)'].abs()
    coefficients_df['accumulated absolute value (%)'] = (coefficients_df['absolute value (%)'].cumsum() * 100 / coefficients_df['absolute value (%)'].sum())
    coefficients_df['std error (%)'] = (coefficients_df['std error'] / coefficients_df['absolute value'] * coefficients_df['absolute value (%)'])


def rank_importance(coefficients_df: pd.DataFrame) -> None:
    # Remove coefficients with high chance of being produced by random error
    coefficients_df.query(f'`p-value` < {MAX_P_VALUE}', inplace = True)
    coefficients_df.sort_values('absolute value', ascending = False, inplace = True)
    coefficients_df.drop(coefficients_df[coefficients_df['name'] == '1'].index, inplace=True)


def format_values_to_improve_readability(coefficients_df: pd.DataFrame) -> None:
    # That will display better in X axis label of bar chart, making it clear to show variables interactions
    coefficients_df['name'] = coefficients_df['name'].apply(lambda name: name.replace(' ', ' * '))
    # That will remove the lesser bars that might polute the chart with a long tail to the right
    coefficients_df.drop(coefficients_df[coefficients_df['absolute value (%)'] < 1].index, inplace=True)
