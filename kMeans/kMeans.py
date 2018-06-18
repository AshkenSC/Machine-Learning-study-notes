# 导入numpy库，需要使用其中部分函数
from numpy import *

# 将文本文件存储的数据导入到列表中。文本文件每一行为tab分隔的浮点数
# 参数fileName为要导入的文件名
def loadDataSet(fileName):
    # 新建空列表dataMat，用于存储并返回最终数据格式化导入的结果
    dataMat = []
    # 打开名为fileName的文件，并将其变量fr中
    # 不能直接处理文件，要将其先打开后存在一个变量里
    # fr存储了打开但未处理的文本文件，还需进一步格式化存储在列表中
    fr = open(fileName)
    # 按行遍历打开的文件fr。readlines()函数读取fr文件的所有行
    for line in fr.readlines():
        # line.strip():删除当前行首尾的空白字符；
        # line.strip.split('\t')在删除首尾空白字符的基础上，按照tab分割字符串。\t表示tab字符
        # 将处理结果存储在curLine中
        curLine = line.strip().split('\t')
        # 上述curLine存储的只是分割后的字符串列表，每个元素还不是数值格式
        # 使用map(float, curLine)将其转换为float浮点型格式，并存储在fitLine中
        fltLine = map(float,curLine)
        # 将fitLine作为新元素添加到dataMat中
        dataMat.append(fltLine)
    # 函数返回最终结果dataMat
    return dataMat

# 计算两个向量之间的欧氏距离。输入参数为两个列表格式存储的向量，vecA和vecB
def distEclud(vecA, vecB):
    # 从内层到外层：power(a,n)：求a的n次方。如果a是列表，则分别求各元素n次方
    # sum(a)：求列表a各元素的和；sqrt(a)：求a的平方根
    return sqrt(sum(power(vecA - vecB, 2)))

# 为给定数据集构建一个包含k个随机质心的集合。随机质心必须在数据集边界内
# 参数：数据集dataSet，随机质心的数量k
def randCent(dataSet, k):
    # 读取数据集dataSet第二维的长度。（第一维为样本数，第二维为样本属性）
    n = shape(dataSet)[1]
    # TODO: centroids赋值待进一步理解
    # zeros((k, n))：初始化一个1*k*n的三维全0矩阵。注意k,n外面有两层括号。如果是k*n二维矩阵，就是zeros(k,n)
    # mat()：将列表转化为numpy矩阵格式。上述zeros创建了“矩阵”，但存储本质还是列表
    centroids = mat(zeros((k,n)))
    # 构建簇质心
    for j in range(n):
        # minJ存储了dataSet第j列元素中的最小值
        # dataSet[a:b, j]即取dataSet从a到b行的第j列元素。a,b不写即取第j列所有元素。加min即取这些元素最小值
        minJ = min(dataSet[:,j])
        #与上面类似，max(dataSet[:,j]得到第j列最大值。将其和minJ相减，得到j列取值范围
        rangeJ = float(max(dataSet[:,j]) - minJ)
        # 先看等号右边，从内而外分析
        # random.rand(k,1)返回一个k行1列的0-1范围随机数列表。再乘以rangeJ，即为0-rangeJ范围的随机数
        # 再加上minJ，最终minJ + rangeJ * random.rand(k,1)为一个k行1列的，取值范围在minJ到maxJ的随机数列表
        # 再将其用mat()处理，得到一个1*k*1的三维矩阵。
        # 由等式左边知道，这个矩阵作为质心的第j列
        centroids[:,j] = mat(minJ + rangeJ * random.rand(k,1))
    return centroids

# 共四个参数。两个必选：数据集和簇的数目；两个可选：计算距离和创建初始质心的函数
def kMeans(dataSet, k, distMeas=distEclud, createCent=randCent):
    # 获取dataSet第一个维度的大小，即dataSet里有多少数据点
    m = shape(dataSet)[0]
    # cluster assignment矩阵，用来存储每个点的簇分配结果
    # 包含两列，一列记录簇索引值，第二列存储误差（即当前点到簇质心的距离）
    clusterAssment = mat(zeros((m,2)))
    centroids = createCent(dataSet, k)
    clusterChanged = True
    while clusterChanged:
        clusterChanged = False
        for i in range(m):#for each data point assign it to the closest centroid
            minDist = inf; minIndex = -1
            for j in range(k):
                distJI = distMeas(centroids[j,:],dataSet[i,:])
                if distJI < minDist:
                    minDist = distJI; minIndex = j
            if clusterAssment[i,0] != minIndex: clusterChanged = True
            clusterAssment[i,:] = minIndex,minDist**2
        #print centroids
        for cent in range(k):#recalculate centroids
            ptsInClust = dataSet[nonzero(clusterAssment[:,0].A==cent)[0]]#get all the point in this cluster
            centroids[cent,:] = mean(ptsInClust, axis=0) #assign centroid to mean
    return centroids, clusterAssment