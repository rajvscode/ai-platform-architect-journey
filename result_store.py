import json

RESULT_FILE = "results.json"


def load_results():
    try:
        with open(RESULT_FILE, "r") as f:
            return json.load(f)
    except:
        return {}


def save_results(data):
    with open(RESULT_FILE, "w") as f:
        json.dump(data, f, indent=2)


def save_result(job_id, result):
    data = load_results()
    data[job_id] = result
    save_results(data)


def get_result(job_id):
    data = load_results()
    return data.get(job_id)