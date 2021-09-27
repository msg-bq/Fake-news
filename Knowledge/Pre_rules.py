from rule import *

__all__ = ['Rule_For_Operator_Cure_COVID']

Rule_For_Operator_Cure_COVID = ['Rule_Cure_1']
All_rules = [Cure_rules]

class Rule_Cure_1(BaseRule):
    '''
    Cure相关规则第一条：在COVID19_Cure的认为可以治疗新冠，反之认为是谣言
    '''
    def __init__(self):
        name = 'Rule_Cure_1'
        adtecedent = None #eval调用判别
        consequent = self.Apply_rule
        scope = {'First': Concept_COVID19_Cure} #第x个参数允许的取值范围。这里写成all，而不是文档里的COVID19_Cure，主要是懒了，我一条规则里其实写了两条
        #这种自定义的集合，统一@开头，全大写便于识别
        super().__init__(name, adtecedent, consequent, scope, comments)

    def Apply_rule(self, variables): #Cure_COVID(COVID19_Cure) = True, Cure_COVID(COVID19_Cure') = False
        '''
        应当输入一个药物
        :type: Individual(str)
        '''
        if (self.Compare_adtecedent(variables) == True):
            #前件匹配上的话，执行后件。后件是针对每个规则单独书写的。不过后期期望根据str自动化的转为代码。目前不是问题，因为格式很规整。以后还需要思考
            if(type(variables[0]) != Individual): #类型得正确
                if(variables[0] in scope['First']): #如果在这药物里面
                    op = ActionOperators(operator=Cure_COVID,
                                         variables=[variables[0]]) #用list封装第一个，而不是直接传入，是考虑到有时候只要一部分
                    return Assertion(LHS = ActionOperators,
                                     RHS = True) #返回一个断言
                else:
                    op = ActionOperators(operator=Cure_COVID,
                                         variables=[variables[0]])  # 用list封装第一个，而不是直接传入，是考虑到有时候只要一部分
                    return Assertion(LHS=ActionOperators,
                                     RHS=False)
                    return
            else:
                return None

        else:
            return None #表示规则匹配失败，无法获取consequent
