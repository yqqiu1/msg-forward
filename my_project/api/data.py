# -*- coding: utf-8 -*-
import time
import ujson

class databank:
    nextCleanTime = int(time.time())+1800
    noMobile = 0
    mobile = {}
    sms = {}


# mobile:
# { '#projectId1': { '#mobile1' : { 'status': #I1, 'expirationTime': #T1},
#                    '#mobile2' : { 'status': #I2, 'expirationTime': #T2}
#                  },
#   '#projectId2': { '#mobile3' : { 'status': #I2, 'expirationTime': #T3},
#                    '#mobile4' : { 'status': #I2, 'expirationTime': #T4}
#                  },
# }
# stauts: 0 not used. 1 sent. 2 ready for offline 
#
#
# sms:
# { '#projectId1': { '#mobile1' : { 'smsId': #I1, 'sms': #S1, 'pushTime': #T1},
#                    '#mobile2' : { 'smsId': #I2, 'sms': #S2, 'pushTime': #T2}
#                  },
#   '#projectId2': { '#mobile3' : { 'smsId': #I3, 'sms': #S3, 'pushTime': #T3},
#                    '#mobile4' : { 'smsId': #I4, 'sms': #S4, 'pushTime': #T4}
#                  },
# }





def mobileAppend ( projects ):
    t = int(time.time()) + 480 # 10位时间戳 8分钟有效期
    for project in projects:
        try:
            projectId = project['projectId']
            mobiles = project['mobile']

            if projectId not in databank.mobile.keys():
                databank.mobile[projectId]={}
            for mobile in mobiles:
                databank.mobile[projectId][mobile]=dict(
                    status = 0,
                    expirationTime = t,
                    )
        except:
            print("Warning in mobileAppend: project might be illegal input")
            print("in project: " )
            print(project)





def popExpiredMobile ():

    currentTime = int(time.time())
    listExpiredProject=[]
    CountExpiredProject=0
    for projectId in list(databank.mobile.keys()):

        listExpiredMobile = []
        for mobile in list(databank.mobile[projectId].keys()):
            if databank.mobile[projectId][mobile]['status']==2\
                    or databank.mobile[projectId][mobile]['expirationTime'] < currentTime :
                listExpiredMobile.append(mobile)
                del databank.mobile[projectId][mobile]

        if len(listExpiredMobile)>0:
            databank.noMobile -= len(listExpiredMobile)
            dictExpiredProject=dict(
                projectId = projectId,
                mobile = listExpiredMobile,
            )
            listExpiredProject.append(dictExpiredProject)
            CountExpiredProject +=1
            if CountExpiredProject == 5:
                break

    return listExpiredProject





def requestOffline(projectId,mobile):
    if projectId in databank.mobile.keys():
        if mobile in databank.mobile[projectId].keys():
            databank.mobile[projectId][mobile]['status']=2





def isMobileExist (projectId, mobile):
    if not projectId in databank.mobile.keys():
        return False
    if not mobile in databank.mobile[projectId].keys():
        return False
    return True





def requestMobile(projectId):
    if projectId not in databank.mobile.keys():
        return ""
    currentTime = int(time.time())
    for mobile in databank.mobile[projectId].keys():
        if databank.mobile[projectId][mobile]['status']==0:
            if databank.mobile[projectId][mobile]['expirationTime']>currentTime:
                databank.mobile[projectId][mobile]['expirationTime']+=60;
                databank.mobile[projectId][mobile]['status']=1
                return mobile
            databank.mobile[projectId][mobile]['status']=2
    return ""





def smsAppend ( messages ):
    currentTime = int(time.time())
    for message in messages:
        try:
            pushTime = message['pushTime']
            pushTime = currentTime
            newMessage = dict(
                id=message['id'],
                sms=message['sms'],
                pushTime=pushTime,
                )
            projectId = message['projectId']
            mobile = message['mobile']

            if projectId not in databank.sms.keys():
                databank.sms[projectId]={}
            databank.sms[projectId][mobile]=newMessage

            if projectId in databank.mobile.keys():
                if mobile in databank.mobile[projectId].keys():
                    databank.mobile[projectId][mobile]['status']=2

        except:
            print("Warning in smsAppend: message might be illegal input")
            print("in message: ")
            print(message)






def smsClean():
    currentTime = int(time.time())

    if currentTime>databank.nextCleanTime:
        databank.nextCleanTime = currentTime+1800
        cleanTime = currentTime - 300
        for projectId in list(databank.sms.keys()):
            for mobile in list(databank.sms[projectId].keys()):
                if databank.sms[projectId][mobile]['pushTime'] < cleanTime:
                    del databank.sms[projectId][mobile]





def smsQuery ( projectId, mobile ):
    smsClean()
    if projectId in databank.sms.keys():
        if mobile in databank.sms[projectId].keys():
            return databank.sms[projectId][mobile]['sms']
    return ""




def log ( ):
    print("")
    print("current time:                 " + str(int(time.time())))
    print("next sms database clean time: " + str(databank.nextCleanTime))
    print("")
    print("mobile:{")
    for projectId in databank.mobile.keys():
        print("  '"+str(projectId)+"':{")
        for mobile in databank.mobile[projectId].keys():
            print("    '" + str(mobile) + "': " + str(databank.mobile[projectId][mobile]))
        print("  }")
    print("}")
    print("")
    print("sms:{")
    for projectId in databank.sms.keys():
        print("  '"+str(projectId)+"':{")
        for mobile in databank.sms[projectId].keys():
            print("    '" + str(mobile) + "': " + str(databank.sms[projectId][mobile]))
        print("  }")
    print("}")
