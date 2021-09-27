#命名规则 Rule/Concept/Operator + _ + 具体名字

from concept import *
from variable_type import *
from Pre_concepts import *
from Pre_rules import *

__all__ = ['BaseOperator', 'ActionOperators']

class BaseOperator(object):
    '''
    Operator的母类
    '''
    def __init__(self, number_of_variables=0, comments=''):
        self.number_of_variables = number_of_variables
        self.rules = rules
        self.comments = comments

class ActionOperators(object):
    '''
    最初为了兼容Assertion做参数的场景。名字和杨明师兄的一样，但是目的好像不一样的。
    现在它也被用来帮助我们按operator来归类、运算rule，减少完全的遍历，我不造这个是否值得。理论上这可以自动化的完成，因为这相当于预遍历。
    '''
    def __init__(self, operator, variables):
        self.operator = operator
        self.variables = variables

    def Forward(self): #这是不是只对输出值的有效？如果是的话，就需要判一些情况？
        return self.operator(self.variables) #这个地方应该是遍历诸多规则

    # def Inference(self): #不知道有无这个需求

class Operator_Cure_COVID(BaseOperator):
    '''
    能否治疗新冠的operator，包含了与cure相关的所有规则，返回
    '''
    def __init__(self):
        number_of_variables = 1
        rules = [Rule_For_Operator_Cure_COVID]
        comments = ''
        super().__init__(number_of_variables = number_of_variables,
                         rules = rules,
                         comments = comments)

    def __call__(self, variables):
        new_facts = []
        for rule in self.rules:
            if(rule.Compare_adtecedent(variables) == True): #能匹配上的就用
                facts = rule.Apply_rule(variables)
                new_facts.extend(facts)

        return new_facts



#把各个rule汇总到一个operator里，这就定义了operator，并且可以遍历获取事实



