# 设计思路

## 文件介绍
* concept.py 目前收录了Concept的母类BaseConcept
* variable_type.py 是继承BaseConcept写的concepts的数据类型(当然数据类型自身也是种concept)，同时也是作为参数的变量的数据类型。包括Number(数字型，类型为int或float)、Individual(此时定义为纯个体，仅限于单个元素，类型为字符串)、Set(一至多个元素的集合，类型为数组)、Assertion(断言本身也可以作为参数带入，类型是定义的BaseAssertion类)
* Pre_concepts.py 是基于variable_type.py来具体写我们设了哪些concepts(除数据类型外的其他concepts，如COVID19_Cure)
* Operator.py 暂时包括了operator和rules的母类和一些基本的class，回头打算把operator和rule分在两个地方的

## 设计逻辑
### 基本逻辑
  断言逻辑应该是一种范畴的思想吧，所以所有的东西我都打算写成class，显式地以对象的样子来边写，虽然说是说python内部实现都是对象。
  concept比较简单，单纯地用对象的一个变量value，记录它的值就行。只有当它是Assertion时，才会因为python不提供记录等式的数据结构(不打算用str表示)，所以单独写个BaseAssertion类，以存储断言式的左右式。
  
  
### 细节
* BaseConcept就一个value，用于记录具体包含什么。Number记录int或float，Individual记录str，Set记录list，这三个是python自带的。但Assertion记录
