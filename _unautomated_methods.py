# Methods that aren't yet fully integrated to the workflow of data generation and visualization
import pandas as pd

from global_constants import COST_TAB, DETAILED_COST_TAB, EXCEL_FILE, ROOT_PATH
from helpers._common import (H_from_pH, g_from_mol, org_concentrations,
                             oxide_from_atom)
from mass_balance._solver import solver
from projects.nd_sm_cut import project_d2ehpa_002
from templates._classes import Proton
from visualization._compare_surfaces import compare_surfaces
from visualization._detailed_cost_chart import detailed_cost_chart
from visualization._isotherm_chart import isotherm_chart


def isotherm_wrapper():
    cost_df = pd.read_excel(f'{ROOT_PATH}{EXCEL_FILE}', COST_TAB)

    pHi, ao_ratio, n_cells = cost_df.loc[0, ['pHi', 'ao ratio', 'n cells']]
    proton = Proton(feed_concentration = H_from_pH(pHi))
    rees = project_d2ehpa_002.rees

    solver(project_d2ehpa_002.distribution_ratio_model, rees, proton, ao_ratio, n_cells)

    for ree in rees:
        ree.aq_feed_concentration = oxide_from_atom(g_from_mol(ree.aq_feed_concentration, ree.atom_molar_mass),
                                                    ree.stoichiometric_proportion, ree.atom_molar_mass, ree.oxide_molar_mass)
        ree.org_feed_concentration = oxide_from_atom(g_from_mol(ree.org_feed_concentration, ree.atom_molar_mass),
                                                    ree.stoichiometric_proportion, ree.atom_molar_mass, ree.oxide_molar_mass)

        ree.cells_aq_concentrations = [oxide_from_atom(g_from_mol(molar_aq_concentration, ree.atom_molar_mass),
                                                    ree.stoichiometric_proportion, ree.atom_molar_mass, ree.oxide_molar_mass)
                                    for molar_aq_concentration in ree.cells_aq_concentrations]

        ree.cells_org_concentrations = org_concentrations(ree.cells_aq_concentrations, ree.distribution_ratios)

    isotherm_chart(rees)


def concentration_effects_wrapper():

    concentrated_detailed_cost_df = pd.read_excel(f'{ROOT_PATH}concentrated.xlsx', DETAILED_COST_TAB)
    detailed_cost_chart(concentrated_detailed_cost_df)

    concentrated_cost_df = pd.read_excel(f'{ROOT_PATH}concentrated.xlsx', COST_TAB)
    cost_df = pd.read_excel(f'{ROOT_PATH}{EXCEL_FILE}', COST_TAB)
    cost_df_slice = cost_df.query(f'extractant == "D2EHPA" and `extractant concentration` == 0.02')
    concentrated_cost_df_slice = concentrated_cost_df.query(f'extractant == "D2EHPA" and `extractant concentration` == 0.02')
    compare_surfaces([cost_df_slice, concentrated_cost_df_slice], True)
