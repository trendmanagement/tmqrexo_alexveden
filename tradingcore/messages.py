from datetime import datetime

class MsgBase:
    mtype = 'base'

    def __init__(self, dict_data=None):
        self.date = datetime.now()
        self.context = {}
        self.sender_appclass = ''
        self.sender_appname = ''

        if dict_data is not None:
            if not isinstance(dict_data, dict):
                raise ValueError("dict argument should be dictionary got: {0}".format(type(dict_data)))
            self.__dict__ = dict_data

    def as_dict(self):
        self.__dict__['mtype'] = self.mtype
        return self.__dict__

    def __str__(self):
        return str(self.as_dict())


class MsgStatus(MsgBase):
    mtype = 'status'

    def __init__(self, status, message, context={}, notify=False):
        super().__init__()
        self.message = message
        self.status = status
        self.context = context
        self.notify = notify

class MsgQuoteNotification(MsgBase):
    mtype = 'quote'

    def __init__(self, instrument, date, context={}):
        super().__init__()
        self.instrument = instrument
        self.date = date
        self.context = context

class MsgEXOQuote(MsgBase):
    mtype = 'exoquote'

    def __init__(self, exo_name, exo_date, context={}):
        super().__init__()
        self.exo_name = exo_name
        self.exo_date = exo_date
        self.context = context

class MsgAlphaState(MsgBase):
    mtype = 'alphastate'

    def __init__(self, swarm, context={}):
        super().__init__()

        self.swarm_name = swarm.name
        self.exo_name = swarm.exo_name
        self.instrument = swarm.instrument

        self.exposure = swarm.last_exposure
        self.prev_exposure = swarm.last_prev_exposure
        self.rebalamce_date = swarm.last_rebalance_date
        self.last_date = swarm.last_date
        self.context = context

class MsgAlphaSignal(MsgBase):
    mtype = 'alphasignal'

    def __init__(self, alphastate_msg, pos_list, context={}):
        super().__init__()
        self.swarm_name = alphastate_msg.swarm_name
        self.exo_name = alphastate_msg.exo_name
        self.instrument = alphastate_msg.instrument
        self.exposure = alphastate_msg.exposure
        self.positions = pos_list
        self.context = context



