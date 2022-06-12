import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter


def pareto_chart(df: pd.DataFrame) -> None:

    fig, ax = plt.subplots()

    df['absolute value'] = df['value'].abs()
    df['accumulated absolute value (%)'] = (df['absolute value'].cumsum() / df['absolute value'].sum() * 100).round(2)

    bars = ax.bar(df['name'], df['absolute value'].round(2), color = '#0066ff')
    ax.set_title('Importância das Variáveis no Custo Total de Produção')
    ax.set_xlabel('Efeitos Padronizados')
    ax.set_ylabel('Importância Absoluta')
    ax.bar_label(bars)

    ax2 = ax.twinx()
    ax2.plot(df.index, df['accumulated absolute value (%)'], color='red', marker='D', ms=7)
    ax2.axhline(80, color='orange', linestyle='dashed')
    ax2.yaxis.set_major_formatter(PercentFormatter())
    ax2.set_ylabel('Importância Absoluta Acumulada (%)')

    fig.autofmt_xdate(rotation=60)
    plt.show()