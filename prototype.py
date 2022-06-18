
import pandas as pd
import statsmodels.api as sm
from sklearn.preprocessing import PolynomialFeatures

from _generate_charts import generate_charts
from _generate_data import calculate
from global_constants import (COMPLETE_RESULTS_TAB, COST_TAB,
                              DETAILED_COST_TAB, EXCEL_FILE, ROOT_PATH,
                              STANDARDIZED_COST_TAB)
from helpers._common import atom_from_oxide, mol_from_g
from helpers._utils import standardize
from mass_balance._distribution_ratio_models import logD_x_pH
from projects.nd_sm_cut import projects, project_d2ehpa_002
from static_values._rees import NEODYMIUM as ND
from static_values._rees import SAMARIUM as SM
from static_values._substances import MONAZITE
from templates._models import Project
from visualization._compare_surfaces import compare_surfaces
from visualization._detailed_cost_chart import detailed_cost_chart
from visualization._pareto_chart import (
    get_regression_comprehensive_coefficients_table, pareto_chart)
from visualization._recovery_cost_relationship_chart import \
    recovery_cost_relationship_chart
from visualization._regression import get_regression_coefficients_table
from mass_balance._solver import solver
from templates._classes import Proton
from helpers._common import H_from_pH, org_concentrations, oxide_from_atom, g_from_mol
from visualization._isotherm_chart import isotherm_chart
from _unautomated_methods import isotherm_wrapper, concentration_effects_wrapper


""" calculate(projects)
generate_charts(True) """

# isotherm_wrapper()
concentration_effects_wrapper()



