import pandas as pd


class CostsManagerBase(object):
    def __init__(self, exo_info, costs_context):
        self.exo_info = exo_info
        self.context = costs_context

    def get_costs(self, exo_df):
        """
        Returns transactions costs vector for EXO
        :param exo_df:
        :return:
        """
        raise NotImplementedError('You must override get_costs() method')

    def __str__(self):
        return 'CostsManagerBase'


class CostsManagerEXOFixed(CostsManagerBase):
    def get_costs(self, exo_df):
        """
        Returns transactions costs vector for EXO
        :param exo_df:
        :return:
        """
        cost_context = self.context['costs']

        if 'context' in cost_context:
            if 'costs_options' not in cost_context['context']:
                raise ValueError("'costs_options' missing in costs settings['context']")
            if 'costs_futures' not in cost_context['context']:
                raise ValueError("'costs_futures' missing in costs settings['context']")

            costs_per_option = cost_context['context']['costs_options']
            costs_per_future = cost_context['context']['costs_futures']

            if 'nfutures_executed' not in exo_df:
                raise ValueError("You are using old version of EXO data array, rebuild EXO series to calculate costs properly")

            rollover_costs = exo_df['nfutures_executed'].abs() * abs(costs_per_future) +  exo_df['noptions_executed'].abs() * abs(costs_per_option)
            transaction_costs = exo_df['nfutures_opened'].abs() * abs(costs_per_future) + exo_df['noptions_opened'].abs() * abs(costs_per_option)

            return pd.DataFrame({'rollover_costs': rollover_costs, 'transaction_costs': transaction_costs}, index=exo_df.index)
        else:
            raise ValueError("'context' missing in costs settings")

    def __str__(self):
        return 'CostsManagerEXOFixed'




