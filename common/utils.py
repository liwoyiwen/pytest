import time
import datetime


def getName(name="test"):
    return name+"_"+time.strftime('%Y-%m-%d_%H:%M:%S')

def getDate(a=0):
    return (datetime.datetime.now()+datetime.timedelta(days=int(a))).strftime("%Y-%m-%d")


def getDate1(a=0):
    return (datetime.datetime.now()+datetime.timedelta(days=int(a))).strftime("%Y-%m-%d %H:%M:%S")



def getTime(a=0):

    return (datetime.datetime.now()+datetime.timedelta(minutes=int(a))).strftime("%H:%M:%S")

def getTime2(a=0):

    return (datetime.datetime.now()+datetime.timedelta(minutes=int(a))).strftime("%H:%M")

def getTime3(a=0):

    return (datetime.datetime.now()+datetime.timedelta(minutes=int(a))).strftime("%Y-%m-%d %H:%M:%S")

def geturl():

    return "http://www.baidu.cn"

def timeConvert(s):
    timeArray = time.strptime(s, "%Y-%m-%d %H:%M:%S")
    timeStamp = int(time.mktime(timeArray)*1000)
    print(timeStamp)


def convert(popularizeId):
    if popularizeId!='':
        return int(popularizeId)

    else:
        return popularizeId




if __name__=="__main__":
    pass
