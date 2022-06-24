import matplotlib.pyplot as plt
import pandas as pd
from global_constants import CHARTS_RESULTS_FOLDER_PATH

def variables_histogram(cost_df: pd.DataFrame, save_fig: bool = False) -> None:

    fig, axs = plt.subplots(2, 2, figsize=(12, 8))
    fig.text(0.04, 0.5, 'Frequência', va='center', rotation='vertical', fontsize = 14)

    cost_df['n cells'].hist(bins=14, ax = axs[0, 0], grid = False)
    cost_df['ao ratio'].hist(bins=16, ax = axs[0, 1], grid = False)
    cost_df['pHi'].hist(bins=11, ax = axs[1, 0], grid = False)
    cost_df['total cost (usd)'].hist(bins=10, ax = axs[1, 1], grid = False, color = 'red')

    axs[0, 0].set_xlabel('Nº de células')
    axs[0, 1].set_xlabel('Razão A/O')
    axs[1, 0].set_xlabel('pH inicial')
    axs[1, 1].set_xlabel('Custo total (US$)')

    plt.subplots_adjust(hspace=0.3)

    plt.show() if not save_fig else plt.savefig(f'{CHARTS_RESULTS_FOLDER_PATH}Histograma das Variáveis.png', bbox_inches='tight')