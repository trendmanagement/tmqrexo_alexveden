

class Account:
    def __init__(self, acc_dict, mongodb):
        self._dict = acc_dict
        self._db = mongodb


    @property
    def name(self):
        return self._dict['name']

    @property
    def client_name(self):
        return self._dict['client_name']

    @property
    def dbid(self):
        return self._dict['_id']
