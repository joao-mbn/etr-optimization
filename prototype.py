from helpers._common import atom_from_oxide, mol_from_g, org_concentrations
from mass_balance._distribution_ratio_models import logD_x_pH
from mass_balance._solve_many import solve_many
from mass_balance._solver import solver
from static_values._rees import DYSPROSIUM as DY
from static_values._rees import HOLMIUM as HO
from static_values._rees import NEODYMIUM as ND
from static_values._rees import PRASEODYMIUM as PR
from static_values._rees import SAMARIUM as SM
from templates._classes import Proton, Ree
from templates._factories import rees_factory
from visualization._isotherm_chart import isotherm_chart
from visualization._approveds_plot import cost_relationship_curve
from templates._models import Project
from _main import main
from projects.nd_sm_cut import projects

# main(projects)
cost_relationship_curve()

# Limpar o código

# p507 = dict(name='P507', concentration=0.1)

# rees = rees_factory([pr, nd, sm])
# rees.sort(key=lambda ree: ree.atom_molar_mass)

# summary, approved = solve_many(cut, logD_x_pH, rees, Proton(), max_cells_interval,
#                                pHi_interval, ao_ratio_interval, required_raffinate_purity)

# solver(logD_x_pH, rees, Proton(0.01), ao_ratio=2, n_cells=2)
# praseodymium, neodymium, samarium = rees

# praseodymium.cells_org_concentrations = org_concentrations(praseodymium.cells_aq_concentrations, praseodymium.distribution_ratios)
# neodymium.cells_org_concentrations = org_concentrations(neodymium.cells_aq_concentrations, neodymium.distribution_ratios)
# samarium.cells_org_concentrations = org_concentrations(samarium.cells_aq_concentrations, samarium.distribution_ratios)

# isotherm_chart([praseodymium, neodymium, samarium])

# data, approved = solve_many('Dy/Ho', logD_x_pH, [dysprosium, holmium], proton, (30, 40), (0, 1), (0.5, 2), 0.98)
# dysprosium = Ree(0.00855232467, DY["NAME"], DY["OXIDE_WEIGHT"], DY["SYMBOL"], model_coefficients=[3.22552, -0.99999])
# holmium = Ree(0.01775799374, HO["NAME"], HO["OXIDE_WEIGHT"], HO["SYMBOL"], model_coefficients=[3.05008, -0.68760])

