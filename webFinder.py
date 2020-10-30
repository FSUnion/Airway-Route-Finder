import threading
import time
import RouteFinderLib
import pickle
import socket
import validcode
import random
import config



class RouteRequest:
    validnum=0
    address=None

    def __init__(self,addr):
        self.validnum=random.randint(1000,9999)
        self.address=addr

requestList=[]
threadNumber_statistic=0

class SessionHandler(threading.Thread):
    client_socket=None
    client_addr=None

    def run(self):
        global requestList,threadNumber_statistic
        try:
            requestDataBytes=self.client_socket.recv(1024)
            requestData=str(requestDataBytes,"utf-8")
            requestHead=requestData.split('\r\n')[0].split(' ')[1]
            thread_num = len(threading.enumerate())
            print("线程({},{},开启线程统计{})==用户[{},{}]连接，请求{}   {}".format(self.name,thread_num,threadNumber_statistic,client_address[0],client_address[1],requestHead,\
                time.strftime("%m-%d %H:%M:%S", time.localtime()))) #/getRoute?from=ZGHA&to=ZJSY&valid=1111
            command=requestHead.split('?')[0]
            para=""
            if requestHead.__contains__("?"):
                para=requestHead.split('?')[1]
            if command.__contains__("/getRoute") and para.split('&').__len__()==3:
                validcodeans=para.split('&')[2].replace("valid=","")
                hasRequest=False
                remoteInstance=None
                for i in requestList:
                    if i.validnum==int(validcodeans):
                        hasRequest=True
                        remoteInstance=i
                        break
                
                if hasRequest==True:
                    ORIG=para.split('&')[0].replace("from=","")
                    DEST=para.split('&')[1].replace("dest=","")
                    data=SearchRoute(ORIG,DEST)
                    self.client_socket.send(bytes("HTTP/1.1 200 OK\r\nContent-Type:text/html\r\n\r\n"+data,"utf-8"))
                    requestList.remove(remoteInstance)
                else:
                    self.client_socket.send(bytes("HTTP/1.1 200 OK\r\nContent-Type:text/html\r\n\r\nNo Result.","utf-8"))
            elif command.__contains__("/getImage"):
                requestInstance=RouteRequest(client_address)
                imageBytes=validcode.getImageBytes(requestInstance.validnum)
                self.client_socket.send(bytes("HTTP/1.1 200 OK\r\nContent-Type:image/jpeg\r\n\r\n","utf-8")+imageBytes)
                requestList.append(requestInstance)
            elif command.__contains__("/getCycle"):
                self.client_socket.send(bytes("HTTP/1.1 200 OK\r\nContent-Type:text/html\r\n\r\n"+config.NAVDAT_CYCLE,"utf-8"))
                
            else:
                #webpagedat
                self.client_socket.send(bytes("HTTP/1.1 200 OK\r\nContent-Type:text/html\r\n\r\n"+webpagedat,"utf-8"))
            
        except Exception as x:
                print("线程({},当前线程数{},开启线程统计{})出错:{} 尝试回收当前线程   {}".format(self.name,thread_num,threadNumber_statistic,\
                x,time.strftime("%m-%d %H:%M:%S", time.localtime()))) #/getRoute?from=ZGHA&to=ZJSY&valid=1111

        finally:
                self.client_socket.close()
                threadNumber_statistic=threadNumber_statistic-1
                thread_num = len(threading.enumerate())
                print("线程({},当前线程数{},开启线程统计{})退出 线程回收成功   {}".format(self.name,thread_num,threadNumber_statistic,\
                time.strftime("%m-%d %H:%M:%S", time.localtime()))) #/getRoute?from=ZGHA&to=ZJSY&valid=1111
        return


webfile=open("index.html","r",encoding='UTF-8')
webpagedat=webfile.read()
webfile.close()

if config.DOMAIN_SUPPORT == True:
    webpagedat=webpagedat.replace("127.0.0.1:8000",config.USER_DOMAIN)

webpagedat=webpagedat.replace("BAIDUAPIKEY",config.BAIDUMAP_API_KEY)

navRTE=open(config.SET_NAVDAT_PATH,"rb")
RouteFinderLib.nodeList=pickle.load(navRTE)
navRTE.close()
searched_icao_DEP=[]
searched_icao_ARR=[]

def SearchRoute(orig,dest):
    global searched_icao_DEP,searched_icao_ARR
    endNode=None
    #orig="ZGHA";dest="ZJSY"
    if orig not in searched_icao_DEP:
        RouteFinderLib.startNode=RouteFinderLib.ReadSIDAirport(orig)
        searched_icao_DEP.append(orig)
    else:
        RouteFinderLib.startNode=RouteFinderLib.FindNodeByNAME_NonHash(orig)[0]
    if dest not in searched_icao_ARR:
        endNode=RouteFinderLib.ReadSTARAirport(dest)
        searched_icao_ARR.append(dest)
    else:
        endNode=RouteFinderLib.FindNodeByNAME_NonHash(dest)[0]
    return RouteFinderLib.Dijkstra(RouteFinderLib.startNode.iid,endNode.iid)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("", config.LISTEN_PORT))
server_socket.listen(128)

while True:
    client_socket, client_address = server_socket.accept()
    #print("[%s, %s]用户连接" % client_address)
    ss=SessionHandler()
    ss.client_addr=client_address
    ss.client_socket=client_socket
    ss.start()
    threadNumber_statistic=threadNumber_statistic+1
        
