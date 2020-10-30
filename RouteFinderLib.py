import threading
import sys
import math
import time
import heapq
import pickle
import config
import json

# IID is the index of the node in nodeList

ASDATA_PATH=config.LOCAL_ASDATA_PATH

class Edge:
    nfrom = 0  # IID
    nend = 0  # IID
    dist = 0
    name = ""
    toinstantnode = None
    color = (0, 0, 0)

    def __init__():
        return

    def __init__(self, nodefrom, node_end, name, r, g, b):
        self.nfrom = nodefrom.iid
        self.nend = node_end.iid
        self.name = name
        self.color = (r, g, b)
        # self.toinstantnode = node_end


class Node:
    iid = 0
    name = ""
    px = 0.0
    py = 0.0
    nextList = None

    def __init__(self, name, x, y):
        self.iid = nodeList.__len__()
        self.name = name
        self.px = x
        self.py = y
        self.nextList = []
        self.nextList.clear()

    def gethash(self):
        return CalcNodeHash(self.px,self.py)

def CalcNodeHash(x,y):
    return int(abs(int(x)*int(y)))

class searchingNode:
    name = 0
    iid = 0
    route = ""
    dist = 0
    route = ""
    routelist=[] #(edgename,routename,iid)

    def __init__(self, node):
        self.iid = node.iid
        self.name = node.name
        self.route = str(startNode.name)


nodeList = []
edgeRGB_dic = {}
startNode = None

PI = 3.1415926535898
EARTH_RADIUS = 6378.137


def rad(x):
    return x * PI / 180.0


def GetDistance_KM(lat1, lon1, lat2, lon2):
    radLat1 = rad(lat1)
    radLat2 = rad(lat2)
    a = radLat1 - radLat2
    b = rad(lon1) - rad(lon2)
    s = 2 * math.asin(math.sqrt(math.pow(math.sin(a / 2), 2) +
                                math.cos(radLat1) * math.cos(radLat2) * math.pow(math.sin(b / 2), 2)))
    s = s*EARTH_RADIUS
    return s


def CalcDist(iid1, iid2):
    nodeinstant1 = nodeList[iid1]
    nodeinstant2 = nodeList[iid2]
    px1 = nodeinstant1.px
    px2 = nodeinstant2.px
    py1 = nodeinstant1.py
    py2 = nodeinstant2.py
    return GetDistance_KM(px1, py1, px2, py2)

class RouteInformation:
    exeTime=""
    routeData=""
    routeDist=""
    nodes=[] #NODENAME LAT LON

    def __init__(self,sttime,route,dist,listobj):
        self.exeTime=sttime
        self.routeData=route
        self.routeDist=dist
        self.nodes=listobj

def Dijkstra(start, end):
    timestart = time.time()
    allNodeDist = []
    visitedTable = []
    for i in nodeList:
        allNodeDist.append(99999999.9)
        visitedTable.append(False)
    startNode = searchingNode(nodeList[start])

    queue=[]
    heapq.heappush(queue,(0.0,id(startNode),startNode))
    targetNode = None
    while queue.__len__() != 0:
        currentNode = heapq.heappop(queue)[2]
        #if visitedTable[currentNode.iid] is True:
         #   continue
        visitedTable[startNode.iid] = True
        tempcurrnode = nodeList[currentNode.iid]

        # Add result
        if tempcurrnode.iid == end:
            if targetNode == None:
                targetNode = currentNode
            else:
                if targetNode.dist > currentNode.dist:
                    targetNode = currentNode

        for n in tempcurrnode.nextList:
            nextNode = searchingNode(nodeList[n.nend])
            #if visitedTable[nextNode.iid is True:
            #    continue
            nextNode.route = currentNode.route + \
               " "+n.name+" "+nodeList[n.nend].name
            nextNode.routelist=list(currentNode.routelist)
            nextNode.routelist.append((n.name,nodeList[n.nend].name,n.nend))
            nextNode.dist = currentNode.dist + \
                CalcDist(currentNode.iid, nodeList[n.nend].iid)
            if allNodeDist[nextNode.iid] > nextNode.dist:
                allNodeDist[nextNode.iid] = nextNode.dist
                heapq.heappush(queue,(nextNode.dist,id(nextNode),nextNode))
    # print("finished")
    time_end= time.time()
    print("Dijkstra Function:"+str((time_end-timestart)/1000000000)+"s")
    sttime="%.2f"%((time_end-timestart)/1000000000)
    routeObj=None
    if targetNode is None:
        print("No result.")
        routeObj = RouteInformation(sttime,"No result.","0.00 km",None)
    else:
        #print(targetNode.route, targetNode.dist)
        distStr="%.2f km"%targetNode.dist
        routeTotal=OutputRoute(targetNode.routelist)
        print(routeTotal,targetNode.dist)
        nodesinfor=getEveryNodeInforList(targetNode.routelist)
        routeObj = RouteInformation(sttime,routeTotal,distStr,nodesinfor)
    return getOutput(routeObj)

def getOutput(routeobj):
    #output="查询时间：%s s\r\n航路：%s\r\n航程：%s||||NODENAME1 LAT1 LON1\r\nNODENAME2 LAT2 LON2"
    output="查询时间：%s s\r\n航路：%s\r\n航程：%s||||%s"%(routeobj.exeTime,routeobj.routeData,\
        routeobj.routeDist,routeobj.nodes)
    return output

def getEveryNodeInforList(routelist):
    ansstr="" #'NODENAME LAT LON'
    for i in routelist:
        ansstr=ansstr+("%s %.5f %.5f\r\n"%(nodeList[i[2]].name,nodeList[i[2]].px,nodeList[i[2]].py))
    return ansstr

