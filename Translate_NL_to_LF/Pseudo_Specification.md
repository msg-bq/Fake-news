此文件同样用于记录代码逻辑，不过会比modeling部分的简单一些

# 依存关系
## cure样本
### 前言
建树和用规则抽取，其实是差不多的事情。我说建树，无非也就是想着将A治疗B或者A是B的治疗方法这类三元组形式的成分，变成一个父节点和两个子节点的树，直接从里面拿就行。所以不建这棵树，只是先从里面取这样的三元组，其实也是一回事儿嘛

建个树呢，好处是好看，规整。弊端呢，就是不灵活。就像刚才我说一个父节点两个子节点，那对于主谓宾结构来说，谓语动词是中心词，它父节点，其他两个是左右子节点，这个看起来挺舒服。
可是对于"A是B的治疗方法"，这时候is是中心词，A是主语，cure是一个be动词后的那个词，表属性。我们想要的B，其实应该是cure的修饰词，是cure的间接宾语。这时候is是父节点，A是子节点，cure是子节点，B是cure的子节点。那这棵树还好不好看，其实也两说哈。

而如果不建树，那就是写规则。对于A治疗B的样本，没话说，三个元素提取出来，提取做动词的cure，以及cure的主语宾语，这就是一条规则。
对于A是B的治疗方法，提取做名词的cure，放在动词的位置，提取cure的中心词is的主语作为主语，cure的宾语作为宾语，就是条新规则。

### 建树规则
**（考虑到我们是多人协作，建树的话代码是交融在一起的，因为最终就一个完整的建树流程。一旦没弄好就很麻烦，所以暂时先不这么干，先写成规则的形式。日后有需要再重构代码）**

首先，依存关系树是中心词指向父节点的，我们把它反向指到子节点舒服一点。
然后，conj，应当与cc前的中心词，共享主语和宾语等指向。
第三，如果conj，也有自己的主语宾语等某个成分的话，那就不和前面的中心词共享成分了。

### 抽取规则（目前只看这里就行）
**提取出来的规则，都要在这里以书面形式介绍。**

一、cure样本
1. cure做动词的规则
   1. cure的主动句（函数名VB_1）：[代码1（抽取全面）](https://github.com/msg-bq/Fake-news/blob/main/Translate_NL_to_LF/DSP.py#L184)、[代码2（格式整齐）](https://github.com/msg-bq/Fake-news/blob/main/Translate_NL_to_LF/DSP-new.py#L8)
      1. 如果cure的主语和直接宾语均存在，则直接提取nsubj和dobj。 
      2. 如果主语不存在，且cure的依存关系是conj，则向上寻找cure的head，使用第一个有主语的head的nsubj；如果宾语不存在，且存在某个词以conj的依存关系指向cure，则向下寻找cure的conj，使用第一个有直接宾语的子节点的dobj。
      
      3. 如果上述仍找不到，认为规则无法覆盖。
      
      **注：代码中其实还有prep+pobj这种间接宾语的部分。不过我后来想了想，cure是及物的，正常应该不会有间接宾语。就跳过了**。 

2. cure做名词的规则
   1. A是治疗方法为了B：[代码](https://github.com/msg-bq/Fake-news/blob/main/Translate_NL_to_LF/DSP-new.py#L47)
   
      1. 提取"主语+be动词+cure(NOUN)+介词+间接宾语"
   
      2. 并要求be动词(实践中是直接选取cure的父节点)，与cure的关系是attr。
   
      3. 主语部分包括"nsubj"和"expl"。前者是正常主语，后者是there be句型的there
   
   2. A是B的治疗方法：[代码](https://github.com/msg-bq/Fake-news/blob/main/Translate_NL_to_LF/DSP-new.py#L91)
      
      提取"主语+be动词+cure的修饰词+cure"。其余同上。
   
3. cure做被动句的规则：[代码](https://github.com/msg-bq/Fake-news/blob/main/Translate_NL_to_LF/DSP-new.py#L131)
   
   提取"主语-be动词(依存关系auxpass表被动)-cured-by-间接宾语"
