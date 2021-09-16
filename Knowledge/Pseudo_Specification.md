# 设计思路
## 文件介绍
* concept.py 目前收录了Concept的母类BaseConcept
* variable_type.py 是继承BaseConcept写的concepts的数据类型(当然数据类型自身也是种concept)，同时也是作为参数的变量的数据类型。包括number(数字型，类型为int或float)、Individual(个体，仅限于单个元素，类型为字符串)、Set(一至多个元素的集合，类型为数组)、Assertion(断言本身也可以作为参数带入，类型是定义的BaseAssertion类)
* Pre_concepts.py 是基于variable_type.py来具体写我们设了哪些concepts(除数据类型外的其他concepts，如COVID19_Cure)
* Operator.py 暂时包括了operator和rules的母类和一些基本的class，回头打算把operator和rule分在两个地方的
