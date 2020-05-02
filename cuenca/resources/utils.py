import datetime as dt


class DictFactory(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for k, v in self.items():
            if isinstance(v, dt.date):
                self[k] = v.isoformat()
