from concept import *
from variable_type import *

__all__ = ['BaseOperator', 'ActionOperators']

class BaseOperator(object):
    '''
    Operator的母类
    '''
    def __init__(self, number_of_variables=0, comments=''):
        self.number_of_variables = number_of_variables
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

class Cure_COVID(BaseOperator):
    '''
    能否治疗新冠的operator，返回True or False
    '''
    def __init__(self):
        number_of_variables = 1
        super().__init__(number_of_variables = number_of_variables)

    def __call__(self, variables):
        # assert self.number_of_variables == len(self.variables) #应该是个字典，暂时先不限制数量了，说不准有多个参数的需求。
        #等碰到重载等需求时候再判断吧
        if(variables[])

#把各个rule汇总到一个operator里，这就定义了operator，并且可以遍历获取事实

def VariablesIsSatisfied(input_adtecedent, adtecedent, scope):
    '''
    判断规则的adtecedent中，各传入的变量是否和adtecedent一致，且在论域内
    :type: number, Individual, Set, Assertion
    :return: True or False
    '''
    if(len(input_adtecedent.variables) != len(adtecedent.variables)):
        return False

    for input_item, item in zip(input_adtecedent, adtecedent):
        if(type(input_item) != type(item)):
            return False
        if(type(input_item) == Number):
            pass #暂时还没在scope里设置取值范围相关规定
        elif(type(input_item) == Individual):


class BaseRule(object):
    '''
    Rule的母类
    '''
    def __init__(self, name='', adtecedent=None, consequent=None, scope=None, comments=''):
        self.name = name
        self.adtecedent = adtecedent #这两个需要单独在各自class里定义
        self.consequent = consequent
        self.scope = scope
        self.comments = comments


Cure_rules = ['Rule_Cure_1']
All_rules = [Cure_rules]

class Rule_Cure_1(BaseRule):
    '''
    Cure相关规则第一条：在COVID19_Cure的认为可以治疗新冠，反之认为是谣言
    '''
    def __init__(self):
        name = 'Rule_Cure_1'
        adtecedent = None #eval调用判别
        consequent = self.Apply_rule
        scope = {'First': '@ALL'} #第x个参数允许的取值范围。这里写成all，而不是文档里的COVID19_Cure，主要是懒了，我一条规则里其实写了两条
        #这种自定义的集合，统一@开头，全大写便于识别
        super().__init__(name, adtecedent, consequent, scope, comments)

    def Compare_adtecedent(self, input_adtecedent): #类型是assertion
        if (self.adtecedent == None):
            return True
        else: #这时候应该是匹配assertion是否一致，按道理是没有其他类型会作为输入的
            if((adtecedent.operator == input_adtecedent.operator)
                    and VariablesIsSatisfied(adtecedent.variables, input_adtecedent.variables)):
                #匹配算子和
                #这个比较还是挺草率的，依赖于python的=运算符对诸多类型的支持。但是还是得谨慎一下
                if(adtecedent.Forward() == input_adtecedent.Forward()):
                    return True
                else:
                    return False
            else:
                return False


    def Apply_rule(self, variables):
        if (Compare_adtecedent == True):

        else:
            return False #表示规则匹配失败，无法获取consequent