#依存句法，尚未写完

import spacy
import en_core_web_sm

#这是获取依存关系的例子
def ner_spacy(models, datasets):
    nlp = eval(models + ".load()")
    doc = nlp(datasets)

    return doc
train_data = "hydroxychloroquine azithromycin and zinc cure the virus"
ner_results = ner_spacy('en_core_web_sm', train_data)
for token in ner_results:
    print('{0}({1}) <-- {2} -- {3}({4})'.format(token.text, token.tag_, token.dep_, token.head.text, token.head.tag_))

#这里是依存关系绘图
from spacy import displacy
displacy.serve(ner_results, style='dep')


#下面是抽取部分尚未写完
def ner_spacy(models, datasets):
    nlp = eval(models + ".load()")
    doc = nlp(datasets)
    return doc

# dependency_rules = {}
# cure_dependency_rules = []
# dependency_rules['cure_dependency_rules': 'cure_dependency_rule']

class cure_dependency_rule(): #记录和cure有关的各种规则，不过很多规则应该是通用的，所以日后可以考虑单独拎出去，作为一个可被索引的抽取规则库
    def __init__(self, text):
        self.text = text
        replace_words_generate(self.text)
        self.ner_result = ner_spacy('en_core_web_sm', self.text)
#         self.sematic_tree = self.build_sematic_tree(self.ner_result) #建树虽然整齐，但是好像还是不那么地舒服。
# #要不在cc处，建成类似可持久化的形式？另外不知道有无向上索引的,好像没有
        self.rules = ['svo']

    def build_sematic_tree(ner_result):  # 先不建树了，有一个双向的指针就好了
        '''
        :return: Point_tokens['cure'] = {'nsubj': ['azithromycin'], 'ROOT': ['cure'], 'dobj': ['virus']}
        '''
        Point_tokens = {}  # 记录父节点到子节点的指针
        for token in ner_result:
            head = token.head.text
            if (head not in Point_tokens.keys()): #判断父节点不存在
                Point_tokens[head] = {}
            if (token.dep_ not in Point_tokens[head].keys()): #判断父节点对应的子节点的类型是否存在
                Point_tokens[head][token.dep_] = []
            Point_tokens[head][token.dep_].append(token.text) #用数组是因为，同依存关系的子节点可以有多个，比如conj
        return Point_tokens


    #     def build_sematic_tree(self, ner_result):
#         Root = {'word': [], 'dep': '', 'tag': '', 'son': {}, 'pos': []}
#         now = Root
# #         pos_tokens = {}
#         pos_cnt = 0
#         pos_son = []
#         for token in self.ner_result:
# #             pos_tokens[token.text] = pos_cnt
#             if(token.dep == 'ROOT'):
#                 pos_son.append(pos_cnt)
#                 pos_cnt += 1
#                 while(pos_cnt < len(self.ner_result)
#                       && (self.ner_result[pos_cnt].dep_ == 'cc' || self.ner_result[pos_cnt].dep_ == 'conj')):
#                     if(self.ner_result[pos_cnt].dep_ == 'conj'):
#                         pos_son.append(pos_cnt)
#                     pos_cnt += 1
#
#             pos_cnt += 1
#
#         now['pos'] = pos_son
#
#         while(len(pos_son) != 0):
#             for pos in now['pos']:
#                 now['word'].append(ner_result[pos].text)
#                 now['dep'] = ner_result[pos].dep_
#                 now['tag'] = ner_result[pos].tag_
#
#                 #找子节点
#                 pos_cnt_son = 0
#                 for token in self.ner_result:
#                     if(token.head.text == ner_result[pos].text):
#                         nxt = {'word': [], 'dep': '', 'tag': '', 'son': {}, 'pos' = []}
#
#                     pos_cnt_son += 1
    
    
    def translate_to_svo(self):
        for token in self.ner_result:
            if(token.text.find('cure') != -1): #筛选的时候应该已经过滤secure等了。token.text[:3] == 'cur' && 
                success = 1 #尚未成功，这个参数是因为，一个词性可能对应不同的规则，需要一个个试过去
                end = 0 #实在试完了都不匹配，那也没办法
                num = 0 #第几个规则
                while(success && num < rules_cnt):
                    translate_rule, rules_cnt = match_rules(token, num)
                    num += 1
                    result = translate_rule(token)
                    
        
    def replace_words_generate(self):
        #有一些特殊的词值得换掉
        the_covid = ['the covid19', 'the new coronavirus', 'the novel coronavirus', 'covid19', 'new coronavirus', 'novel coronavirus']
        for word in the_covid:
            pos = self.text.find(word)
            if(pos != -1):
                self.text = self.text.replace(word, 'the virus')
    
    def match_rules(self, token, num): #num指示某个规则的第几个，初始0
        VB_rule = [self.VB_1] #前面是把一个个的规则放在数组里，日后索引函数地址
        
        if(token.tag_ == 'VB') #暂时考虑词性来分配，如果以后有其他方案，再说
            return VB_rule[num], len(VB_rule)

    def VB_1(self):
        
        

#     #依存关系检测
#     for token in ner_results:
#         print('{0}({1}) <-- {2} -- {3}({4})'.format(token.text, token.tag_, token.dep_, token.head.text, token.head.tag_))
