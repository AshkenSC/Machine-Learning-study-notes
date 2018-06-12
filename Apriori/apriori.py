from numpy import *

# ����һ�������ݼ���Ϊʾ���Ͳ���
def loadDataSet():
    return [[1, 3, 4], [2, 3, 5], [1, 2, 3, 5], [2, 5]]

# ��������C1��C1�Ǵ�СΪ1�����к�ѡ��ļ���
def createC1(dataSet):
    # ����һ�����б�C1�������������в��ظ�����ֵ
    C1 = []
    # �������ݼ������н��׼�¼
    for transaction in dataSet:
        # ��ÿһ����¼��������¼��ÿһ��
        for item in transaction:
            # ���ĳ����Ʒ��û����C1�г��֣�������ӵ�C1�С�
            # ע�ⲻ�Ǽ򵥵������Ʒ��Ŀ������ÿ�����ֻ��������Ʒ��ĵ�Ԫ���б�
            # ����Ϊ��ÿ����Ʒ��Ŀ����һ�����ϣ����㷨������������Ҫ�����ϲ�������Python�޷�������Ԫ�ؼ��ϣ����ֻ���õ�Ԫ���б�
            if not [item] in C1:
                C1.append([item])
    # ���Դ��б�������򣬽�����ÿ��Ԫ��ӳ�䵽frozenset����������frozenset���б�
    C1.sort()
    # ��C1�е�ÿһ���һ�����伯�ϡ�frozenset��ָ�����������ļ��ϣ����û����ɸı��
    return map(frozenset, C1)

# ��C1����L1����ɨ�輯��C1���ж�C1�еĵ�Ԫ����Ƿ�������С֧�ֶ�Ҫ��
# ���������ɼ���L1��L1��Ԫ���໥��Ϲ���C2��C2�ٽ�һ�����˱�ΪL2
# �������������ݼ�����ѡ��б�����Ȥ�����С֧�ֶ�
def scanD(D, Ck, minSupport):
    # ����һ�����ֵ�
    ssCnt = {}
    # �������ݼ��е����н��׼�¼�Լ�C1�е����к�ѡ��
    for tid in D:
        for can in Ck:
            # �����ǰ��������C1�е�ĳ�������ǵ�ǰ��������ĳ�����׼�¼��һ���֣��������ֵ��ж�Ӧ�ļ���ֵ���˴��ֵ�ļ����Ǽ��ϣ���
            if can.issubset(tid):
                if not ssCnt.has_key(can): ssCnt[can]=1
                else: ssCnt[can] += 1
    numItems = float(len(D))
    retList = [] # ���б��洢������С֧�ֶ�Ҫ��ļ���
    supportData = {} # ���ֵ䣬�洢��Ƶ����Լ����Ƕ�Ӧ��֧�ֶ�
    # �����ֵ�SScnt�������������֧�ֶȡ����֧�ֶ�������С֧�ֶ�Ҫ�󣬾ͽ����ӵ�retList��
    for key in ssCnt:
        support = ssCnt[key]/numItems
        if support >= minSupport:
            retList.insert(0,key)
        supportData[key] = support
    # ����һ������֧�ֶ�ֵ���ֵ��Ա���
    return retList, supportData

# ����Ck
def aprioriGen(Lk, k):
    retList = []
    lenLk = len(Lk)
    for i in range(lenLk):
        for j in range(i+1, lenLk):
            L1 = list(Lk[i])[:k-2]; L2 = list(Lk[j])[:k-2]
            L1.sort(); L2.sort()
            # ���ǰk-2������ͬʱ�����������Ϻϲ�
            if L1==L2:
                retList.append(Lk[i] | Lk[j]) # �ϲ�����
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