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

def randCent(dataSet, k):
    n = shape(dataSet)[1]
    centroids = mat(zeros((k,n)))
    for j in range(n):
        minJ = min(dataSet[:,j])
        rangeJ = float(max(dataSet[:,j]) - minJ)
        centroids[:,j] = mat(minJ + rangeJ * random.rand(k,1))
    return centroids