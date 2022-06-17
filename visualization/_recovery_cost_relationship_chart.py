import pandas as pd
from global_constants import CHARTS_RESULTS_FOLDER_PATH, FONT
import matplotlib.pyplot as plt
from visualization._regression import get_regression, predict
import numpy as np
from matplotlib.ticker import PercentFormatter, StrMethodFormatter


def recovery_cost_relationship_chart(df: pd.DataFrame, save_fig: bool = False):

    new_df = df[['recovery', 'total cost (usd)']].copy()
    new_df['recovery'] = (new_df['recovery'] * 100).round(2)
    new_df['recovery^-1'] = 1 / new_df['recovery']

    degree = 1
    regression, score = get_regression(new_df, degree, 'total cost (usd)', ['recovery^-1'], True)
    recovery_samples = np.linspace(15, 98, 100)
    predicted_costs = predict(regression, (recovery_samples ** -1).reshape(-1, 1), recovery_samples.shape, degree)

    plt.figure(figsize=(10, 6))
    plt.plot(new_df['recovery'], new_df['total cost (usd)'], 'o', markersize = 1, color = 'blue')
    plt.plot(recovery_samples, predicted_costs, '-', linewidth = 3, color = 'red')

    plt.xlabel('Recuperação (%)')
    plt.ylabel('Custo total (USD)')
    plt.text(70, 4e6, r'$y = a \cdot x^{-1}$ + b', fontdict = FONT)
    plt.text(70, 3.7e6, f'R² = {score:.2f}', fontdict = FONT)
    plt.gca().xaxis.set_major_formatter(PercentFormatter())
    plt.gca().yaxis.set_major_formatter(StrMethodFormatter('${x:,.0f}'))

    plt.show() if not save_fig else plt.savefig(f'{CHARTS_RESULTS_FOLDER_PATH}Recuperação-Custo.png', bbox_inches='tight')