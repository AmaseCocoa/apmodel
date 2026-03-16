import apmodel

test = {
  "@context": "https://www.w3.org/ns/activitystreams",
  "type": "Create",
  "actor": "https://example.org",
  "object": "https://example.org"
}

print(type(apmodel.load(test)))