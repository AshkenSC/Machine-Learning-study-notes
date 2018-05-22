from math import log
import opereator

# Create a simple data set of water animals for the tests
def createDataSet():
    dataSet = [[1, 1, 'yes'],
               [1, 1, 'yes'],
               [1, 0, 'no'],
               [0, 1, 'no'],
               [0, 1, 'no']]
    labels = ['no surfacing','flippers']
    #change to discrete values
    return dataSet, labels

# Calculate Shannon entropy of the data set
def calcShannonEnt(dataSet):
    numEntries = len(dataSet)
    labelCounts = {}
    for featVec in dataSet:
    # the the number of unique elements and their occurance
        currentLabel = featVec[-1]
        if currentLabel not in labelCounts.keys(): labelCounts[currentLabel] = 0
        labelCounts[currentLabel] += 1
    shannonEnt = 0.0
    for key in labelCounts:
        prob = float(labelCounts[key])/numEntries
        shannonEnt -= prob * log(prob,2) #log base 2
    return shannonEnt

# Split given data set using given feature with certain value
def splitDataSet(dataSet, axis, value):
    retDataSet = []
    for featVec in dataSet:
        if featVec[axis] == value:
            reducedFeatVec = featVec[:axis]     #chop out axis used for splitting
            reducedFeatVec.extend(featVec[axis+1:])
            retDataSet.append(reducedFeatVec)
    return retDataSet

# Select among features
def chooseBestFeatureToSplit(dataSet):
    numFeatures = len(dataSet[0]) - 1      #the last column is used for the labels
    baseEntropy = calcShannonEnt(dataSet)
    bestInfoGain = 0.0; bestFeature = -1
    for i in range(numFeatures):        #iterate over all the features
        featList = [example[i] for example in dataSet]#create a list of all the examples of this feature
        uniqueVals = set(featList)       #get a set of unique values
        newEntropy = 0.0
        for value in uniqueVals:
            subDataSet = splitDataSet(dataSet, i, value)
            prob = len(subDataSet)/float(len(dataSet))
            newEntropy += prob * calcShannonEnt(subDataSet)
        infoGain = baseEntropy - newEntropy     #calculate the info gain; ie reduction in entropy
        if (infoGain > bestInfoGain):       #compare this to the best gain so far
            bestInfoGain = infoGain         #if better than current best, set to best
            bestFeature = i
    return bestFeature                      #returns an integer

def majorityCnt(classList):
    classCount={}
    for vote in classList:
        # keys()返回字典里所有键。本if句功能：如果字典classList中没有vote这个键
        # 就新建一个键vote，并赋初值0
        if vote not in classCount.keys(): classCount[vote] = 0
        classCount[vote] += 1
    # sorted()返回一个新的排序好的列表。第一个参数表示根据字典classCount产生的迭代器，以遍历classCount
    # 第二个参数operator.itemgetter(1)表示根据classCount每个成员的第二个元素进行排序。注意classCount
    # 是一个字典，因此每个成员的第一个元素是键，第二个元素是值
    # 第三个参数，reverse=True表示结果降序排列。如果为False则表示结果升序排列
    sortedClassCount = sorted(classCount.iteritems(), key=operator.itemgetter(1), reverse=True)
    return sortedClassCount[0][0]

def createTree(dataSet,labels):
    classList = [example[-1] for example in dataSet]
    if classList.count(classList[0]) == len(classList):
    # classList.count(classList[0])就是数据划分列表classList下第一个类别的元素的数量。
    # 如果第一个类别的元素的数量等于整个划分列表classList的大小，说明所有元素都只属于第一类
    # 说明该划分下的样本类别已经完全相同。
        return classList[0]
    if len(dataSet[0]) == 1:
    # len(dataSet[0]) == 1，说明只剩下一个属性了，不能再根据属性进一步划分了
    # （回忆前面每进行一次划分，都会删去那次划分所依据的特征）。
    # 但是现在这个划分下面仍然有一个以上类别的样本。因此根据前述的“多数表决”原则，由数量最多的样本确定这个叶子结点的类别。
        return majorityCnt(classList)
    # chooseBestFeatureToSplit(dataSet)是返回dataSet里划分效果最好的特征列序号。
    # 将它的值存放在变量bestFeat里，作为参数列表labels的下标
    bestFeat = chooseBestFeatureToSplit(dataSet)
    # 数据集dataSet只是单纯的将属性向量数值化后的列表
    # 而labels列表则包含了对每个属性列对应的文本化描述标签，后面制作图表时方便理解说明
    # 这样，labels[bestFeat]表示划分效果最好的那一列特征对应的标签文本描述，将它存放在变量bestFeatLabel中。
    bestFeatLabel = labels[bestFeat]
    # myTree：一个字典，当前里面只有一个键值对。
    # 其中，键为上面求出的最佳划分特征之标签bestFeatLabel
    # 而其对应值为另一个字典。当前这个字典为空，后面会再递归调用createTree函数在这个空字典里创造新的嵌套字典。
    myTree = {bestFeatLabel:{}}
    # 删除特征标签列表里对应着最优特征列（bestFeat）的标签，因为它已经被用于划分过了，后面不能再用来继续划分。
    del(labels[bestFeat])
    # 和前面类似，语句[example[ bestFeat] for example in dataSet]表示遍历数据集dataSet里所有样本，并将它们的第bestFeat列的元素依次存放在列表featValues里。
    featValues = [example[bestFeat] for example in dataSet]
    # 把最优划分特征列的所有元素存放在featValues里以后，通过set(featValues)函数，取其中所有不相同的值，并将它们存储在集合类型变量uniqueVals里。
    uniqueVals = set(featValues)
    # 对于字典uniqueVal中每个元素，即对于每个不同的取值：
    # 首先，创建一个子标签列表，包含当前标签列表的所有元素；
    # 然后，对myTree[ bestFeatLabel][ value]赋值。赋值由递归调用createTree函数来完成。
    # 如果调用createTree后得到的划分下面所有样本类别完全相同（前述注释情况1），或者已经不能再进一步划分（前述注释情况2），则createTree会返回一个具体的“类别号-类别标签”键值对；
    # 否则还会创建一个字典，这时就形成了嵌套。
    for value in uniqueVals:
        subLabels = labels[:]       #copy all of labels, so trees don't mess up existing labels
        myTree[bestFeatLabel][value] = createTree(splitDataSet(dataSet, bestFeat, value),subLabels)
    return myTree