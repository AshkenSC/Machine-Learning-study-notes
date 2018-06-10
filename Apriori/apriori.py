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

def scanD(D, Ck, minSupport):
    ssCnt = {}
    for tid in D:
        for can in Ck:
            if can.issubset(tid):
                if not ssCnt.has_key(can): ssCnt[can]=1
                else: ssCnt[can] += 1
    numItems = float(len(D))
    retList = []
    supportData = {}
    for key in ssCnt:
        support = ssCnt[key]/numItems
        if support >= minSupport:
            retList.insert(0,key)
        supportData[key] = support
    return retList, supportData