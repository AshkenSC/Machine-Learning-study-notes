import matplotlib.pyplot as plt

# define text and arrow format
decisionNode = dict(boxstyle="sawtooth", fc='0.8')
leafNode = dict(boxstyle='round4', fc='0.8')
arrow_args = dict(arrowstyle='<-')

# plot note with arrow
def plotNode(nodeTxt, centerPt, parentPt, nodeType):
    createPlot.ax1.a

def createPlot():
    fig = plt.figure(1, facecolor='white')
    fig.clf()
    createPlot.ax1 = plt.subplot(111, frameon=False)
    plotNode("decision node", (0.5, 0.1), (0.1, 0.5))