# 设计思路

## 文件介绍
* concept.py 目前收录了Concept的母类BaseConcept
* variable_type.py 是继承BaseConcept写的concepts的数据类型(当然数据类型自身也是种concept)，同时也是作为参数的变量的数据类型。包括Number(数字型，类型为int或float)、Individual(此时定义为纯个体，仅限于单个元素，类型为字符串)、Set(一至多个元素的集合，类型为数组)、Assertion(断言本身也可以作为参数带入，类型是定义的BaseAssertion类)
* Pre_concepts.py 是基于variable_type.py来具体写我们设了哪些concepts(除数据类型外的其他concepts，如COVID19_Cure)
* Operator.py 暂时包括了operator和rules的母类和一些基本的class，回头打算把operator和rule分在两个地方的

## 设计逻辑
### 基本逻辑
  断言逻辑应该是一种范畴的思想吧，所以所有的东西我都打算写成class，显式地以对象的样子来边写，虽然说是说python内部实现都是对象。
  
  Concept比较简单，单纯地用对象的一个变量value，记录它的值就行。只有当它是Assertion时，才会因为python不提供记录等式的数据结构(不打算用str表示)，所以单独写个BaseAssertion类，以存储断言式的左右式。
  
  Operator由于需要和rule结合，且无法从形式上良定义，所以我认为有这样两个问题需要解决：
  
  * 可执行。既然不是从形式上定义，那可执行就意味着依相关的rules，获取consequent或获取consequent的右式。前者是指，如"X导致严重疾病 → X有害"这样的蕴含推理，那"X导致严重疾病"此时，Lead这个operator，配上合适的变量，执行的结果应该是对应的consequent这个整体，它可以是任何上面设定好的数据类型。后者是指，如果前件为空，则只要与这个operator相关的rule，必然可以直接执行consequent内的等式(这种情况下consequent一定写的是一个Assertion类型的等式，这是我重构rule时，为适应蕴含所做的书写rule的基本要求。这个如果我当时没说清的话，你告我一声咱俩重新聊一下)，那么此时将会执行获取"变量属于对应scope"的那条规则所对应的右式。

  * 可比对。adtecedent是否吻合，scope限制是否满足或者满足哪个。adtecedent可以直接设定数据类型必为Assertion。这样的假设，好处是更明了，不需要判一大片数据类型；不足是会遗漏一些蕴含，大家都是范畴嘛，所以concept也可以有蕴含，或者从属关系(A属于B)也可能蕴含着(A的)一些推论等。但是我觉得没关系，一是咱目前的场景应该没这种的。二是偶尔adtecedent非Assertion的蕴含，我觉得可以通过设立新的operator来涵盖，比如说从属关系意味着A有B的一些性质，那这个也可以把从属当成一个operator，就成了"属于(A, B) = True → B的xxx性质"。当然这个例子可能不是很难，依赖编程解决也一样。

  为了解决上述问题，则有如下coding的逻辑：
  * 为了执行，那在我们这个场景中，operator本身的定义是文字型定义，所以多数时候它不是可以直接执行的，而是与各个rule相关联的执行。这个类暂时是BaseOperator(可能会和ActionOperators合并)，类中记录了参数、以及相关的规则(相关是指，此Operator出现在某条rule的adtecedent或consequent的左式(adtecedent为空)中)。并书写__call__来令其可执行，返回所有可匹配的rule能生成的新facts(此类尚未写完)。这样的话，"执行"就被定义为"遍历所有此operator可以蕴含(做adtecedent推consequent)或可以"="(adtecedent为空)的rule"，返回consequent或consequent的右式。__init__里设定好涉及的rule、传入参数的数量和定义域，在__call__时传入参数(包括允许传入参数和Assertion的右式，这样的话才能支持所有的数据类型)。继承ActionOperators这个母类，而继续定义的新class(表示operator)，都是预定义好的，后期是不动的，除非rule有扩充。
  * Assertion左式可以是一个Operator(X)，所以需要一个类，它可以存储Operator和已知变量具体值的X，这个类并非是预定义的，而是明确写出来变量的值的。所以ActionOperators包括具体的变量，以及需要在__init__里定义一个可以包含"继承于BaseOperator而预定义的Operator"的变量，以便以后推理时调用。
  * 类似上一条的两种情况，匹配也是分匹配adtecedent和当adtecedent为空时，匹配consequent的左式。前者因为默认必是Assertion类型，直接分别匹配左右式即可。后者，实际就是匹配类型为Assertion的consequent的左式。也就是说，这两种情景，都是匹配一端，本质逻辑是一样的。而这一端，要么是Assertion，那就是继续递归，直到需要匹配的是括号内的变量。那这时候就是要么完全相等，要么是从属关系。根据不同的类型，各自判一下就行。判别逻辑是通用的，写在BaseRule这个母类里。
  
  Rule就没什么说的了，按照原本的写就好了。需要的数据类型或operator相关的一些类，也在上述过程中定义好了。需要的函数就是上面coding逻辑的第三条。然后还有个需要单独写的，是自己设一些符号，代表特定的未定义concept或其他需求。比如"@ALL"代表全集，"@Default:XXX 代表默认参数"，"@Dict:XX 代表这是个字典，而不是普通的class concept，可以直接hash而不是遍历"等等，根据需求增加。
  
### 细节
* BaseConcept就一个value，用于记录具体包含什么。Number记录int或float，Individual记录str，Set记录list，这三个是python自带的。但Assertion记录
