from _classes import Proton, Ree
from _solver import solver
from charts_builder import isotherm_chart
from common import atom_from_oxide, mol_from_g, org_concentrations
from distribution_ratio_models import logD_x_pH
from constants import PRASEODYMIUM as PR, NEODYMIUM as ND, SAMARIUM as SM, DYSPROSIUM as DY, HOLMIUM as HO
from solve_many import solve_many

pr_feed_aq_mols_atom = atom_from_oxide(mol_from_g(0.48, PR['OXIDE_WEIGHT']), PR['OXIDE_STOICHIOMETRIC_PROPORTION'], PR['ATOMIC_WEIGHT'], PR['OXIDE_WEIGHT'])
nd_feed_aq_mols_atom = atom_from_oxide(mol_from_g(12.808, ND['OXIDE_WEIGHT']), ND['OXIDE_STOICHIOMETRIC_PROPORTION'], ND['ATOMIC_WEIGHT'], ND['OXIDE_WEIGHT'])
sm_feed_aq_mols_atom = atom_from_oxide(mol_from_g(0.923, SM['OXIDE_WEIGHT']), SM['OXIDE_STOICHIOMETRIC_PROPORTION'], SM['ATOMIC_WEIGHT'], SM['OXIDE_WEIGHT'])

praseodymium = Ree(pr_feed_aq_mols_atom, PR["NAME"], PR["OXIDE_WEIGHT"], PR["SYMBOL"], model_coefficients=[0.4026, -1.5661])
neodymium = Ree(nd_feed_aq_mols_atom, ND["NAME"], ND["OXIDE_WEIGHT"], ND["SYMBOL"], model_coefficients=[0.8569, -1.9035])
samarium = Ree(sm_feed_aq_mols_atom, SM["NAME"], SM["OXIDE_WEIGHT"], SM["SYMBOL"], model_coefficients=[1.1924, -1.2654])
proton = Proton(0.01)

n_cells = 5
ao_ratio = 2

summary, approved = solve_many('Nd/Sm', logD_x_pH, [praseodymium, neodymium, samarium], proton, (2, 7), (1, 2), (0.5, 2), 0.99)

# rees, proton = solver(logD_x_pH, [praseodymium, neodymium, samarium], proton, ao_ratio=ao_ratio, n_cells=n_cells)
# praseodymium, neodymium, samarium = rees

# praseodymium.cells_org_concentrations = org_concentrations(praseodymium.cells_aq_concentrations, praseodymium.distribution_ratios)
# neodymium.cells_org_concentrations = org_concentrations(neodymium.cells_aq_concentrations, neodymium.distribution_ratios)
# samarium.cells_org_concentrations = org_concentrations(samarium.cells_aq_concentrations, samarium.distribution_ratios)

#isotherm_chart([praseodymium, neodymium, samarium])

# data, approved = solve_many('Dy/Ho', logD_x_pH, [dysprosium, holmium], proton, (30, 40), (0, 1), (0.5, 2), 0.98)
# dysprosium = Ree(0.00855232467, DY["NAME"], DY["OXIDE_WEIGHT"], DY["SYMBOL"], model_coefficients=[3.22552, -0.99999])
# holmium = Ree(0.01775799374, HO["NAME"], HO["OXIDE_WEIGHT"], HO["SYMBOL"], model_coefficients=[3.05008, -0.68760])

