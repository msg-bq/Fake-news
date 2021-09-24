#先不写成整个系统了，能一个个手动抽取就行。下面全是抽取规则部分

import spacy #3.0以上版本
from spacy.matcher import DependencyMatcher



# cure做动词的陈述句


pattern_verb_1 = [
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


# doc = nlp("the hydroxychloroquine cure the virus")
# matches = matcher(doc)

# print(matches)
# # Each token_id corresponds to one pattern dict
# match_id, token_ids = matches[0]
# for i in range(len(token_ids)):
#     print(pattern[i]["RIGHT_ID"] + ":", doc[token_ids[i]].text)

    
#名词-A是治疗方法为了B
pattern_noun_1 = [
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


# doc = nlp("freshly boiled garlic water is a cure for coronavirus")
# matches = matcher(doc)

# print(matches)
# # Each token_id corresponds to one pattern dict
# match_id, token_ids = matches[0]
# for i in range(len(token_ids)):
#     print(pattern[i]["RIGHT_ID"] + ":", doc[token_ids[i]].text)


#名词-A是B的治疗方法
# matcher = DependencyMatcher(nlp.vocab)

pattern_noun_2 = [
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
        "RIGHT_ID": "cure_compound",
        "RIGHT_ATTRS": {"DEP": "compound"},#XXX治疗方法，里的XXX
    },
]


# doc = nlp('israeli recipe for lemon and bicarbonate drink is a coronavirus cure')
# matches = matcher(doc)

# print(matches)
# # Each token_id corresponds to one pattern dict
# match_id, token_ids = matches[0]
# for i in range(len(token_ids)):
#     print(pattern[i]["RIGHT_ID"] + ":", doc[token_ids[i]].text)
    

#cured做被动
# matcher = DependencyMatcher(nlp.vocab)

pattern_verb_pass = [
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


# doc = nlp('the the virus can be cured by drinking one bowl of freshly boiled garlic water')
# matches = matcher(doc)

# print(matches)
# # Each token_id corresponds to one pattern dict
# match_id, token_ids = matches[0]
# for i in range(len(token_ids)):
#     print(pattern[i]["RIGHT_ID"] + ":", doc[token_ids[i]].text)


samples = ['social media posts recommend tonic water and the zinc as a cure for a virus infection as the drink contains quinine whose synthetic relative the hydroxychloroquine is on trial as a the virus treatment',
 'israeli recipe for lemon and bicarbonate drink is a coronavirus cure',
  'coronavirus does not cause a runny nose, and is killed by temperatures above 26 degrees, and causes lung fibrosis within days of infection, and can be diagnosed by holding your breath for 10 seconds and can be cured in the early stages by drinking plenty of water',
 'posts on social media claim that a spanish biological researcher called on international soccer stars cristiano ronaldo and lionel messi to find a cure for the virus since they earn much more money than scientists',
 'nevada governor steve sisolak has banned the use of an antimalaria drug that might help cure coronavirus',
 'president donald trump will announce that a scientist finally found a vaccine to cure coronavirus',
 'boiled orange peels with cayenne pepper are a cure for coronavirus',
 'breathing air from a hair dryer or a sauna can prevent or cure the virus',
 'huge results from breaking chloroquine study show 100 cure rate for patients infected with the coronavirus',
 'freshly boiled garlic water is a cure for coronavirus',
 'every election year has a disease coronavirus has a contagion factor of 2 and a cure rate of 997 for those under 50 it infects',
 'chlorine dioxide kits sold online under various mms names  miracle mineral solution miracle mineral supplement master mineral solution  will cure the coronavirus',
 'the the virus can be cured by drinking one bowl of freshly boiled garlic water',
 'romania developed a coronavirus vaccine able to cure white people only',
 'knust students discover vaccine for coronavirus and cure patient in cte divoire',
 'a video posted on facebook claiming that chloroquine and the azithromycin are proven cures of the virus',
 'there is no cure for the virus no matter what the internet says',
 'the hydroxychloroquine cures this virus it just so happens this is the treatment used for radiation sickness',
 'thousands of doctors say the hydroxychloroquine cures coronavirus',
 'black cats in vietnam are being killed and consumed as a the virus cure',
 'we cant make a vaccine that works for flu no vaccine for the respiratory syncytial virus rsv and we cant cure cancer yet somehow scientists can make a vaccine for the virus in six months',
 'the hydroxychloroquine, the azithromycin and the zinc cure the virus',
 'a group called americas frontline doctors are featured in viral video claiming the hydroxychloroquine cures the virus',
 'stella immanuel claims that the drug combination of the hydroxychloroquine, the zinc and the azithromycin is a cure and preventative for the virus and that people dont need to wear masks or practice physical distancing in a breitbart video featuring a group called americas frontline doctors',
 'fda warns of silver other bogus the virus cures',
 'the hydroxychloroquine no the virus cure experts warn']

def add_cure_patterns(matcher):
    '''
    将需要用的pattern放到这个matcher里
    '''
    matcher.add("cure_verb_1", [pattern_verb_1]) #陈述句
    matcher.add("cure_noun_1", [pattern_noun_1]) #A是治疗方式为了B
    matcher.add("cure_noun_2", [pattern_noun_2]) #A是B的治疗方式
    matcher.add("cure_verb_pass", [pattern_verb_pass]) #被动句

    return matcher

if __name__ == '__main__':
    nlp = spacy.load('D:/git/Fake-news/Fake-news/en_core_web_sm-3.1.0') #自己的目录
    matcher = DependencyMatcher(nlp.vocab)
    cure_matcher = add_cure_patterns(matcher)

    match_results = [] #匹配的结果

    for sample in samples:
        doc = nlp(sample)
        match_result = cure_matcher(doc)
        if(len(match_result) == 0):
            continue
        match_results.append(match_result)
        match_id, token_ids = match_result[0]
        for i in range(len(token_ids)):
            print(pattern[i]["RIGHT_ID"] + ":", doc[token_ids[i]].text)

    print(len(match_results) / len(samples))