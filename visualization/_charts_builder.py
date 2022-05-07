import math as m

from matplotlib import pyplot as plt

from helpers._utils import flatten
from templates._classes import Ree


def isotherm_chart(rees: list[Ree]):

    fig = plt.figure()

    # Plots grid
    n_colums = 2
    n_rows = m.ceil(len(rees) / n_colums)

    for i, ree in enumerate(rees):

        # List building -----------------------------------
        operating_line_x_axis = [ree.aq_feed_concentration] + ree.cells_aq_concentrations
        operating_line_y_axis = ree.cells_org_concentrations + [ree.org_feed_concentration]

        equilibrium_line_x_axis = ree.cells_aq_concentrations
        equilibrium_line_y_axis = ree.cells_org_concentrations

        stages_x_axis = [ree.aq_feed_concentration] + flatten([2 * [aq_conc] for aq_conc in ree.cells_aq_concentrations])
        stages_y_axis = flatten([2 * [org_conc] for org_conc in ree.cells_org_concentrations]) + [ree.org_feed_concentration]

        # Plot building -----------------------------------
        position = int('{0}{1}{2}'.format(n_rows, n_colums, i + 1))
        axes = fig.add_subplot(position)

        axes.plot(operating_line_x_axis, operating_line_y_axis, '.-', markersize = 2, label = 'Reta de Operação')
        axes.plot(equilibrium_line_x_axis, equilibrium_line_y_axis, '.-', markersize = 2, label = 'Curva de Equilíbrio')
        axes.plot(stages_x_axis, stages_y_axis, '.-', markersize = 2, label = 'Estágios')

        axes.set_xlabel('Aquoso')
        axes.set_ylabel('Orgânico')
        axes.set_ylim([0, None])
        axes.set_xlim([0, None])
        axes.legend(loc = 0)
        axes.set_title('Isoterma de extração de {0}'.format(ree.name))

    plt.show()