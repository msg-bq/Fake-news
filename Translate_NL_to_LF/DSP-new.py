#先不写成整个系统了，能一个个手动抽取就行。下面全是抽取规则部分

import spacy #3.0以上版本
from spacy.matcher import DependencyMatcher

nlp = spacy.load('en_core_web_sm-3.1.0') #自己下载后的目录

# cure做动词的陈述句
matcher = DependencyMatcher(nlp.vocab)

pattern = [
    {
        "RIGHT_ID": "anchor_cure",
        "RIGHT_ATTRS": {"ORTH": "cure"}
    },
    {
        "LEFT_ID": "anchor_cure",
        "REL_OP": "$--",
        "RIGHT_ID": "cure_subject",
        "RIGHT_ATTRS": {"DEP": "nsubj"},
    },
    {
        "LEFT_ID": "anchor_cure",
        "REL_OP": ">",
        "RIGHT_ID": "cure_object",
        "RIGHT_ATTRS": {"DEP": "dobj"},
    },
#     {
#         "LEFT_ID": "cure_object",
#         "REL_OP": ">>",
#         "RIGHT_ID": "cure_objects",
#         "RIGHT_ATTRS": {"DEP": 'conj'},
#     }
]

matcher.add("cure", [pattern])
doc = nlp("hydroxychloroquine cure the virus")
matches = matcher(doc)

print(matches) # [(4851363122962674176, [6, 0, 10, 9])]
# Each token_id corresponds to one pattern dict
match_id, token_ids = matches[0]
for i in range(len(token_ids)):
    print(pattern[i]["RIGHT_ID"] + ":", doc[token_ids[i]].text)

    
#名词
pattern = [
    {
        "RIGHT_ID": "anchor_cure_noun",
        "RIGHT_ATTRS": {"ORTH": {"IN": ["cure", "cures"]}, "POS": "NOUN"},
        "RIGHT_ATTRS": {"DEP": "attr"}
    },
    {
        "LEFT_ID": "anchor_cure_noun",
        "REL_OP": "<",
        "RIGHT_ID": "cure_attr",
        "RIGHT_ATTRS": {},#寻找is are这种，就是cure的父节点自己。并且要求这个词与cure的关系是attr
    },
    {
        "LEFT_ID": "cure_attr",
        "REL_OP": ">",
        "RIGHT_ID": "nsubj",
        "RIGHT_ATTRS": {"DEP": {"IN": ["nsubj", "expl"]}}, #expl是处理there be的
    },
    {
        "LEFT_ID": "anchor_cure_noun",
        "REL_OP": ">",
        "RIGHT_ID": "cure_prep",
        "RIGHT_ATTRS": {"DEP": "prep"},
    },
    {
        "LEFT_ID": "cure_prep",
        "REL_OP": ">",
        "RIGHT_ID": "cure_pobj",
        "RIGHT_ATTRS": {"DEP": "pobj"},
    },
]

matcher.add("cure_noun", [pattern])
doc = nlp("freshly boiled garlic water is a cure for coronavirus")
matches = matcher(doc)

print(matches)
# Each token_id corresponds to one pattern dict
match_id, token_ids = matches[0]
for i in range(len(token_ids)):
    print(pattern[i]["RIGHT_ID"] + ":", doc[token_ids[i]].text)
