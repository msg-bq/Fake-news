# 先不写成整个系统了，能一个个手动抽取就行。下面全是抽取规则部分

import spacy  # 3.0以上版本
from spacy.matcher import DependencyMatcher

# cure做动词的陈述句


pattern_verb_1 = [
    {
        "RIGHT_ID": "anchor_cure",
        "RIGHT_ATTRS": {"ORTH": {"IN": ["cure", "cures"]}}
    },
    {
        "LEFT_ID": "anchor_cure",
        "REL_OP": "$--",
        "RIGHT_ID": "cure_subject",
        "RIGHT_ATTRS": {"DEP": {"IN": ["nsubj", "csubj"]}},
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


# 名词-A是治疗方法为了B
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
        "RIGHT_ATTRS": {},  # 寻找is are这种，就是cure的父节点自己。并且要求这个词与cure的关系是attr
    },
    {
        "LEFT_ID": "cure_attr",
        "REL_OP": ">",
        "RIGHT_ID": "nsubj",
        "RIGHT_ATTRS": {"DEP": {"IN": ["nsubj", "expl"]}},  # expl是处理there be的
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


# 名词-A是B的治疗方法
# matcher = DependencyMatcher(nlp.vocab)

pattern_noun_2 = [
    {
        "RIGHT_ID": "anchor_cure_noun",
        "RIGHT_ATTRS": {"ORTH": {"IN": ["cure", "cures"]}, "POS": "NOUN", "DEP": {"IN": ["attr", "pobj"]}},
    },
    {
        "LEFT_ID": "anchor_cure_noun",
        "REL_OP": "<",
        "RIGHT_ID": "cure_attr",
        "RIGHT_ATTRS": {},  # 寻找is are这种，就是cure的父节点自己。并且要求这个词与cure的关系是attr
    },
    {
        "LEFT_ID": "cure_attr",
        "REL_OP": ";*", #原来是>>，换成这个后，如果有多个nsubj，应当取最后那个没宾语的。所以这个还是适合写代码，选取往上走第一个有主语的，然后再把conj一串带走
        "RIGHT_ID": "nsubj",
        "RIGHT_ATTRS": {"DEP": {"IN": ["nsubj", "nsubjpass", "expl"]}},  # expl是处理there be的; advcl好像意味着引导一个从句，还有待继续考虑 #nsubjpass是考虑到有时候主语处在被动态
    },
    {
        "LEFT_ID": "anchor_cure_noun",
        "REL_OP": ">",
        "RIGHT_ID": "cure_compound",
        "RIGHT_ATTRS": {"DEP": "compound"},  # XXX治疗方法，里的XXX
    },
]

# doc = nlp('israeli recipe for lemon and bicarbonate drink is a coronavirus cure')
# matches = matcher(doc)

# print(matches)
# # Each token_id corresponds to one pattern dict
# match_id, token_ids = matches[0]
# for i in range(len(token_ids)):
#     print(pattern[i]["RIGHT_ID"] + ":", doc[token_ids[i]].text)


# cured做被动
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
        "RIGHT_ATTRS": {"ORTH": "by", "DEP": {"IN": ["prep", "agent"]}},  # 应该只能是cured by吧。by的依存关系，如果后面是名词，则是agent
        # 动词是prep。这是连动词的规则
    },
    {
        "LEFT_ID": "cure_prep_by",
        "REL_OP": ">",
        "RIGHT_ID": "cure_pcomp",  # by后面的动词
        "RIGHT_ATTRS": {"DEP": "pcomp"},
    },
    # 希望的是一直取介词取到最后一个pobj为止，或者就最后一个pobj也行。用自带这个matcher规则的话就得写一大串，感觉不如写代码，先这样叭
    # 不过如果是只要最后一个的话，倒是可以取巧，直接选取所有的pobj，然后从最后的mathes里弄数值最大的那个出来就行
    {
        "LEFT_ID": "cure_pcomp",
        "REL_OP": ">>",
        "RIGHT_ID": "cure_pobj",  # by后面的动词
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

pattern_verb_2 = [ #其实为了整齐应该放在上面，但是下面是避免影响markdown的索引
    {
        "RIGHT_ID": "anchor_cure",
        "RIGHT_ATTRS": {"ORTH": {"IN": ["cure", "cures"]}}
    },
    {
        "LEFT_ID": "anchor_cure",
        "REL_OP": ">", #和verb_1相比，只有这里变了。这个对于VB_1函数的话，应该是都能包括的
        "RIGHT_ID": "cure_subject",
        "RIGHT_ATTRS": {"DEP": {"IN": ["nsubj", "csubj"]}},
    },
    {
        "LEFT_ID": "anchor_cure",
        "REL_OP": ">",
        "RIGHT_ID": "cure_object",
        "RIGHT_ATTRS": {"DEP": "dobj"},
    },
]


samples = [
    'social media posts recommend tonic water and the zinc as a cure for a virus infection as the drink contains quinine whose synthetic relative the hydroxychloroquine is on trial as a the virus treatment',
    'israeli recipe for lemon and bicarbonate drink is a virus cure',
    'coronavirus does not cause a runny nose, and is killed by temperatures above 26 degrees, and causes lung fibrosis within days of infection, and can be diagnosed by holding your breath for 10 seconds and can be cured in the early stages by drinking plenty of water',
    'nevada governor steve sisolak has banned the use of an antimalaria drug that might help cure coronavirus',
    'president donald trump will announce that a scientist finally found a vaccine to cure coronavirus',
    'boiled orange peels with cayenne pepper are a cure for the virus',
    'breathing air from a hair dryer or a sauna can prevent or cure the virus',
    'freshly boiled garlic water is a cure for coronavirus',
    'Chlorine dioxide kits sold online under various MMS names Miracle Mineral Solution, Miracle Mineral Supplement, Master Mineral Solution will cure the virus.',
    'the virus can be cured by drinking one bowl of freshly boiled garlic water',
    'romania developed a virus vaccine able to cure white people only',
    'lemon juice and bicarbonate mixture prevents and cures the virus in israel',
    'knust students discover vaccine for the virus and cure patient in cte divoire',
    'a video posted on facebook claiming that chloroquine and the azithromycin are proven cures of the virus',
    'there is no cure for the virus no matter what the internet says',
    'the hydroxychloroquine cures this virus it just so happens this is the treatment used for radiation sickness',
    'thousands of doctors say the hydroxychloroquine cures coronavirus',
    'black cats in vietnam are being killed and consumed as a the virus cure',
    'hydroxychloroquine, azithromycin and zinc cure the virus', #前面有非停止词的时候再加the，其他时候就算了
    'a group called americas frontline doctors are featured in viral video claiming the hydroxychloroquine cures the virus',
    'stella immanuel claims that the drug combination of the hydroxychloroquine, the zinc and the azithromycin is a cure and preventative for the virus and that people dont need to wear masks or practice physical distancing in a breitbart video featuring a group called americas frontline doctors',
    'the hydroxychloroquine no the virus cure, experts warn']


def add_cure_patterns(matcher):
    '''
    将需要用的pattern放到这个matcher里
    '''
    matcher.add("cure_verb_1", [pattern_verb_1])  # 陈述句
    matcher.add("cure_verb_2", [pattern_verb_2]) #陈述句
    matcher.add("cure_noun_1", [pattern_noun_1])  # A是治疗方式为了B
    matcher.add("cure_noun_2", [pattern_noun_2])  # A是B的治疗方式
    matcher.add("cure_verb_pass", [pattern_verb_pass])  # 被动句

    return matcher


if __name__ == '__main__':
    nlp = spacy.load('D:/git/Fake-news/Fake-news/en_core_web_sm-3.1.0')  # 自己的目录
    matcher = DependencyMatcher(nlp.vocab)
    cure_matcher = add_cure_patterns(matcher)

    match_results = []  # 匹配的结果

    for sample in samples:
        doc = nlp(sample)
        match_result = cure_matcher(doc)
        if (len(match_result) == 0):
            continue
        match_results.append(match_result)
        match_id, token_ids = match_result[0]
        print("样本原句：", sample)
        print("提取情况：")
        for i in range(len(token_ids)):
            print(cure_matcher.get(match_id)[1][0][i]["RIGHT_ID"] + ":", doc[token_ids[i]].text)
        print("=======================")

    print("样本数：", len(samples))
    print("识别成功数：", len(match_results))
    print(len(match_results) / len(samples))