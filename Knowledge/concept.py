
__all__ = ['BaseConcept']

class BaseConcept(object):
    def __init__(self, value=None, name='', comments=''):
        self.value = value  # 值，用列表存
        self.name = name  # 概念名/概念类型
        self.comments = comments

    # def #遍历需求

