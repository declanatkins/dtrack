import json
import numpy as np


class DTrackJsonEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, np.ndarray):
            return o.tolist()
        elif hasattr(o, 'to_json'):
            return o.to_json()
        else:
            return super().default(o)