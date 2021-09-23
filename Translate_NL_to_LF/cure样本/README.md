我们拿这个练个手，发现新的规则，就记录在[这里](https://github.com/msg-bq/Fake-news/blob/main/Translate_NL_to_LF/Pseudo_Specification.md)

第一次我们就以熟悉内容为主。师兄师姐你们各拿五个尝试一下，以此来评估下我是不是有没说清的地方。两点：1)涉及的规则有可能已经被总结进来了；2)有的样本可能会因为提取复杂，而本来就不打算总结规则。
不要求100%召回或精确率。所以表担心这个很难搞，是有基底的，并且太难做的我们本也不打算做。

涉及cure的样本如下(完成的在markdown格式下的括号内输入"X", 会显示为对勾)，师姐前五个，可心师兄6-10，剩下的我处理：

- [ ] 'social media posts recommend tonic water and zinc as a cure for a novel coronavirus infection as the drink contains quinine whose synthetic relative hydroxychloroquine is on trial as a covid19 treatment',
- [ ] 'israeli recipe for lemon and bicarbonate drink is a coronavirus cure',
- [ ] 'thousands of doctors say hydroxychloroquine cures coronavirus',
- [ ] 'romania developed a coronavirus vaccine able to cure white people only',
- [ ] 'lemon juice and bicarbonate mixture prevents and cures covid19 in israel',
- [ ] 'nevada governor steve sisolak has banned the use of an antimalaria drug that might help cure coronavirus',
- [ ] 'president donald trump will announce that a scientist finally found a vaccine to cure coronavirus',
- [ ] 'boiled orange peels with cayenne pepper are a cure for coronavirus',
- [ ] 'breathing air from a hair dryer or a sauna can prevent or cure covid19',
- [ ] 'huge results from breaking chloroquine study show 100 cure rate for patients infected with the coronavirus',
- [X] 'freshly boiled garlic water is a cure for coronavirus',
- [X] 'every election year has a disease coronavirus has a contagion factor of 2 and a cure rate of 997 for those under 50 it infects', **治愈率不算cure样本**
- [X] 'chlorine dioxide kits sold online under various mms names miracle mineral solution, miracle mineral supplement master, mineral solution will cure the coronavirus',**稍微有点不足，因为这一个词太长了**
- [ ] 'the new coronavirus can be cured by drinking one bowl of freshly boiled garlic water',
- [ ] 'coronavirus does not cause a runny nose is killed by temperatures above 26 degrees causes lung fibrosis within days of infection can be diagnosed by holding your breath for 10 seconds and can be cured in the early stages by drinking plenty of water',
- [X] 'knust students discover vaccine for coronavirus and cure patient in cte divoire', **不过这个是cure patient**，也还凑合算吧。这个如果patient前面不加the，cure会被识别为名词。这其实是个典型的可以常识知识增强的例子，就是说cure型patient不太可能是正确含义，动词才合理。但是吧，现阶段要不要做这个其实两说。因为效果其实太难预估了
- [X] 'a video posted on facebook claiming that chloroquine and azithromycin are proven cures of covid19', **proven会被错误识别，连到video上。尚未简单办法处理，先跳**
- [X] 'posts on social media claim that a spanish biological researcher called on international soccer stars cristiano ronaldo and lionel messi to find a cure for covid19 since they earn much more money than scientists',**无关样本**
- [X] 'there is no cure for covid19 no matter what the internet says', **这个没有作为主语的实体，要么不识别，要么单独写个None标签**
- [X] 'hydroxychloroquine cures this virus it just so happens this is the treatment used for radiation sickness',
- [X] 'thousands of doctors say hydroxychloroquine cures coronavirus',
- [ ] 'black cats in vietnam are being killed and consumed as a covid19 cure',
- [X] 'we cant make a vaccine that works for flu no vaccine for the respiratory syncytial virus rsv and we cant cure cancer yet somehow scientists can make a vaccine for covid19 in six months', **cure cancer，与cure样本无瓜**
- [X] 'hydroxychloroquine azithromycin and zinc cure covid19',
- [X] 'a group called americas frontline doctors are featured in viral video claiming hydroxychloroquine cures covid19',
- [X] 'stella immanuel claims that the drug combination of hydroxychloroquine zinc and azithromycin is a cure and preventative for covid19 and that people dont need to wear masks or practice physical distancing in a breitbart video featuring a group called americas frontline doctors',
- [X] 'fda warns of silver other bogus covid19 cures', **这个也基本不属于我们要处理的**
- [ ] 'hydroxychloroquine no covid cure, experts warn'

**注：目前打对勾的，尚未提取各词相关的修饰，只是提了中心词**
