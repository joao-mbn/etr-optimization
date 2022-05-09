from static_values._rees import REES
from helpers._utils import value_or_default

from templates._classes import Ree


def ree_factory(wannabe_rees: list[dict]) -> list[Ree]:

    rees: list[Ree] = []

    for wannabe_ree in wannabe_rees:
        REE = next(filter(lambda REE: REE['SYMBOL'] == wannabe_ree['symbol'], REES))
        ree = Ree(wannabe_ree['aq_feed_concentration'],
                  REE['NAME'],
                  REE['SYMBOL'],
                  REE['ATOMIC_WEIGHT'],
                  REE['OXIDE_WEIGHT'],
                  stoichiometric_proportion=REE['OXIDE_STOICHIOMETRIC_PROPORTION'],
                  org_feed_concentration=value_or_default(wannabe_ree, 'org_feed_concentration', 0),
                  model_coefficients=wannabe_ree['model_coefficients'])
        rees.append(ree)

    return rees
