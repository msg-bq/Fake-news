from concept import BaseConcept
from Operator import ActionOperators

__all__ = ['Number', 'Individual', 'Set', 'Assertion']

class Number(BaseConcept):
    def __init__(self, value=None, name='', comments=''):
        super().__init__(value, name, comments)
        assert type(value) == int or float

class Individual(BaseConcept):
    def __init__(self, value=None, name='', comments=''):
        super().__init__(value, name, comments)
        assert type(value) == str

class Set(BaseConcept):
    '''
    用于实例化的concept，如COVID19_Cure
    '''
    def __init__(self, value=None, name='', comments=''):
        super().__init__(value, name, comments)
        assert type(value) == list


class BaseAssertion(object):
    def __init__(self, LHS=None, RHS=None):
        assert type(LHS) == ActionOperators #我一时间忘了周老师有无严格要求左式是Operator(X)的形式，
        # 不过至少转代码的时候强行设定这个，感觉不亏，也利于整齐
        self.LHS = LHS #为了整齐叭，用的时候主要用
        self.RHS = RHS

class Assertion(BaseConcept):
    def __init__(self, value=None, name='', comments=''):
        super().__init__(value, name, comments)
        assert type(value) == BaseAssertion
