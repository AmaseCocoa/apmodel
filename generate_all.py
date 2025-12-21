import time

start_time = time.time()
import apmodel
end_time = time.time()
print(f"import apmodel execution time: {end_time - start_time:.6f} seconds")

import json


def test_misskey_person():
    data_loc = "./tests/data/misskey_actor.json"
    with open(data_loc, "r") as f:
        actor_dict = json.load(f)

    start_time = time.time()
    actor = apmodel.load(actor_dict)
    end_time = time.time()
    print(f"apmodel.load execution time: {end_time - start_time:.6f} seconds")

    r = apmodel.to_dict(actor)
    print(json.dumps(r, indent=4, ensure_ascii=False))


test_misskey_person()
