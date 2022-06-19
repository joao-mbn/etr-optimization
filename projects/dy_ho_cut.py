from helpers._common import mol_atom_from_mass_oxide
from mass_balance._distribution_ratio_models import logD_x_pH
from static_values._rees import DYSPROSIUM as DY
from static_values._rees import HOLMIUM as HO
from static_values._substances import XENOTIME
from templates._models import Project

cut = 'Dy/Ho'
distribution_ratio_model = logD_x_pH
max_cells_interval = (15, 40)
pHi_interval = (0, 1)
ao_ratio_interval = (0.5, 2)
required_raffinate_purity = 0.995
minimal_recovery = 0.15
mineral = XENOTIME
reos_of_interest_mineral_content = sum([mineral['REOS_DISTRIBUTION'][reo] for reo in ['Tb', 'Dy']])

dy_feed_aq_mols_atom = mol_atom_from_mass_oxide(3.19, DY['OXIDE_STOICHIOMETRIC_PROPORTION'], DY['OXIDE_WEIGHT'])
ho_feed_aq_mols_atom = mol_atom_from_mass_oxide(6.71, HO['OXIDE_STOICHIOMETRIC_PROPORTION'], HO['OXIDE_WEIGHT'])

project_p507_026 = Project(
    **dict(
        rees=[
            dict(symbol = 'Dy', aq_feed_concentration = dy_feed_aq_mols_atom, model_coefficients = dict(a = 3.22552, b = -0.99999)),
            dict(symbol = 'Ho', aq_feed_concentration = ho_feed_aq_mols_atom, model_coefficients = dict(a = 3.05008, b = -0.68760))
        ],
        extractant=dict(name='P507', concentration=0.26),
        cut = cut,
        distribution_ratio_model = distribution_ratio_model,
        max_cells_interval = max_cells_interval,
        pHi_interval = pHi_interval,
        ao_ratio_interval = ao_ratio_interval,
        required_raffinate_purity = required_raffinate_purity,
        minimal_recovery = minimal_recovery,
        mineral = mineral,
        reos_of_interest_mineral_content = reos_of_interest_mineral_content,
    )
)

projects = [
    project_p507_026,
]
