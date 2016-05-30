import pandas as pd


class CostsManagerBase(object):
    def __init__(self, exo_info, costs_context):
        self.exo_info = exo_info
        self.context = costs_context

    def get_costs(self, price):
        """
        Returns transactions costs vector for EXO
        :param price:
        :return:
        """
        return pd.Series(0, index=price.index)


class CostsManagerEXOFixed(CostsManagerBase):
    def calc_costs_per_side(self, options_costs, futures_costs):
        """
        Calculates costs per one EXO unit
        """
        pcf = self.exo_info['pcf']
        pcfqty = self.exo_info['pcfqty']

        costs = 0.0

        for i, c in enumerate(pcf):
            if c == 2:  # Futures contract
                costs += abs(pcfqty[i] * futures_costs)
            elif c == 0:  # Call contract
                costs += abs(pcfqty[i] * options_costs)
            elif c == 1:  # Put contract
                costs += abs(pcfqty[i] * options_costs)
            else:
                # Unexpected error
                raise ValueError("Unexpected contact type: {0}".format(c))

        return costs

    def get_costs(self, price):
        """
        Returns transactions costs vector for EXO
        :param price:
        :return:
        """
        cost_context = self.context['costs']

        if 'context' in cost_context:
            if 'costs_options' not in cost_context['context']:
                raise ValueError("'costs_options' missing in costs settings['context']")
            if 'costs_futures' not in cost_context['context']:
                raise ValueError("'costs_futures' missing in costs settings['context']")

            costs_value = self.calc_costs_per_side(cost_context['context']['costs_options'], cost_context['context']['costs_futures'])
            return pd.Series(costs_value, index=price.index)
        else:
            raise ValueError("'context' missing in costs settings")