def OutputRoute(routelist):
    stack=[]
    for i in routelist:
        if stack.__len__()>0:
            if stack[stack.__len__()-1][0]==i[0]:
                stack[stack.__len__()-1]=i
                continue
        stack.append(i)
    answer=startNode.name+" "
    for i in stack:
        answer=answer+i[0]+" "+i[1]+" "
    return answer

def FindNodeByNAME(name,x,y):
    for j in nodeList:
        if j.name == name and j.gethash() == CalcNodeHash(x,y):
            return j
    return None

def FindNodeByNAME_NonHash(name):
    ans=[]
    for j in nodeList:
        if j.name == name:
            ans.append(j)
    return ans


nodeReadCnt= 0
edgecnt= 0
datlen= 0


def ReadASData():
    global nodeList, nodeReadCnt, edgecnt, datlen

    file= open(ASDATA_PATH+"ATS.txt", "r")
    datlines= file.readlines()
    datlen= datlines.__len__()
    nodenamelist= [] #(nodename,hash)
    print("开始读点")
    for i in datlines:
        if i.split(',')[0] == 'S':
            nod1= Node(i.split(',')[1], float(
                i.split(',')[2]), float(i.split(',')[3]))
            nod2= Node(i.split(',')[4], float(
                i.split(',')[5]), float(i.split(',')[6]))
            
            set1=(nod1.name,CalcNodeHash(nod1.px,nod1.py))
            set2=(nod2.name,CalcNodeHash(nod2.px,nod2.py))
            if set1 not in nodenamelist:
                nodeList.append(nod1)
                nodenamelist.append(set1)
            if set2 not in nodenamelist:
                nodeList.append(nod2)
                nodenamelist.append(set2)
            nodeReadCnt= nodeReadCnt+1
    edgename=""
    print("开始读边")
    for i in datlines:
        if i.split(',')[0] == 'A':
            edgename=i.split(',')[1]
            continue
        if i.split(',')[0] == 'S':
            previousNode=FindNodeByNAME(i.split(',')[1],float(i.split(',')[2]),float(i.split(',')[3]))
            nextNode=FindNodeByNAME(i.split(',')[4],float(i.split(',')[5]),float(i.split(',')[6]))
            previousNode.nextList.append(
                Edge(previousNode,nextNode, edgename, 0,
                    0, 0))
        edgecnt=edgecnt+1
    file.close()
    print("读入："+str(edgecnt)+"条边")

def ReadSIDAirport(ICAO):
    global nodeList
    file= open(ASDATA_PATH+"\\proc\\"+ICAO+".txt", "r")
    datasource=file.read()
    file.seek(0)
    datlines=file.readlines()
    
    file.close()

    apfile=open(ASDATA_PATH+"\\Airports.txt", "r")
    apdat=apfile.readlines()
    apfile.close()

    apLat=0.0
    apLon=0.0
    for i in apdat:
        if i.__contains__(ICAO):
            apLat=float(i.split(',')[3])
            apLon=float(i.split(',')[4])
            break

    airport_node=Node(ICAO,apLat,apLon)
    dat_per_para=datasource.split('\n\n')
    #print(dat_per_para)
    added_nodes=[]
    for i in dat_per_para:
        perline=i.split('\n')
        #print(perline)
        if perline[0].__contains__("SID,"):
            nextName=perline[perline.__len__()-1].split(',')[1]
            lat=float(perline[perline.__len__()-1].split(',')[2])
            lon=float(perline[perline.__len__()-1].split(',')[3])
            if nextName in added_nodes:
                continue
            tfNode=FindNodeByNAME(nextName,lat,lon)
            if tfNode is None:
                print("机场"+ICAO+"无法添加航点:"+nextName,lat,lon)
                continue
            print("机场"+ICAO+"添加航点:"+tfNode.name,lat,lon)
            airport_node.nextList.append(Edge(airport_node,tfNode,"SID",0,0,0))
            added_nodes.append(nextName)
    nodeList.append(airport_node)
    return airport_node

def ReadSTARAirport(ICAO):
    global nodeList
    file= open(ASDATA_PATH+"\\proc\\"+ICAO+".txt", "r")
    datasource=file.read()
    file.seek(0)
    datlines=file.readlines()
    file.close()
    apfile=open(ASDATA_PATH+"\\Airports.txt", "r")
    apdat=apfile.readlines()
    apfile.close()

    apLat=0.0
    apLon=0.0
    for i in apdat:
        if i.__contains__(ICAO):
            apLat=float(i.split(',')[3])
            apLon=float(i.split(',')[4])
            break

    airport_node=Node(ICAO,apLat,apLon)
    dat_per_para=datasource.split('\n\n')
    added_nodes=[]
    for i in dat_per_para:
        perline=i.split('\n')
        #print(perline)
        if perline[0].__contains__("STAR,"):
            nextName=perline[1].split(',')[1]
            lat=float(perline[1].split(',')[2])
            lon=float(perline[1].split(',')[3])
            if nextName in added_nodes:
                continue
            tfNode=FindNodeByNAME(nextName,lat,lon)
            if tfNode is None:
                print("机场"+ICAO+"无法添加航点:"+nextName,lat,lon)
                continue
            print("机场"+ICAO+"添加航点:"+tfNode.name,lat,lon)
            tfNode.nextList.append(Edge(tfNode,airport_node,"STAR",0,0,0))
            added_nodes.append(nextName)
    nodeList.append(airport_node)
    return airport_node

