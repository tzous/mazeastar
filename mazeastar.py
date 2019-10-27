# -*- coding: UTF-8 -*-

# Filename : mazeastar.py
# 并查集生成迷宫，并且利用AStar算法自动解迷宫
#

import random

# 并查集生成迷宫
aa = 14
tree = []  # 节点地图
isling = []  # 节点连通关系
for i in range(0, aa):
    ta = []
    for j in range(0, aa):
        ta.append(-1)  # 初始值为-1
    tree.append(ta)

for i in range(0, aa * aa):
    tb = []
    for j in range(0, aa * aa):
        tb.append(-1)  # 初始值为-1
    isling.append(tb)


def getnei(a):  # 获得邻居号，上下左右四个节点  random
    x = int(a / aa)  # 要精确成整数
    y = a % aa
    mynei = []  # 储存邻居
    if x - 1 >= 0:
        mynei.append((x - 1) * aa + y)  # 上节点
    if x + 1 < aa:
        mynei.append((x + 1) * aa + y)  # 下节点
    if y - 1 >= 0:
        mynei.append(x * aa + y - 1)  # 左节点
    if y + 1 < aa:
        mynei.append(x * aa + y + 1)  # 右节点
    ran = random.randint(0, len(mynei) - 1)

    return (mynei[ran])


def search(a):  # 找到根节点
    if tree[int(a / aa)][a % aa] > 0:  # 说明是子节点
        return search(tree[int(a / aa)][a % aa])
    else:
        return a


def union(a, b):  # 合并
    a1 = search(a)  # a根
    b1 = search(b)  # b根

    if a1 != b1:
        if tree[int(a1 / aa)][a1 % aa] < tree[int(b1 / aa)][b1 % aa]:  # 这个是负数()
            tree[int(a1 / aa)][a1 % aa] += tree[int(b1 / aa)][b1 % aa]  # 个数相加  注意是负数相加
            tree[int(b1 / aa)][b1 % aa] = a1  # b树成为a树的子树，b的根b1直接指向a，值>0
        else:
            tree[int(b1 / aa)][b1 % aa] += tree[int(a1 / aa)][a1 % aa]
            tree[int(a1 / aa)][a1 % aa] = b1  # a所在树成为b所在树的子树，值>0


while search(0) != search(aa * aa - 1):  # 并查集主要思路
    num = int(random.randint(0, aa * aa - 1))  # 产生一个小于aa*aa-1的随机数
    neihbour = getnei(num)  # 取一个邻居
    if search(num) == search(neihbour):  # 检查是否在同一个集合中
        continue
    else:  # 不在同一个集合中则将两个集合合并
        isling[num][neihbour] = 1  # 表示 num 和 neihbour 两节点连通
        isling[neihbour][num] = 1
        union(num, neihbour)

# 以下为显示迷宫
# 画第一条横线
s = "+"
for j in range(0, aa):
    s = s + "-+"
print(s)
# 画第一行至aa-1行格子及下面的横线
for i in range(0, aa):
    s = "|"
    for k in range(0, aa - 1):  # 防止最后一列溢出
        s = s + " "
        if isling[i * aa + k][i * aa + k + 1] == 1:
            s = s + " "
        else:
            s = s + "|"
    s = s + " |"  # 追加画最后一格
    print(s)
    # 画格子下面的横线，要检测是否与下一行格子连通
    s = "+"
    for k in range(0, aa):
        if i < aa - 1:  # 防止最后一行溢出
            if isling[i * aa + k][(i + 1) * aa + k] == 1:
                s = s + " "
            else:
                s = s + "-"
            s = s + "+"
        else:  # 追加画最后一行横线
            s = s + "-+"
    print(s)


# AStar算法
#
class Node:  # 节点
    def __init__(self, x, y):
        self.x = x  # 节点坐标
        self.y = y
        self.g = 0  # 到起点的长度
        self.h = 0  # 到终点的长度
        self.px = -1  # 父节点x
        self.py = -1  # 父节点y


