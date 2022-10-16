import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from global_constants import CHARTS_RESULTS_FOLDER_PATH, FONT
from matplotlib.ticker import PercentFormatter, StrMethodFormatter

from visualization._regression import get_regression, predict


def recovery_cost_relationship_chart(df: pd.DataFrame, save_fig: bool = False):

    new_df = df[['recovery', 'total cost (usd)']].copy()
    new_df['recovery^-1'] = 1 / new_df['recovery']
    new_df['total cost (usd)'] = new_df['total cost (usd)'] / 10000

    degree = 1
    regression, score = get_regression(new_df, degree, 'total cost (usd)', ['recovery^-1'], True)
    recovery_samples = np.linspace(0.4, 0.98, 100)
    predicted_costs = predict(regression, (recovery_samples ** -1).reshape(-1, 1), recovery_samples.shape, degree)

    plt.figure(figsize=(10, 6))
    plt.plot((new_df['recovery'] * 100).round(2), new_df['total cost (usd)'], 'o', markersize = 1, color = 'blue')
    plt.plot((recovery_samples * 100).round(2), predicted_costs, '-', linewidth = 3, color = 'red')

    plt.xlabel('Recuperação (%)', fontsize = 16)
    plt.ylabel('Custo total (USD/Kg)', fontsize = 16)
    plt.text(new_df['recovery'].max() * 70, new_df['total cost (usd)'].max() * 0.9,
             f'y = {regression.coef_[0][0]:.2f}' + r'$ \cdot x^{-1}$ +' + f'{regression.intercept_[0]:.2f}', fontdict = FONT)
    plt.text(new_df['recovery'].max() * 70, new_df['total cost (usd)'].max() * 0.85, f'R² = {score:.2f}', fontdict = FONT)
    plt.gca().xaxis.set_major_formatter(PercentFormatter())
    plt.gca().yaxis.set_major_formatter(StrMethodFormatter('${x:,.0f}'))

    plt.show() if not save_fig else plt.savefig(f'{CHARTS_RESULTS_FOLDER_PATH}Recuperação-Custo.png', bbox_inches='tight')
