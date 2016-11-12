#coding:utf-8
from random import random,randint,choice
#玩家1是赢家，返回0， 玩家2是赢家，返回1 平局，返回-1
def gridgame(p):
	#游戏区域大小
	max = (3,3)
	#记住每位玩家的上一步
	lastmove=[-1,-1]
	#记住玩家的位置
	location= [[randint(0, max[0]), randint(0, max[1])]]
	#将第二玩家放在离第一玩家足够远的地方
	location.append([(location[0][0] + 2)%4, (location[0][1] + 2)%4])
	#打成平局前最大移动步数50
	for o in range(50):
		#针对每位玩家
		for i in range(2):
			locs = location[i][:]+location[1-i][:]
			locs.append(lastmove[i])
			move = p[i].evaluate(locs)%4
			#如果同一行中朝同一个方向移动了两次，判定为你输
			if lastmove[i]==move: return 1-i
			lastmove[i] = move
			if move==0:
				location[i][0] -= 1
				#限制游戏区域
				if location[i][0] < 0: location[i][0]=0
			if move==1:
				location[i][0]+=1
				if location[i][0]>max[0]:location[i][0]=max[0]
			if move==2:
				location[i][1]-=1
				if location[i][1]<0:location[i][1]=0
			if move==3:
				location[i][1]+=1
				if location[i][1]>max[1]:location[i][1]=max[1]
			#如果抓住了对方玩家，判定为你赢
			if location[i]==location[1-i]:return i
		return -1
		
def tournament(pl):
	#统计失败的次数
	losses = [0 for p in pl]
	#每位玩家都和其他玩家对抗
	for i in range(len(pl)):
		for j in range(len(pl)):
			if i==j: continue
		#谁是胜利者
		winner = gridgame([pl[i],pl[j]])
		#失败得2分，打平得1分
		if winner==0:
			losses[j]+=2
		elif winner==1:
			losses[i]+=2
		elif winner==-1:
			losses[i]+=1
			losses[j]+=1
			pass
	#对结果进行排序
	z=zip(losses,pl)
	z.sort()
	return z
	
class humanplayer:
	def evaluate(self, board):
		#得到自己的位置和玩家的位置
		me=tuple(board[0:2])
		others=[tuple(board[x:x+2]) for x in range(2, len(board)-1, 2)]
		#显示游戏区域
		for i in range(4):
			for j in range(4):
				if (i,j)==me:
					print 'O',
				elif (i,j) in others:
					print 'X',
				else:
					print '-',
			print
		
		#显示上一步
		print 'Your last move was %d' % board[len(board) -1]
		print ' 0'
		print '2 3'
		print ' 1'
		print 'Enter move: ',
		#不论用户输入什么内容，均直接返回
		move = int(raw_input())
		return move