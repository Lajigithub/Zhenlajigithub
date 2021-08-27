/*=================================




//====================================




*/




//====================================
const $iosrule = iosrule();

const log=1;//设置0关闭日志,1开启日志

//++++++++++++++++++++++++++++++++-


const program="京东获取ck";

const msg="获取地址，手网页打卡https://bean.m.jd.com/bean/signIndex.action，登录"


//++++++++++++++++++++++++++++++++

//3.需要执行的函数都写这里
function main()
{     jdck_begin();
}

function jdck_begin()
{
for(let i=0;i<idarry.length;i++)
{
  let sign_ck=$iosrule.read(idarry[i])+"\n";

console.log(sign_ck)

}




}


//++++++++++++++++++++++++++++++++++++
//4.基础模板

if ($iosrule.isRequest) {
  jdck_getck()
  $iosrule.end()
} else {
  main();
  $iosrule.end()
}



  
 


function jdck_getck() {

  if ($request.headers) {

 var urlval = $request.url;
var md_bd=$request.body;
var md_hd=$request.headers;




if(urlval.indexOf("bean/signIndex.action")>=0)
{
console.log(urlval);
let mdstr=JSON.stringify(md_hd);


if (mdstr.indexOf("Cookie")>=0)

{
let md_ck=md_hd.Cookie;
let ck=md_ck.match(/pt_key=(.+?);/)[0]+md_ck.match(/pt_pin=(.+?);/)[0]

let nm=decodeURIComponent(md_ck.match(/pt_pin=(.+?);/)[1])
console.log("复制粘贴用户名"+nm+"的cookies")
console.log(ck)


let bd= $iosrule.write(ck,nm);


if (bd==true) 
 papa(program+"【"+nm+"】","[获取cookies]成功",ck);
else
papa(program,"[获取京东cookies数据失败]",msg);

}
}











  
}}









function papa(x,y,z){

$iosrule.notify(x,y,z);}
function getRandom(start, end, fixed = 0) {
  let differ = end - start
  let random = Math.random()
  return (start + differ * random).toFixed(fixed)
}




function iosrule() {
    const isRequest = typeof $request != "undefined"
    const isSurge = typeof $httpClient != "undefined"
    const isQuanX = typeof $task != "undefined"
    const notify = (title, subtitle, message) => {
        if (isQuanX) $notify(title, subtitle, message)
        if (isSurge) $notification.post(title, subtitle, message)
    }
    const write = (value, key) => {
        if (isQuanX) return $prefs.setValueForKey(value, key)
        if (isSurge) return $persistentStore.write(value, key)
    }
    const read = (key) => {
        if (isQuanX) return $prefs.valueForKey(key)
        if (isSurge) return $persistentStore.read(key)
    }
    const get = (options, callback) => {
        if (isQuanX) {
            if (typeof options == "string") options = { url: options }
            options["method"] = "GET"
            $task.fetch(options).then(response => {
                response["status"] = response.statusCode
                callback(null, response, response.body)
            }, reason => callback(reason.error, null, null))
        }
        if (isSurge) $httpClient.get(options, callback)
    }
    const post = (options, callback) => {
        if (isQuanX) {
            if (typeof options == "string") options = { url: options }
            options["method"] = "POST"
            $task.fetch(options).then(response => {
                response["status"] = response.statusCode
                callback(null, response, response.body)
            }, reason => callback(reason.error, null, null))
        }
        if (isSurge) $httpClient.post(options, callback)
    }
    const end = () => {
        if (isQuanX) isRequest ? $done({}) : ""
        if (isSurge) isRequest ? $done({}) : $done()
    }
    return { isRequest, isQuanX, isSurge, notify, write, read, get, post, end }
};



