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
from projects import projects

main(projects)
# cost_relationship_curve()

# Limpar o código

# pr_feed_aq_mols_atom = atom_from_oxide(mol_from_g(0.48, PR['OXIDE_WEIGHT']), PR['OXIDE_STOICHIOMETRIC_PROPORTION'], PR['ATOMIC_WEIGHT'], PR['OXIDE_WEIGHT'])
# nd_feed_aq_mols_atom = atom_from_oxide(mol_from_g(12.808, ND['OXIDE_WEIGHT']), ND['OXIDE_STOICHIOMETRIC_PROPORTION'], ND['ATOMIC_WEIGHT'], ND['OXIDE_WEIGHT'])
# sm_feed_aq_mols_atom = atom_from_oxide(mol_from_g(0.923, SM['OXIDE_WEIGHT']), SM['OXIDE_STOICHIOMETRIC_PROPORTION'], SM['ATOMIC_WEIGHT'], SM['OXIDE_WEIGHT'])

# pr = dict(symbol = 'Pr', aq_feed_concentration = pr_feed_aq_mols_atom, model_coefficients = dict(a = 0.4026, b = -1.5661) )
# nd = dict(symbol = 'Nd', aq_feed_concentration = nd_feed_aq_mols_atom, model_coefficients = dict(a = 0.8569, b = -1.9035) )
# sm = dict(symbol = 'Sm', aq_feed_concentration = sm_feed_aq_mols_atom, model_coefficients = dict(a = 1.1924, b = -1.2654) )

# p507 = dict(name='P507', concentration=0.1)

# cut = 'Nd/Sm'
# distribution_ratio_model = logD_x_pH
# max_cells_interval = (2, 10)
# pHi_interval = (1, 2)
# ao_ratio_interval = (0.5, 2)
# required_raffinate_purity = 0.995

# project = Project(
#     **dict(
#         rees = [pr, nd, sm],
#         extractant = p507,
#         cut = cut,
#         distribution_ratio_model = distribution_ratio_model,
#         max_cells_interval = max_cells_interval,
#         pHi_interval = pHi_interval,
#         ao_ratio_interval = ao_ratio_interval,
#         required_raffinate_purity = required_raffinate_purity,
#     )
# )

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

