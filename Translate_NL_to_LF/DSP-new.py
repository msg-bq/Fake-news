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

print(matches)
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

    
#cured做被动
matcher = DependencyMatcher(nlp.vocab)

pattern = [
    {
        "RIGHT_ID": "anchor_cure_passive",
        "RIGHT_ATTRS": {"ORTH": "cured", "POS": "VERB"},
    },
    {
        "LEFT_ID": "anchor_cure_passive",
        "REL_OP": ";*",
        "RIGHT_ID": "cure_subject",
        "RIGHT_ATTRS": {"DEP": {"IN": ["nsubj", "nsubjpass"]}},
    },
    {
        "LEFT_ID": "anchor_cure_passive",
        "REL_OP": ">",
        "RIGHT_ID": "be",
        "RIGHT_ATTRS": {"DEP": "auxpass"}
    },
    {
        "LEFT_ID": "anchor_cure_passive",
        "REL_OP": ">",
        "RIGHT_ID": "cure_prep_by",
        "RIGHT_ATTRS": {"ORTH": "by", "DEP": "prep"},#应该只能是cured by吧。by的依存关系，如果后面是名词，则是agent
        #动词是prep。这是连动词的规则
    },
    {
        "LEFT_ID": "cure_prep_by",
        "REL_OP": ">",
        "RIGHT_ID": "cure_pcomp", #by后面的动词
        "RIGHT_ATTRS": {"DEP": "pcomp"},
    },
    #希望的是一直取介词取到最后一个pobj为止，或者就最后一个pobj也行。用自带这个matcher规则的话就得写一大串，感觉不如写代码，先这样叭
    #不过如果是只要最后一个的话，倒是可以取巧，直接选取所有的pobj，然后从最后的mathes里弄数值最大的那个出来就行
    {
        "LEFT_ID": "cure_pcomp",
        "REL_OP": ">>",
        "RIGHT_ID": "cure_pobj", #by后面的动词
        "RIGHT_ATTRS": {"DEP": "pobj"},
    },
]

matcher.add("cure_pass", [pattern])
doc = nlp('the new coronavirus can be cured by drinking one bowl of freshly boiled garlic water')
matches = matcher(doc)

print(matches) 
# Each token_id corresponds to one pattern dict
match_id, token_ids = matches[0]
for i in range(len(token_ids)):
    print(pattern[i]["RIGHT_ID"] + ":", doc[token_ids[i]].text)
