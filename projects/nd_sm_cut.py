from helpers._common import atom_from_oxide, mol_from_g
from mass_balance._distribution_ratio_models import logD_x_pH
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

nd_feed_aq_mols_atom = atom_from_oxide(mol_from_g(12.808, ND['OXIDE_WEIGHT']), ND['OXIDE_STOICHIOMETRIC_PROPORTION'], ND['ATOMIC_WEIGHT'], ND['OXIDE_WEIGHT'])
sm_feed_aq_mols_atom = atom_from_oxide(mol_from_g(0.923, SM['OXIDE_WEIGHT']), SM['OXIDE_STOICHIOMETRIC_PROPORTION'], SM['ATOMIC_WEIGHT'], SM['OXIDE_WEIGHT'])

project_d2ehpa_002 = Project(
    **dict(
        rees=[
            dict(symbol = 'Nd', aq_feed_concentration = nd_feed_aq_mols_atom, model_coefficients = dict(a = 1.7508, b = -4.1342)),
            dict(symbol = 'Sm', aq_feed_concentration = sm_feed_aq_mols_atom, model_coefficients = dict(a = 1.9842, b = -3.3128))
        ],
        extractant=dict(name='D2EHPA', concentration=0.02),
        cut = cut,
        distribution_ratio_model = distribution_ratio_model,
        max_cells_interval = max_cells_interval,
        pHi_interval = pHi_interval,
        ao_ratio_interval = ao_ratio_interval,
        required_raffinate_purity = required_raffinate_purity,
        minimal_recovery = minimal_recovery,
    )
)

project_d2ehpa_006 = Project(
    **dict(
        rees=[
            dict(symbol = 'Nd', aq_feed_concentration = nd_feed_aq_mols_atom, model_coefficients = dict(a = 0.8569, b = -1.9035)),
            dict(symbol = 'Sm', aq_feed_concentration = sm_feed_aq_mols_atom, model_coefficients = dict(a = 1.1924, b = -1.2654))
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
            dict(symbol = 'Nd', aq_feed_concentration = nd_feed_aq_mols_atom, model_coefficients = dict(a = 1.0539, b = -1.7022)),
            dict(symbol = 'Sm', aq_feed_concentration = sm_feed_aq_mols_atom, model_coefficients = dict(a = 1.5262, b = -1.1515))
        ],
        extractant=dict(name='D2EHPA', concentration=0.10),
        cut = cut,
        distribution_ratio_model = distribution_ratio_model,
        max_cells_interval = max_cells_interval,
        pHi_interval = pHi_interval,
        ao_ratio_interval = ao_ratio_interval,
        required_raffinate_purity = required_raffinate_purity,
        minimal_recovery = minimal_recovery,
    )
)

project_p507_002 = Project(
    **dict(
        rees=[
            dict(symbol = 'Nd', aq_feed_concentration = nd_feed_aq_mols_atom, model_coefficients = dict(a = 0.2816, b = -2.3104)),
            dict(symbol = 'Sm', aq_feed_concentration = sm_feed_aq_mols_atom, model_coefficients = dict(a = 1.6547, b = -3.7877))
        ],
        extractant=dict(name='P507', concentration=0.02),
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
            dict(symbol = 'Nd', aq_feed_concentration = nd_feed_aq_mols_atom, model_coefficients = dict(a = 1.5074, b = -3.5508)),
            dict(symbol = 'Sm', aq_feed_concentration = sm_feed_aq_mols_atom, model_coefficients = dict(a = 2.1979, b = -3.4925))
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
            dict(symbol = 'Nd', aq_feed_concentration = nd_feed_aq_mols_atom, model_coefficients = dict(a = 1.6106, b = -3.3279)),
            dict(symbol = 'Sm', aq_feed_concentration = sm_feed_aq_mols_atom, model_coefficients = dict(a = 2.213, b = -2.9758))
        ],
        extractant=dict(name='P507', concentration=0.10),
        cut = cut,
        distribution_ratio_model = distribution_ratio_model,
        max_cells_interval = max_cells_interval,
        pHi_interval = pHi_interval,
        ao_ratio_interval = ao_ratio_interval,
        required_raffinate_purity = required_raffinate_purity,
        minimal_recovery = minimal_recovery,
    )
)

project_cyanex572_002 = Project(
    **dict(
        rees=[
            dict(symbol = 'Nd', aq_feed_concentration = nd_feed_aq_mols_atom, model_coefficients = dict(a = 0.0999, b = -2.5252)),
            dict(symbol = 'Sm', aq_feed_concentration = sm_feed_aq_mols_atom, model_coefficients = dict(a = 2.8357, b = -6.6998))
        ],
        extractant=dict(name='Cyanex 572', concentration=0.02),
        cut = cut,
        distribution_ratio_model = distribution_ratio_model,
        max_cells_interval = max_cells_interval,
        pHi_interval = pHi_interval,
        ao_ratio_interval = ao_ratio_interval,
        required_raffinate_purity = required_raffinate_purity,
        minimal_recovery = minimal_recovery,
    )
)

project_cyanex572_006 = Project(
    **dict(
        rees=[
            dict(symbol = 'Nd', aq_feed_concentration = nd_feed_aq_mols_atom, model_coefficients = dict(a = 1.0167, b = -3.3632)),
            dict(symbol = 'Sm', aq_feed_concentration = sm_feed_aq_mols_atom, model_coefficients = dict(a = 2.4586, b = -4.5786))
        ],
        extractant=dict(name='Cyanex 572', concentration=0.06),
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
            dict(symbol = 'Nd', aq_feed_concentration = nd_feed_aq_mols_atom, model_coefficients = dict(a = 1.5592, b = -3.976)),
            dict(symbol = 'Sm', aq_feed_concentration = sm_feed_aq_mols_atom, model_coefficients = dict(a = 1.9341, b = -3.2532))
        ],
        extractant=dict(name='Cyanex 572', concentration=0.10),
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
    project_d2ehpa_002,
    project_d2ehpa_006,
    project_d2ehpa_010,
    project_p507_002,
    project_p507_006,
    project_p507_010,
    project_cyanex572_002,
    project_cyanex572_006,
    project_cyanex572_010,
]
