from numpy import *

# 载入一个简单数据集作为示例和测试
def loadDataSet():
    return [[1, 3, 4], [2, 3, 5], [1, 2, 3, 5], [2, 5]]


# 构建集合C1。C1是大小为1的所有候选项的集合
def createC1(dataSet):
    # 创建一个空列表C1，用来储存所有不重复的项值
    C1 = []
    # 遍历数据集中所有交易记录
    for transaction in dataSet:
        # 对每一条记录，遍历记录中每一项
        for item in transaction:
            # 如果某个物品项没有在C1中出现，则将其添加到C1中。
            # 注意不是简单地添加物品项目，而是每次添加只包含该物品项的单元素列表。
            # 这是为了每个物品项目构建一个集合，在算法后续处理中需要做集合操作。但Python无法创建单元素集合，因此只能用单元素列表
            if not [item] in C1:
                C1.append([item])
    # 最后对大列表进行排序，将其中每个元素映射到frozenset（），返回frozenset的列表
    C1.sort()
    # 对C1中的每一项构建一个不变集合。frozenset是指被“冰冻”的集合，即用户不可改变的
    return map(frozenset, C1)

# 从C1生成L1。L1为从C1过滤出的所有满足最小支持度的单元素项集
# L1中元素相互组合构成待过滤的所有二元素项集C2。C2经过滤后，保留满足最小支持度的二元素项集，构成L2
# 三个参数：数据集、候选项集列表、感兴趣项集的最小支持度
def scanD(D, Ck, minSupport):
    # 创建一个空字典
    ssCnt = {}
    # 遍历数据集中的所有交易记录
    for tid in D:
        # 遍历C1中的所有候选集
        for can in Ck:
            # 如果当前遍历到的C1中的某条集合是当前遍历到的某条交易记录的一部分，则增加字典中对应的计数值（此处字典的键就是集合）。
            # issubset(tid):顾名思义，用于判断当前项集can是否是tid的子集
            if can.issubset(tid):
                # ssCnt.has_key(can)表示检查字典ssCnt里是否有键can。
                # 这个if语句表示，如果字典里没有当前候选项集can，则新增一个键，并赋初值1
                # 如果已经有了can这个键，则将原来的计数值+1
                if not ssCnt.has_key(can): ssCnt[can]=1
                else: ssCnt[can] += 1
    numItems = float(len(D))  # len(D)返回数据集D的大小。使用numItems存储之
    retList = [] # 空列表，存储满足最小支持度要求的集合
    supportData = {} # 空字典，存储最频繁项集以及它们对应的支持度
    # 遍历字典SScnt，计算所有项集的支持度。如果支持度满足最小支持度要求，就将项集添加到retList中
    for key in ssCnt:
        # 计算当前项集key的支持度
        # （项集目前存储在字典里，键是项集，对应值是出现次数）
        support = ssCnt[key]/numItems
        # 如果当前项集支持度大于最小支持度
        if support >= minSupport:
            # 将当前项集添加到待输出列表retList头部
            # insert函数用于向列表中添加元素。第一个参数为元素位置，第二个参数为元素内容
            retList.insert(0,key)
        supportData[key] = support
    # 返回一个从Cn过滤出来的，满足最小支持度的项集列表retList
    # 返回一个包含支持度值的字典supportData以备用
    return retList, supportData

# 功能：创建并输出候选项集Ck
# 两个参数：频繁项集列表Lk，项集元素个数k
def aprioriGen(Lk, k):
    retList = []        # 创建一个空列表
    lenLk = len(Lk)     # 计算频繁项集列表Lk中的元素数目
    # 两层嵌套循环，实现Lk中元素的两两比较
    # 外层循环确定被比较的两个元素其中之一
    for i in range(lenLk):
        # 在外层确定元素i作为其中一个比较对象时，内层从i+1一直遍历到末尾，为另一个比较元素
        # 例如外层i=0时，内层循环从1，2，3...直到n。即将0元素分别与1~n比较
        # 外层执行到第二层时，i=1，内层则从2，3，...直到n，即将1元素分别与2,3...n比较
        for j in range(i+1, lenLk):
            # list(Lk[i])表示将Lk[i]转化为列表。
            # 后面跟[:k-2}表示取这个列表的前k-2项（是0到k-1，注意左闭右开）
            L1 = list(Lk[i])[:k-2]; L2 = list(Lk[j])[:k-2]
            # 将列表L1, L2分别排序。
            L1.sort(); L2.sort()
            # 比较L1和L2，注意它们只存储了前k-2项
            # 当L1==L2，即前k-2个项相同时，将Lk[i] Lk[j]两个集合合并
            '''
            为什么是比较前k-2个元素？例如，当利用0，1，2构建01，02，12时，实际上是对单元素项集的组合。
            如果想利用01，02，12创建三元素项集，这样将集合两两简单合并，得到012，012，012。
            同样结果重复了三次，但我们下面还要扫描三元素项集列表得到不重复的结果。这样增加了不必要的运算
            
            如果改进方法，只比较01，02，12的第一个元素，只对第一个元素相同的集合求并操作，即只并01，02，因为他们第一个元素相同
            这时，我们将得到唯一的一个结果012，并且只进行了一次操作。这就不用像上面方法一样剔除重复值了
            '''
            if L1==L2:
                # 将Lk[i]和Lk[j]合并。运算符|表示对集合的“并”操作
                retList.append(Lk[i] | Lk[j])
    return retList

# 两个参数：数据集，最小支持度（这里默认设置为0.5）
# 功能：生成候选项集列表
def apriori(dataSet, minSupport = 0.5):
    # 使用createC1函数，根据输入的数据集dataSet先创建一个C1
    C1 = createC1(dataSet)
    # 将C1转化为集合列表D。使用map函数将set映射到dataSet列表中的每一项
    D = map(set, dataSet)
    # scanD函数返回过滤后的单元素项集L1和支持度数据supportData
    L1, supportData = scanD(D, C1, minSupport)
    # L是最终输出的所有满足最小支持度的项集构成的列表。
    # 其中L1列表包含所有满足要求的单元素项集，作为第一个子列表添加到L中
    # 接下来，满足最小支持度的双元素项集列表L2，三元素项集列表L3…都将陆续添加到L中
    L = [L1]
    k = 2
    # 使用循环来实现1)创建Ck，2)过滤得到Lk，3)将Lk添加到最后结果列表L中的操作
    # 上面一行k=2就是让循环从C2开始
    while (len(L[k-2]) > 0):
        # 创建未过滤k元素项集列表Ck
        Ck = aprioriGen(L[k-2], k)
        # 将Ck过滤得到符合最小支持度要求的k元素项集列表Lk
        Lk, supK = scanD(D, Ck, minSupport)
        # 更新支持度数据
        supportData.update(supK)
        # 将过滤得到的Lk添加到最后结果列表L中
        L.append(Lk)
        k += 1
    return L, supportData