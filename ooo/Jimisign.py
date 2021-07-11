import requests
import re
import json
import urllib
import time
import timeit
import math
import sys
from datetime import datetime
from dateutil import tz
import os
import dateutil.parser

requests.packages.urllib3.disable_warnings()
osenviron={}
djj_djj_cookie=''
Card_telegram=''


cookiesList1=[]
cookiesList2=[]
signbdList=[]
Chosecount=1#选择账号组的第x个，0位全部账号运行，1代表只运行第1个，2代表第2个
Userid=[4530469,]#多个用户
#4530469
telelist=[]
jmheader1={}
jmheader2={}
signbd={}
result=''
id=0


#签到查询和签到ck
def Jimi_plus():
   print('\n开始做任务.........')
   jimiplus_user()
   aggregation()
   signin()
def jimiplus_user():
    print('\n  用户')
    global result
    try:
      url = 'https://superapp.xgimi.com/api/v2/users/'+id
    
      resp = requests.get(url=url,headers=jmheader1,verify=False,timeout=10).json()
      
      if resp['code']=='ok':
         #print(resp['data']['nickName']+'|'+resp['data']['userName']+'|'+resp['data']['mobileAll'])
         loger(resp['data']['nickName']+'|'+resp['data']['userName']+'|'+resp['data']['mobileAll'],0)
      
    except Exception as e:
      msg=str(e)
      print(msg)
def aggregation():
    print('\n 积分')
    global result
    try:
      url = 'https://superapp.xgimi.com/api/v1/users/info/aggregation'
    
      resp = requests.get(url=url,headers=jmheader1,verify=False,timeout=10).json()
      
      if resp['code']=='ok':
         #print('积分'+str(resp['data']['integral']['completeStr']))
         loger(resp['data']['integral']['completeStr'],0) 
    except Exception as e:
      msg=str(e)
      print(msg)
      
def signin():
      print('\n 签到开始')
      url = 'https://mobile-api.xgimi.com/app/v4/integral/signin'
      msg=''
      jmheader2['Content-Type']='application/json'
      
      resp = requests.post(url=url,headers=jmheader2,data=json.dumps(signbd),verify=False,timeout=10).json()
      
      if resp['code']=='ok':
         if resp['data']['status']==3:
           print('签到成功.')
           msg='签到成功.'
         elif resp['data']['status']==2:
           print('重复签到.')
           msg='重复签到.'
      else:
         print('header或者body不对❌，请获取')
         msg='header或者body❌，请重新获取'
      loger(msg,0)

#=============================
def pushmsg(title,txt):
   print('════════════════════════通知═══════════════')
   txt=urllib.parse.quote(txt)
   title=urllib.parse.quote(title)
   try:
     print("\n【Telegram消息】")
     if Card_telegram.strip():
         id=Card_telegram[Card_telegram.find('@')+1:len(Card_telegram)]
         botid=Card_telegram[0:Card_telegram.find('@')]

         turl=f'''https://api.telegram.org/bot{botid}/sendMessage?chat_id={id}&text={title}\n{txt}'''

         response = requests.get(turl,verify=False,timeout=5)
     else:
       print('\n 获取通知数据错误❌')
   except Exception as e:
      pass
      #print(str(e))
    


def watch(flag,list):
   vip=''
   if flag in osenviron:
      vip = osenviron[flag]
   if flag in os.environ:
      vip = os.environ[flag]
   if vip:
       for line in vip.split('&'):
         if not line:
            continue 
         list.append(line.strip())
       return list
   else:
       print(f'''secret【{flag}】 is 空''')
       #exit()
       

def data_check():
     
     if not telelist or (telelist and len(telelist[0]))<30:
            print('\n Card_telegram对应的数据为空,程序无法使用tg通知功能。.注意格式')
     elif telelist and len(telelist[0])>30:
             Card_telegram=telelist[0]
       
     if (not cookiesList1 or (cookiesList1 and len(cookiesList1[0])))<30 and (not cookiesList2 or (cookiesList2 and len(cookiesList2[0])))<30:
          print('\n 程序退出中,Car_cookies对应的数据格式不正确,请填写完整。.')
          exit()
     if Chosecount==0:
          print(f"\n你配置的是{len(cookiesList)}个账号执行任务\n")
     else:
           print(f"\n你配置的是第{Chosecount}个账号执行任务\n")
   
    
def loger(m,flag):
   global result
   if flag==0:
      result +=m+'|'
   if flag==1:
      result +=m+'\n'

def start():
       global cookiesList1,telelist,jmheader1,jmheader2,result,Card_telegram,id,cookiesList2,signbd,Card_telegram
       
       watch('Card_telegram',telelist)
       if len(telelist)>0 and telelist[0].find('@')>0:
          Card_telegram =telelist[0]
       watch('jimi_cookies',cookiesList1)
       watch('jimi_signcookies',cookiesList2)
       watch('jimi_signbody',signbdList)
       data_check()
       n=0
       for count1,count2,count3,user in zip(cookiesList1,cookiesList2,signbdList,Userid):
         n+=1
         if Chosecount>0 and n!=Chosecount:
            continue
         result+='【'+str(n)+'】'
         jmheader1=eval(count1)
         jmheader1.pop('Host',None)
         jmheader2=eval(count2)
         jmheader2.pop('Host',None)
         signbd=eval(count3)
         
         id=str(user)
         Jimi_plus()
         result+='\n'
       
       #print(result)
       pushmsg('吉米plus',result)

if __name__ == '__main__':
    print('天安门时间', datetime.now(tz=tz.gettz('Asia/Shanghai')).strftime("%Y-%m-%d %H:%M:%S", ))
    start()
