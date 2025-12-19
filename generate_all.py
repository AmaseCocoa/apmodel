import json

import apmodel
from apmodel.registry import registry


def test_misskey_person():
    data_loc = "./tests/data/misskey_actor.json"
    with open(data_loc, "r") as f:
        actor_dict = json.load(f)
        apmodel.load(actor_dict)

    #r = apmodel.to_dict(actor)
    #print(json.dumps(r, indent=4, ensure_ascii=False))
print(registry.all())

#test_misskey_person()