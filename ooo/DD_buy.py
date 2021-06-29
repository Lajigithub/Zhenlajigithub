
import re
import requests
import json
import urllib
import time
import timeit
import math
import sys
import string
from datetime import datetime
from dateutil import tz
import os
requests.packages.urllib3.disable_warnings()

osenviron={}
cookiesList=[]
DD_SECRETList=[]
message=''
result=''
apiurl=''
apiurl1=''
apiurl2=''
tele_notice=''#tg通知
jdNotify=True


#===========::::::#===========::::::


headers={"Accept": "*/*","Accept-Encoding": "gzip, deflate, br","Accept-Language": "zh-cn","User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 xzone/9.30.0 station_id/5f8972e364c4190001d7d4a2"}
userTasks=[]
DD_SECRET=''
dnsList=[]

##===========================主体部分


def showMsg():
  global result,message
  print('---------------通知🔔---------------------')
  msg=f"【{index}】\n{message}"
  pushmsg('DD_B',msg)
  result=''
  message = ''

def Dingdong_buy():
  home_point()
  task_list()
  dotask()
  dofeed()
  lucky_draw()
  totalinfo()
  showMsg()




##===========================主体部分
def task_list():
  global userTasks
  userTasks=[]
  url = apiurl+'/api/v2/task/list?'+DD_SECRET+'&gameId=1'
  data= requests.get(url,headers=headers,verify=False, timeout=10).json()
  if data['code']==0:
     userTasks=data['data']['userTasks']
def props_feed(propsId,seedId):
  url = f"{apiurl}/api/v2/props/feed?{DD_SECRET}&gameId=1&propsId={propsId}&seedId={seedId}"
  data= requests.get(url,headers=headers,verify=False, timeout=10).json()
  print(data)
  if data['code']==0:
     msg=data['data']['msg']
     print(msg)
def reward_receive(userRewardLogId):
  url = f"{apiurl}/api/v2/reward/receive?{DD_SECRET}&gameId=1&userRewardLogId={userRewardLogId}"
  data= requests.get(url,headers=headers,verify=False, timeout=10).json()
  print(data['msg'])
def task_reward(userTaskLogId):
  url = apiurl+'/api/v2/task/reward?'+DD_SECRET+'&gameId=1&userTaskLogId='+userTaskLogId
  data= requests.get(url,headers=headers,verify=False, timeout=10).json()
  print(data['msg'])
  
def task_achieve(taskCode):#LOTTERY
  url = apiurl+'/api/v2/task/achieve?'+DD_SECRET+'&gameId=1&taskCode='+taskCode
  data= requests.get(url,headers=headers,verify=False, timeout=10).json()
  print(data['msg'])
#天天翻牌
#、用户每天可使用饲料进行翻牌，每次消耗5g饲料，每个用户每天最多参与10次。
def lucky_draw():
  print('\n【天天翻牌】')
  while True:
    url = f"{apiurl}/api/lucky-draw-activity/draw?{DD_SECRET}&gameId=1&ldaId=30"
    data= requests.get(url,headers=headers,verify=False, timeout=10).json()
    #print(data)
    time.sleep(2)
    if data['code']==0:
      if data['data']['canDraw']:
         print(f"{data['data']['msg']},获得{data['data']['chosen']['name']}")
      else:
          print('每天10次')
          break
    else:
      print(data['msg'])
      break
     
def dotask():
   if len(userTasks)==0:
      return
   N=0
   print('\n【获取任务列表】')
   for item in userTasks:
     N+=1
     descriptions=''
     taskName=item['taskName']
     continuousDays=item['continuousDays']
     buttonStatus=item['buttonStatus']
     userTaskLogId=item['userTaskLogId']
     if len(item['descriptions'])>0:
       descriptions=item['descriptions'][0]
     #print(f"【{N}】{taskName}-({descriptions})-{continuousDays}-{buttonStatus}-{userTaskLogId}")
   #做任务
   print('\n【开始做任务】')
   N=0
   for item in userTasks:
     N+=1
     taskName=item['taskName']
     buttonStatus=item['buttonStatus']
     taskCode=item['taskCode']
     userTaskLogId=item['userTaskLogId']
     #print(f"开始任务【{N}】{taskName}")
     if buttonStatus=='TO_ACHIEVE':
       task_achieve(taskCode)
     if buttonStatus=='TO_REWARD':
       task_reward(userTaskLogId)
     #if buttonStatus=='WAITING_REWARD':
       #task_reward(userTaskLogId)
       
       
       
def FISHPOND_V1():
  url = apiurl+'/api/v2/userguide/detail?'+DD_SECRET+'&gameId=1&guideCode=FISHPOND_V1'
  data= requests.get(url,headers=headers,verify=False, timeout=10).json()
  return data
