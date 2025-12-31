import time
import json
CACHE = {}

def get_cached_insights(key):
    entry = CACHE.get(key)
    if entry:
        return entry['data'], entry['ts']
    return None, None

def set_cached_insights(key, data):
    CACHE[key] = {'data': data, 'ts': time.time()}
