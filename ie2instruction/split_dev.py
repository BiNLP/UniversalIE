import json
from convert.utils.utils import stable_hash, write_to_json

input = '/scratch2/nlp/chenzhenbin/Workspaces/IEPile/data/dev.json'

NER = []
RE = []
EE = []

with open(input, 'r', encoding='utf-8') as f:
    counter = 0
    for line in f:
        data = json.loads(line)

        if data['task'] == 'NER':
            NER.append(data)
            counter += 1
        elif data['task'] == 'RE':
            RE.append(data)
            counter += 1
        elif data['task'] == 'EE':
            EE.append(data)
            counter += 1
        else:
            pass
    print(counter)

NER_PATH = '/scratch2/nlp/chenzhenbin/Workspaces/IEPile/data/dev_ner.json'
RE_PATH = '/scratch2/nlp/chenzhenbin/Workspaces/IEPile/data/dev_re.json'
EE_PATH = '/scratch2/nlp/chenzhenbin/Workspaces/IEPile/data/dev_ee.json'
write_to_json(NER_PATH,NER)
write_to_json(RE_PATH,RE)
write_to_json(EE_PATH,EE)