class AStar:  # 算法类
    def __init__(self, w, h, isling):
        self.W = w  # 地图宽
        self.H = h  # 地图高
        self.Isling = isling  # 节点连通关系
        self.OpenSet = []  # 开放节点表
        self.CloseSet = []  # 关闭节点表

    def findPath(self, startNode, endNode):  # 路径查找
        curNode = startNode  # 将开始节点设为当点节点
        bFound = False
        while (not bFound):
            self.CloseSet.append(curNode)  # 当前节点加入关闭节点
            cura = curNode.x * self.W + curNode.y  # 节点二维坐标转为一维
            arrs = []
            if curNode.x - 1 >= 0:
                arrs.append([curNode.x - 1, curNode.y])  # 左节点
            if curNode.x + 1 < self.W:
                arrs.append([curNode.x + 1, curNode.y])  # 右节点
            if curNode.y - 1 >= 0:
                arrs.append([curNode.x, curNode.y - 1])  # 上节点
            if curNode.y + 1 < self.H:
                arrs.append([curNode.x, curNode.y + 1])  # 下节点
            for arr in arrs:
                a = arr[0] * self.W + arr[1]  # 节点二维坐标转为一维
                if self.Isling[cura][a] != 1:  # 该节点与当前节点不连通，则跳过
                    continue
                found = 0
                for cnode in self.CloseSet:  # 查找是否已在CloseSet
                    if cnode.x == arr[0] and cnode.y == arr[1]:  # 在OpenSet中
                        found = 1
                        break
                if found == 1:    #在Closet中，则跳过
                    continue
                node = Node(arr[0], arr[1])
                node.g = curNode.g + 1  # 重新设置到起点的长度
                node.h = abs(node.x - endNode.x) + abs(node.y - endNode.y)  # 计算到终止节点的长度
                node.px = curNode.x  # 父节点改为当前节点
                node.py = curNode.y
                if node.x == endNode.x and node.y == endNode.y:  # 如果是终止节点，则表示已找到，返回
                    self.CloseSet.append(node)
                    bFound = True
                    return node
                found = 0
                i = -1
                for onode in self.OpenSet:  # 查找是否已在OpenSet
                    i = i + 1
                    if onode.x == node.x and onode.y == node.y:  # 在OpenSet中
                        if node.g < onode.g:  # 如果新g值更小，则更新节点
                            self.OpenSet[i].g = node.g
                            self.OpenSet[i].h = node.h
                            self.OpenSet[i].px = node.px
                            self.OpenSet[i].py = node.py
                        found = 1
                        break
                if found == 0:  # 如果不在OpenSet中，则新节点加入OpenSet
                    self.OpenSet.append(node)
            # 在OpenSet中查找最小f=g+h值，设为当前节点
            f = 99999
            i = -1
            j = -1
            for onode in self.OpenSet:
                i = i + 1
                if f > onode.g + onode.h:
                    f = onode.g + onode.h
                    j = i
            if j < 0:  # 找到了OpenSet为空，表示找不到路径
                return None
            else:
                curNode = self.OpenSet[j]
                del self.OpenSet[j]


astar = AStar(aa, aa, isling)
startNode = Node(0, 0)
endNode = Node(aa - 1, aa - 1)
node = astar.findPath(startNode, endNode)

if node == None:
    print("走不通")
    exit

astar.CloseSet.reverse()
for cnode in astar.CloseSet:
    if cnode.x == node.x and cnode.y == node.y:
        tree[node.x][node.y] = aa*aa
        node.x = cnode.px
        node.y = cnode.py

# 以下为显示迷宫解答
# 画第一条横线
s = "+"
for j in range(0, aa):
    s = s + "-+"
print(s)
# 画第一行至aa-1行格子及下面的横线
for i in range(0, aa):
    s = "|"
    for k in range(0, aa - 1):  # 防止最后一列溢出
        if tree[i][k] == aa*aa:
            s = s + "@"
        else:
            s = s + " "
        if isling[i * aa + k][i * aa + k + 1] == 1:
            s = s + " "
        else:
            s = s + "|"
    if tree[i][aa-1] == aa*aa: # 追加画最后一格
        s = s + "@"
    else:
        s = s + " "
    s = s + "|"
    print(s)
    # 画格子下面的横线，要检测是否与下一行格子连通
    s = "+"
    for k in range(0, aa):
        if i < aa - 1:  # 防止最后一行溢出
            if isling[i * aa + k][(i + 1) * aa + k] == 1:
                s = s + " "
            else:
                s = s + "-"
            s = s + "+"
        else:  # 追加画最后一行横线
            s = s + "-+"
    print(s)