def dofeed():
   data=FISHPOND_V1()
   if data['code']==0:
      seedId=data['data']['baseSeed']['seedId']
      propsId=data['data']['feed']['propsId']
      amount=data['data']['feed']['amount']
      for i in range(int(amount/10)):
       props_feed(propsId,seedId)
       time.sleep(2)
	
	
	
def totalinfo():
  data=FISHPOND_V1()
  if data['code']==0:
    baseSeed=data['data']['baseSeed']
    expPercent=baseSeed['expPercent']
    levelExp=baseSeed['levelExp']
    msg=baseSeed['msg']
    amount=data['data']['feed']['amount']
    
    global message
    message+=f"【鱼塘等级】{levelExp}\n【进度】{expPercent}%\n【剩余饲料】{amount}克\n【提示】{msg}"
    
    
    
def home_point():
  url = f"{apiurl2}/point/home?{DD_SECRET}"
  
  data= requests.get(url,headers=headers,verify=False, timeout=10).json()
  
  if data['code']==0:
      point_num=data['data']['point_num']
      is_today_sign=data['data']['user_sign']['is_today_sign']
      if not is_today_sign:
        user_signin()
      sign_series=data['data']['user_sign']['sign_series']
      
      global message
      message+=f"【积分】{point_num}\n【签到】第{sign_series}天签到\n"
      time_line=data['data']['user_sign']['time_line']
      for it in time_line:
        if sign_series==it['day'] and it['ticket_id']:
           print(it['ticket_name'])
        

def user_signin():
  url = apiurl1+'/api/v2/user/signin/'
  body=f"{DD_SECRET}"
  headers['Content-Type']= 'application/x-www-form-urlencoded'
  data= requests.post(url,headers=headers,data=body,verify=False, timeout=10).json()
  if data['code']==0:
     print('签到成功')
  else:
     print('签到失败'+data['message'])
##===========================主体部分
        
def check(flag,cookiesList):
   global tele_notice
   djj_djj_cookie=''
   if "TELE_NOTICE_1" in os.environ:
     tele_notice= os.environ["TELE_NOTICE_1"]
   if "TELE_NOTICE_1" in osenviron:
     tele_notice= osenviron["TELE_NOTICE_1"]
   if flag in os.environ:
     djj_djj_cookie = os.environ[flag]
   if flag in osenviron:
      djj_djj_cookie = osenviron[flag]
      for line in djj_djj_cookie.split('\n'):
        if not line:
          continue 
        cookiesList.append(line.strip())
   elif djj_djj_cookie:
       for line in djj_djj_cookie.split('\n'):
         if not line:
            continue 
         cookiesList.append(line.strip())
   else:
     print('DTask is over.')
     exit()

def pushmsg(title,txt):
  try:
   txt=urllib.parse.quote(txt)
   title=urllib.parse.quote(title)

   print('~~~~~~~~~~~~~~~~~~~~通知~~~~~~~~~~~~~~~~~~~~\n')
   if tele_notice.strip():
      print("\n【Telegram消息】")
      id=tele_notice[tele_notice.find('@')+1:len(tele_notice)]
      botid=tele_notice[0:tele_notice.find('@')]

      turl=f'''https://api.telegram.org/bot{botid}/sendMessage?chat_id={id}&text={title}\n{txt}'''

      response = requests.get(turl)
      #print(response.text)
  except Exception as e:
      msg=str(e)
      pass
def loger(m):
   #print(m)
   global result
   result +=m
def clock(func):
    def clocked(*args, **kwargs):
        t0 = timeit.default_timer()
        result = func(*args, **kwargs)
        elapsed = timeit.default_timer() - t0
        name = func.__name__
        arg_str = ', '.join(repr(arg) for arg in args)
        print('[🔔运行完毕用时%0.8fs] %s(%s) -> %r' % (elapsed, name, arg_str, result))
        return result
    return clocked
    
@clock
def start():
   print('Localtime',datetime.now(tz=tz.gettz('Asia/Shanghai')).strftime("%Y-%m-%d %H:%M:%S", ))
   global result,index,username,DD_SECRET,apiurl,apiurl1,apiurl2
   check('DD_COOKIE',cookiesList)
   check('DD_SECRET',DD_SECRETList)
   check('DD_URL',dnsList)
   apiurl=dnsList[0]
   apiurl1=dnsList[1]
   apiurl2=dnsList[2]
   index=0
   for count,sc in zip(cookiesList,DD_SECRETList):
     index+=1
     headers['Cookie']=count
     DD_SECRET=sc
     Dingdong_buy()
         
def main_handler(event, context):
    return start()

if __name__ == '__main__':
       start()
