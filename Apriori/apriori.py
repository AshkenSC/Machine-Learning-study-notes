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

# 从C1生成L1。在扫描集合C1后，判断C1中的单元素项集是否满足最小支持度要求。
# 满足的项集构成集合L1，L1中元素相互组合构成C2，C2再进一步过滤变为L2
# 三个参数：数据集、候选项集列表、感兴趣项集的最小支持度
def scanD(D, Ck, minSupport):
    # 创建一个空字典
    ssCnt = {}
    # 遍历数据集中的所有交易记录以及C1中的所有候选集
    for tid in D:
        for can in Ck:
            # 如果当前遍历到的C1中的某条集合是当前遍历到的某条交易记录的一部分，则增加字典中对应的计数值（此处字典的键就是集合）。
            if can.issubset(tid):
                if not ssCnt.has_key(can): ssCnt[can]=1
                else: ssCnt[can] += 1
    numItems = float(len(D))
    retList = [] # 空列表，存储满足最小支持度要求的集合
    supportData = {} # 空字典，存储最频繁项集以及它们对应的支持度
    # 遍历字典SScnt，计算所有项集的支持度。如果支持度满足最小支持度要求，就将项集添加到retList中
    for key in ssCnt:
        support = ssCnt[key]/numItems
        if support >= minSupport:
            retList.insert(0,key)
        supportData[key] = support
    # 返回一个包含支持度值的字典以备用
    return retList, supportData

# 创建Ck
def aprioriGen(Lk, k):
    retList = []
    lenLk = len(Lk)
    for i in range(lenLk):
        for j in range(i+1, lenLk):
            L1 = list(Lk[i])[:k-2]; L2 = list(Lk[j])[:k-2]
            L1.sort(); L2.sort()
            # 如果前k-2个项相同时，将两个集合合并
            if L1==L2:
                retList.append(Lk[i] | Lk[j]) # 合并集合
    return retList


def apriori(dataSet, minSupport = 0.5):
    C1 = createC1(dataSet)
    D = map(set, dataSet)
    L1, supportData = scanD(D, C1, minSupport)
    L = [L1]
    k = 2
    while (len(L[k-2]) > 0):
        Ck = aprioriGen(L[k-2], k)
        Lk, supK = scanD(D, Ck, minSupport)#scan DB to get Lk
        supportData.update(supK)
        L.append(Lk)
        k += 1
    return L, supportData