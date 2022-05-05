from _classes import Proton, Ree
from _solver import *
from charts_builder import isotherm_chart
from common import org_concentrations
from distribution_ratio_models import logD_x_pH
from constants import DYSPROSIUM as DY, HOLMIUM as HO

n_cells = 40
ao_ratio = 0.6

dysprosium = Ree(0.00855232467, DY["NAME"], DY["OXIDE_WEIGHT"], DY["SYMBOL"], model_coefficients=[3.22552, -0.99999])
holmium = Ree(0.01775799374, HO["NAME"], HO["OXIDE_WEIGHT"], HO["SYMBOL"], model_coefficients=[3.05008, -0.68760])
proton = Proton(0.55)

rees, proton = solver(logD_x_pH, [dysprosium, holmium], proton, ao_ratio=ao_ratio, n_cells=n_cells)
dysprosium, holmium = rees

dysprosium.cells_org_concentrations = org_concentrations(dysprosium.cells_aq_concentrations, dysprosium.distribution_ratios)
holmium.cells_org_concentrations = org_concentrations(holmium.cells_aq_concentrations, holmium.distribution_ratios)

isotherm_chart([dysprosium, holmium])


