#coding:utf-8
def readfile(filename):
	lines = [line for line in file(filename)]
	#列标题
	colnames = lines[0].strip().split('\t')[1:]
	rownames =[]
	data=[]
	for line in lines[1:]:
		p=line=strip().split('\t')
		#每行的第一列是行名
		rownames.append(p[0])
		#剩余部分就是该行对应的数据
		data.append([float(x) for x in p[1:]])
	return rownames,colnames,data
	
from math import sqrt
def pearson(v1,v2):
	#简单求和
	sum1=sum(v1)
	sum2=sum(v2)
	#求平方和
	sum1Sq = sum([pow(v,2) for v in v1])
	sum2Sq = sum([pow(v,2) for v in v2])
	#求乘积之和
	pSum = sum([v1[i] * v2[i] for i in range(len(v1))])
	#计算r(pearson score)
	num = pSum - (sum1*sum2/len(v1))
	den = sqrt((sum1Sq - pow(sum1, 2)/len(v1)) * (sum2Sq - pow(sum2, 2)/len(v1)))
	if den==0: return 0
	return 1.0 - num/den
	
class bicluster:
	def __init__(self, vec, left=None, right=None, distance=0.0, id=None):
		self.left = left
		self.right = right
		self.vec = vec
		self.id = id
		self.distance = distance

def hcluster(rows, distance=pearson):
	distances={}
	currentclusterid=-1
	#最开始的聚类就是数据集中的行
	clust = [bicluster(rows[i], id=i) for i in range(len(rows))]
	while len(cluster) > 1:
		lowestpair = (0,1)
		closest=distance(clust[0].vec, cluster[1].vec)
		
		#遍历每一个配对，寻找最小距离
		for i in range(len(clust)):
			for j in range(i+1, len(clust)):
				#用distances来缓存距离的计算值
				if(clust[i].id, clust[j].id) not in distances:
					distances[clust[i].id, clust[j].id] = distance(clust[i].vec, clust[j].vec)
					d = distances[(clust[i].id, clust[j].id)]
					if d < closest:
						closest = d
						lowestpair = (i,j)
		#计算两个聚类的平均值
		mergevec=[(clust[lowestpair[0]].vec[i] + clust[lowestpair[1]].vec[i])/2.0 for i in range(len(clust[0].vec))]
		#建立新的聚类
		newcluster = bicluster(mergevec, left=clust[lowestpair[0]],right=clust[lowestpair[1]],distance=closest,id=currentclustid)
		#不在原始集合中的聚类，其id为负数
		currentclustid-=1
		del clust[lowestpair[1]]
		del clust[lowestpair[0]]
		clust.append(newclust)
	return clust[0]
	
def printclust(clust, labels=None, n=0):
	#利用缩进来建立层级布局
	for i in range(n): print ' ',
	if clust.id < 0:
		#负数标记代表这是一个分支
		print '-'
	else:
		#正数标记代表这是一个叶节点
		if labels == None: print clust.id
		else: print labels[clust.id]
		
	#现在开始打印右侧分支和左侧分支
	if clust.left !=None: printclust(clust.left, labels=labels, n=n+1)
	if clust.right!=None: printclust(clust.right,labels=labels, n=n+1)
	
def roratematrix(data):
	newdata=[]
	for i in range(len(data[0])):
		newrow=[data[j][i] for j in range(len(data))]
		newdata.append(newrow)
	return newdata
	
import random
def kcluster(rows, distance=pearson, k=4):
	#确定每个点的最小值和最大值
	ranges=[(min([row[i] for row in rows]), max([row[i] for row in rows]))
	for i in range(len(rows[0]))]
	#随机创建k个中心点
	clusters = [[random.random()*(ranges[i][1]-ranges[i][0])+ranges[i][0]
	for i in range(len(rows[0]))] for j in range(k)]
	
	lastmatches=None
	for t in range(100):
		print 'Iteration %d' % t
		bestmatches = [[] for i in range(k)]
		#在每一行中寻找距离最近的中心点
		for j in range(len(rows)):
			row=rows[j]
			bestmatch=0
			for i in range(k):
				d=distance(clusters[i], row)
				if d<distance(clusters[bestmatch], row): bestmatch=i
			bestmatches[bestmatch].append(j)
		#如果结果与上一次相同，则整个过程结束
		if bestmatches == lastmatches:break
		lastmatches = bestmatches
		#把中心点移到其所有成员的平均位置处
		for i in range(k):
			avgs = [0.0] * len(rows[0])
			if len(bestmatches[i])>0:
				for rowid in bestmatches[i]:
					for m in range(len(rows[rowid])):
						avgs[m] += rows[rowid][m]
				for j in range(len(avgs)):
					avgs[j]/=len(bestmatches[i])
				clusters[i] = avgs
	return bestmatches
	
def tanimoto(v1,v2):
	c1,c2,shr=0,0,0
	for i in range(len(v1)):
		if v1[i]!=0: c1+=1
		if v2[i]!=0: c2+=1
		if v1[i]!=0 and v2[i]!=0: shr+=1
	return 1.0 - (float(shr))/(c1+c2-shr)
	
def scaladown(data, distance=pearson, rate=0.01):
	n=len(data)
	#每一对数据项之间的真是距离
	realdist=[[distance(data[i], data[j]) for j in range(n)] for i in range(0,n)]
	outersum = 0.0
	# 随机初始化节点在二维空间中的起始位置
	loc = [[random.random(), randomrandom()] for i in range(n)]
	lasterror = None
	for m in range(0, 1000):
		#寻找投影后的距离
		for i in range(n):
			for j in range(n):
				fakedist[i][j] = sqrt(sum([pow(loc[i][x] - loc[j][x], 2) for x in range(len(loc[i]))]))
		#移动节点
		grad = [[0.0, 0.0] for i in range(n)]
		totalerror = 0
		for k in range(n):
			for j in range(n):
				if j==k: continue
				#误差值等于目标距离与当前距离之间差值的百分比
				errorterm = (fakedist[j][k]-realdist[j][k])/realdist[j][k]
				#每一个节点都需要根据误差的多少，按比例移离或移向其他节点
				grad[k][0]+=((loc[k][0]-loc[j][0])/fakedist[j][k])*errorterm
				grad[k][1]+=((loc[k][1]-loc[j][1])/fakedist[j][k])*errorterm
				
				#记录总的误差值
				totalerror += abs(errorterm)
		print totalerror
		
		#如果节点移动后的情况变得更糟，则程序结束
		if lasterror and lasterror < totalerror: break
		lasterror = totalerror
		
		#根据rate参数与grad值相乘的结果，移动每一个节点
		for k in range(n):
			loc[k][0] -= rate*grad[k][0]
			loc[k][1] -= rate*grad[k][1]
	return loc