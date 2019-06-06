import json
skillTag='{"qualifications":null,' \
         '"role":null,' \
         '"chatWindow":null,' \
         '"refreshLevel":2,' \
         '"skillLabel":["java"]}'

result=json.loads(skillTag)
print(type(result))
print(result['skillLabel'])