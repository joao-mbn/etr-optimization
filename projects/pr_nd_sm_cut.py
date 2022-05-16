from helpers._common import atom_from_oxide, mol_from_g
from mass_balance._distribution_ratio_models import logD_x_pH
from static_values._rees import PRASEODYMIUM as PR
from static_values._rees import NEODYMIUM as ND
from static_values._rees import SAMARIUM as SM
from templates._models import Project

cut = 'Nd/Sm'
distribution_ratio_model = logD_x_pH
max_cells_interval = (2, 10)
pHi_interval = (1, 2.5)
ao_ratio_interval = (0.5, 2)
required_raffinate_purity = 0.995
minimal_recovery = 0.15

pr_feed_aq_mols_atom = atom_from_oxide(mol_from_g(0.48, PR['OXIDE_WEIGHT']), PR['OXIDE_STOICHIOMETRIC_PROPORTION'], PR['ATOMIC_WEIGHT'], PR['OXIDE_WEIGHT'])
nd_feed_aq_mols_atom = atom_from_oxide(mol_from_g(12.808, ND['OXIDE_WEIGHT']), ND['OXIDE_STOICHIOMETRIC_PROPORTION'], ND['ATOMIC_WEIGHT'], ND['OXIDE_WEIGHT'])
sm_feed_aq_mols_atom = atom_from_oxide(mol_from_g(0.923, SM['OXIDE_WEIGHT']), SM['OXIDE_STOICHIOMETRIC_PROPORTION'], SM['ATOMIC_WEIGHT'], SM['OXIDE_WEIGHT'])

project_d2ehpa_006 = Project(
    **dict(
        rees=[
            dict(symbol = 'Pr', aq_feed_concentration = pr_feed_aq_mols_atom, model_coefficients = dict(a = 0.4026, b = -1.5661) ),
            dict(symbol = 'Nd', aq_feed_concentration = nd_feed_aq_mols_atom, model_coefficients = dict(a = 0.8569, b = -1.9035) ),
            dict(symbol = 'Sm', aq_feed_concentration = sm_feed_aq_mols_atom, model_coefficients = dict(a = 1.1924, b = -1.2654) ),
        ],
        extractant=dict(name='D2EHPA', concentration=0.06),
        cut = cut,
        distribution_ratio_model = distribution_ratio_model,
        max_cells_interval = max_cells_interval,
        pHi_interval = pHi_interval,
        ao_ratio_interval = ao_ratio_interval,
        required_raffinate_purity = required_raffinate_purity,
        minimal_recovery = minimal_recovery,
    )
)

project_d2ehpa_010 = Project(
    **dict(
        rees=[
            dict(symbol = 'Pr', aq_feed_concentration = pr_feed_aq_mols_atom, model_coefficients = dict(a = 2.84, b = -3.6807) ),
            dict(symbol = 'Nd', aq_feed_concentration = nd_feed_aq_mols_atom, model_coefficients = dict(a = 1.0539, b = -1.7022) ),
            dict(symbol = 'Sm', aq_feed_concentration = sm_feed_aq_mols_atom, model_coefficients = dict(a = 1.5262, b = -1.1515) ),
        ],
        extractant=dict(name='D2EHPA', concentration=0.1),
        cut = cut,
        distribution_ratio_model = distribution_ratio_model,
        max_cells_interval = max_cells_interval,
        pHi_interval = pHi_interval,
        ao_ratio_interval = ao_ratio_interval,
        required_raffinate_purity = required_raffinate_purity,
        minimal_recovery = minimal_recovery,
    )
)

project_p507_006 = Project(
    **dict(
        rees=[
            dict(symbol = 'Pr', aq_feed_concentration = pr_feed_aq_mols_atom, model_coefficients = dict(a = 6.5856, b = -11.441) ),
            dict(symbol = 'Nd', aq_feed_concentration = nd_feed_aq_mols_atom, model_coefficients = dict(a = 1.5074, b = -3.5508) ),
            dict(symbol = 'Sm', aq_feed_concentration = sm_feed_aq_mols_atom, model_coefficients = dict(a = 2.1979, b = -3.4924) ),
        ],
        extractant=dict(name='P507', concentration=0.06),
        cut = cut,
        distribution_ratio_model = distribution_ratio_model,
        max_cells_interval = max_cells_interval,
        pHi_interval = pHi_interval,
        ao_ratio_interval = ao_ratio_interval,
        required_raffinate_purity = required_raffinate_purity,
        minimal_recovery = minimal_recovery,
    )
)

project_p507_010 = Project(
    **dict(
        rees=[
            dict(symbol = 'Pr', aq_feed_concentration = pr_feed_aq_mols_atom, model_coefficients = dict(a = 0.7487, b = -2.3629) ),
            dict(symbol = 'Nd', aq_feed_concentration = nd_feed_aq_mols_atom, model_coefficients = dict(a = 1.6106, b = -3.3279) ),
            dict(symbol = 'Sm', aq_feed_concentration = sm_feed_aq_mols_atom, model_coefficients = dict(a = 2.213, b = -2.9758) ),
        ],
        extractant=dict(name='P507', concentration=0.1),
        cut = cut,
        distribution_ratio_model = distribution_ratio_model,
        max_cells_interval = max_cells_interval,
        pHi_interval = pHi_interval,
        ao_ratio_interval = ao_ratio_interval,
        required_raffinate_purity = required_raffinate_purity,
        minimal_recovery = minimal_recovery,
    )
)

project_cyanex572_010 = Project(
    **dict(
        rees=[
            dict(symbol = 'Pr', aq_feed_concentration = pr_feed_aq_mols_atom, model_coefficients = dict(a = 0.393, b = -2.2876) ),
            dict(symbol = 'Nd', aq_feed_concentration = nd_feed_aq_mols_atom, model_coefficients = dict(a = 1.5592, b = -3.976) ),
            dict(symbol = 'Sm', aq_feed_concentration = sm_feed_aq_mols_atom, model_coefficients = dict(a = 1.9341, b = -3.2532) ),
        ],
        extractant=dict(name='Cyanex 572', concentration=0.1),
        cut = cut,
        distribution_ratio_model = distribution_ratio_model,
        max_cells_interval = max_cells_interval,
        pHi_interval = pHi_interval,
        ao_ratio_interval = ao_ratio_interval,
        required_raffinate_purity = required_raffinate_purity,
        minimal_recovery = minimal_recovery,
    )
)

projects = [
    project_d2ehpa_006,
    project_d2ehpa_010,
    project_p507_006,
    project_p507_010,
    project_cyanex572_010,
]