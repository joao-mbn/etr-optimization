import math as m

from helpers._utils import flatten
from matplotlib import pyplot as plt
from templates._classes import Ree


def isotherm_chart(rees: list[Ree]):

    fig = plt.figure()

    # Plots grid
    n_columns = 2
    n_rows = m.ceil(len(rees) / n_columns)

    for i, ree in enumerate(rees):

        # List building -----------------------------------
        operating_line_x_axis = [ree.aq_feed_concentration] + ree.cells_aq_concentrations
        operating_line_y_axis = ree.cells_org_concentrations + [ree.org_feed_concentration]

        equilibrium_line_x_axis = ree.cells_aq_concentrations
        equilibrium_line_y_axis = ree.cells_org_concentrations

        stages_x_axis = [ree.aq_feed_concentration] + flatten([2 * [aq_conc] for aq_conc in ree.cells_aq_concentrations])
        stages_y_axis = flatten([2 * [org_conc] for org_conc in ree.cells_org_concentrations]) + [ree.org_feed_concentration]

        # Plot building -----------------------------------
        position = int(f'{n_rows}{n_columns}{i + 1}')
        ax = fig.add_subplot(position)

        ax.plot(operating_line_x_axis, operating_line_y_axis, '.-', markersize = 2, label = 'Reta de Operação')
        ax.plot(equilibrium_line_x_axis, equilibrium_line_y_axis, '.-', markersize = 2, label = 'Curva de Equilíbrio')
        ax.plot(stages_x_axis, stages_y_axis, '.-', markersize = 2, label = 'Estágios')

        ax.set_xlabel('Aquoso')
        ax.set_ylabel('Orgânico')
        ax.set_ylim([0, None])
        ax.set_xlim([0, None])
        ax.legend(loc = 0)
        ax.set_title(f'Isoterma de extração de {ree.name}')

    plt.show()
