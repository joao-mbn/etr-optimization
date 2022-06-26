import math as m

from global_constants import CHARTS_RESULTS_FOLDER_PATH
from helpers._utils import flatten
from matplotlib import pyplot as plt
from templates._classes import Ree


def isotherm_chart(rees: list[Ree], save_fig: bool = False):


    # Plots grid
    n_columns = 2
    n_rows = m.ceil(len(rees) / n_columns)

    fig = plt.figure(figsize = (6 * n_columns, 6 * n_rows))

    for i, ree in enumerate(rees):

        operating_line_x_axis = [ree.aq_feed_concentration] + ree.cells_aq_concentrations
        operating_line_y_axis = ree.cells_org_concentrations + [ree.org_feed_concentration]

        equilibrium_line_x_axis = ree.cells_aq_concentrations
        equilibrium_line_y_axis = ree.cells_org_concentrations

        stages_x_axis = [ree.aq_feed_concentration] + flatten([2 * [aq_conc] for aq_conc in ree.cells_aq_concentrations])
        stages_y_axis = flatten([2 * [org_conc] for org_conc in ree.cells_org_concentrations]) + [ree.org_feed_concentration]

        position = int(f'{n_rows}{n_columns}{i + 1}')
        ax = fig.add_subplot(position)

        ax.plot(operating_line_x_axis, operating_line_y_axis, '.-', markersize = 2, label = 'Reta de Operação')
        ax.plot(equilibrium_line_x_axis, equilibrium_line_y_axis, '.-', markersize = 2, label = 'Curva de Equilíbrio')
        ax.plot(stages_x_axis, stages_y_axis, '.-', markersize = 2, label = 'Estágios')

        average_y_step = (max(operating_line_y_axis) - min(operating_line_y_axis)) / len(operating_line_y_axis)
        average_x_step = (max(operating_line_x_axis) - min(operating_line_x_axis)) / len(operating_line_x_axis)

        ax.set_xlabel('Concentração na Fase Aquosa (g/L)')
        ax.set_ylabel('Concentração na Fase Orgânica (g/L)')
        ax.set_ylim([0, max(operating_line_y_axis) + average_y_step])
        ax.set_xlim([min(operating_line_x_axis) - average_x_step, max(operating_line_x_axis) + average_x_step])
        ax.grid(True)
        ax.legend(loc = 0)
        ax.set_title(f'Isoterma de extração de {ree.name}')

    plt.show() if not save_fig else plt.savefig(f'{CHARTS_RESULTS_FOLDER_PATH}Isoterma.png', bbox_inches='tight')
