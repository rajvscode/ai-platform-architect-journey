import json

CACHE_FILE = "cache.json"

def load_cache():
    try:
        with open(CACHE_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_cache(cache):
    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f, indent=2)

def get_from_cache(log):
    cache = load_cache()
    return cache.get(log)

def save_to_cache(log, result):
    cache = load_cache()
    cache[log] = result
    save_cache(cache)