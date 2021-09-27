__all__ = ['BaseRule']

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
        self.order = ['First', 'Second', 'Third'] #虽然其实我觉得也不必排序，因为输出的参数应该不会超出输入的参数
        if(self.adtecedent == None):
            assert type(self.consequent) == Assertion

    def Compare_adtecedent(self, input_adtecedent): #类型是assertion
        if (self.adtecedent == None):
            return True
        else: #这时候应该是匹配assertion是否一致，按道理是没有其他类型会作为输入的
            if((adtecedent.LHS.operator == input_adtecedent.LHS.operator)
                and VariablesIsSatisfied(adtecedent.variables, input_adtecedent.variables)
                and adtecedent.RHS == input_adtecedent.RHS):
                #匹配算子和
                #这个比较还是挺草率的，依赖于python的=运算符对诸多类型的支持。但是还是得谨慎一下
                if(adtecedent.Forward() == input_adtecedent.Forward()):
                    return True
                else:
                    return False
            else:
                return False


    def Is_equal(self, input_adtecedent, adtecedent):
        '''
        衡量两个变量是否相等。虽然此时已知input_adtecedent必为assertion，但也多写一遍判断吧，说不准以后有其他需求
        '''
        if (type(input_adtecedent.LHS) != type(adtecedent.LHS) or type(input_adtecedent.RHS) != type(adtecedent.RHS)): #Assertion应该不会出现，既可以是A的元素a，又是A集合。因为集合是有性质的
            #但是个体会有一些集合外的性质，不太可能直接说完全等价。但这个假设有待商榷。
            return False

        if(type(input_adtecedent) == Assertion):
            LHS_equal = self.Is_ActionOpeartor_equal(input_adtecedent.LHS, adtecedent.LHS)

            #下面是右式
            RHS_equal = None
            if(type(input_adtecedent.RHS) == Assertion): #虽然说是说右式可以为Assertion，写个递归就行。但是咱这里就先跳了啊
                raise ValueError("匹配前件时右式是Assertion")
            elif(type(input_adtecedent.RHS) == ActionOperator):#其他的好像都差不多
                RHS_equal = self.Is_ActionOpeartor_equal(input_adtecedent.RHS, adtecedent.RHS)
            else:
                RHS_equal = self.VariablesIsSatisfied(input_adtecedent.RHS,
                                                      self.scope[self.order[-len(input_adtecedent.RHS):]])

        else:
            pass #暂且没需求

         return (LHS_equal and RHS_equal)

    def Is_ActionOpeartor_equal(self, input_adtecedent, adtecedent):
        if(input_adtecedent.operator != adtecedent.operator):
            return False

        if(self.VariablesIsSatisfied(input_adtecedent_Variables=input_adtecedent.variables,
                                     adtecedent_scope=self.scope[order[:len(input_adtecedent.variables)]]) == False):
            return False

        return True

    def VariablesIsSatisfied(self, input_adtecedent_Variables, adtecedent_scope):
        '''
        判断规则的adtecedent中，各传入的变量是否和adtecedent一致，且在论域内。adtecedent是一个Assertion类型。
        :type: number, Individual, Set, Assertion
        :return: True or False
        '''
        # if (len(input_adtecedent_Variables.variables) != len(adtecedent.variables)):  # adtecedent
        #     return False

        for i in range(len(input_adtecedent_Variables)):
            input_item = input_adtecedent_Variables[i]
            item = adtecedent_scope[i]
            if(item[0] == '@'):
                pass #这就特殊符号的判断了

            elif (type(input_item) == type(item)):
                if (type(input_item) == Number or type(input_item) == Individual or type(input_item) == Set):
                    if(input_item.value != item.value):  # 暂时还没在scope里设置取值范围相关规定。不过数字嘛，应该相等就完了
                        return False
                elif(type(input_item) == bool):
                    if (input_item != item):
                        return False

            else:
                if(type(input_item) == Number): #估计没这种情况吧？
                    raise ValueError("变量类型是数字？")

                elif(type(input_item) == Individual):
                    if(type(item) == Set):
                        if(input_item.value not in item.value): #str不在set里
                            return False
                    else:
                        return False
                elif(type(input_item) == Set):
                    if (type(item) == Set):
                        for indiviual in input_item.value:
                            if(indiviual not in item.value):
                                return False
                    else:
                        return False
                else: #就剩下Assertion和bool了。
                    raise ValueError("emm...补代码吧，不够用了") #其实Assetion应该是允许支持的，但这时候就是推理部分了吧？先不管了。
                #至于bool...bool又没办法包含，不太可能两个变量的类型不一样