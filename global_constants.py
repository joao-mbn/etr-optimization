ROOT_PATH = 'C:/Users/joao.batista/Desktop/My Repos/etr-optimization/'
CHARTS_RESULTS_FOLDER_PATH = ROOT_PATH + 'charts_results/'
PARETO_FOLDER = CHARTS_RESULTS_FOLDER_PATH + 'pareto/'
TRI_SURFACES_FOLDER = CHARTS_RESULTS_FOLDER_PATH + 'tri_surfaces/'
COST_SURFACES = CHARTS_RESULTS_FOLDER_PATH + 'cost_surfaces/'

APPROVEDS_ONLY_EXCEL = 'aprovados sem extrapolação.xlsx'
ALL_CONDITIONS_EXCEL = 'aprovados e reprovados sem extrapolação sem valores absurdos.xlsx'
CONCENTRATED_FEED_EXCEL = 'simulação alimentação concentrada.xlsx'


COST_TAB = 'Custos'
DETAILED_COST_TAB = 'Custos Detalhados'
STANDARDIZED_COST_TAB = 'Custos Padronizados'
COST_PIVOT_TABLE_TAB = 'Tabela Pivô de Custos'
PROCESS_RESULTS_TAB = 'Resultados do Processo'
COMPLETE_RESULTS_TAB = 'Resultados Completos'
TRANSFORMED_REGRESSION_VALUES_TAB = 'Valores Transformados Regressão'
REGRESSION_COEFFICIENTS_TAB = 'Coeficientes da Regressão'


FONT = {
    'family': 'serif',
    'color':  'darkred',
    'weight': 'normal',
    'size': 14,
}


MAX_P_VALUE = 0.05 # Alpha value for statistical significance
CONFIDENCE_LEVEL_VALUE_95 = 1.960 # Z for 95% confidence level
MODEL_DEGREE = 2
INTERACTION_ONLY = True
