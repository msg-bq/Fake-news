from Pre_procession import read_pd

file_path = 'D:/research/CSKNN/军事常识/假新闻/datasets/CoAID-master/total - 副本-完整 - 5月特殊符号.xls'
datasets = read_pd(file_path, 'test')

#取出所有含cure的样本
Prediate_words = [' cure']
screened_data = {}
for text in datasets.iloc[:,0]:
    for word in Prediate_words:
        if(text.find(word) != -1):
            if(word not in screened_data):
                screened_data[word] = []
                screened_data[word].append(text)
            else:
                screened_data[word].append(text)
print(len(screened_data[' cure']))

#下面这部分程序我在vscode里运行的，先放结果叭,之后补代码
# result = [{'verb': 'cure', 'ARG0': 'an antimalaria drug', 'ARG1': 'coronavirus', 'Sentence': 'an antimalaria drug cure coronavirus'}, {'verb': 'cure', 'ARG0': 'a vaccine', 'ARG1': 'coronavirus', 'Sentence': 'a vaccine cure coronavirus'}, {'verb': 'cure', 'ARG0': 'breathing air from a hair dryer or a sauna', 'ARG1': 'covid19', 'Sentence': 'breathing air from a hair dryer or a sauna cure covid19'}, {'verb': 'cure', 'ARG0': 'chlorine dioxide kits sold online under various mms names miracle mineral solution miracle mineral supplement master mineral solution', 'ARG1': 'the coronavirus', 'Sentence': 'chlorine dioxide kits sold online under various mms names miracle mineral solution miracle mineral supplement master mineral solution cure the coronavirus'}, {'verb': 'cure', 'ARG0': 'a coronavirus vaccine', 'ARG1': 'white people', 'Sentence': 'a coronavirus vaccine cure white people'}, {'verb': 'cures', 'ARG0': 'hydroxychloroquine', 'ARG1': 'this virus', 'Sentence': 'hydroxychloroquine cures this virus'}, {'verb': 'cures', 'ARG0': 'hydroxychloroquine', 'ARG1': 'coronavirus', 'Sentence': 'hydroxychloroquine cures coronavirus'}, {'verb': 'cure', 'ARG0': 'we', 'ARG1': 'cancer', 'Sentence': 'we cure cancer'}, {'verb': 'cures', 'ARG0': 'hydroxychloroquine', 'ARG1': 'covid19', 'Sentence': 'hydroxychloroquine cures covid19'}]

#SRL部分代码
from allennlp.predictors.predictor import Predictor
import allennlp_models.tagging
import re

predictor = Predictor.from_path("/data/bingqian/COAID/knowledge/structured-prediction-srl-bert.2020.12.15.tar.gz") #得自己下一个
#http://storage.googleapis.com/allennlp-public-models/structured-prediction-srl-bert.2020.12.15.tar.gz

datasets = screened_data[' cure']

result = []
for text in datasets:
    result.append(predictor.predict(sentence=text))

def find_ARG(description): #找到谓词是cure的词
    split_description = re.split(r'[\[\]]', description)
    ARG = []
    for item in split_description:
        if(item[:3] == 'ARG' and item[4] == ':'):
            if(item[3] == '0'):
                ARG.insert(0, item[6:])
            else:
                ARG.append(item[6:])
            
    if(len(ARG) < 2):
        return False
    else:
        # print(ARG)
        return ARG
    
def extract_facts(datasets):
    Facts = []
    for result in datasets:
        for verb in result['verbs']:
            if(verb['verb'].find('cure') == -1):
                continue
            ARG = find_ARG(verb['description'])
            if(ARG == False):
                continue
            else:
                Facts.append({'verb':verb['verb'],
                            'ARG0':ARG[0],
                            'ARG1':ARG[1],
                            'Sentence': ARG[0] + ' ' + verb['verb'] + ' ' + ARG[1]})
    return Facts

Facts = extract_facts(result)

for fact in Facts:
    print(fact['Sentence'])
 
