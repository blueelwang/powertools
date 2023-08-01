#!/bin/bash

#######
# Author： BlueelWang
# Desc：机器性能监控报警脚本，支持webhook报警， 默认为飞书机器人
# Date：2023-08-01
#######
#获取cpu负载
cpu_load=`uptime | awk -F ':' '{print $5}'| awk -F ',' '{print $1}' | xargs`

#获取磁盘使用率
data_name="/"
disk_used=`df -h | grep -w $data_name | awk -F'[ %]+' '{print $5}'`

#获取内存情况
mem_total=`free -m | awk -F '[ :]+' 'NR==2 {print $2}'`
mem_used=`free -m | awk -F '[ :]+' 'NR==2 {print $3}'`

#统计内存使用率
mem_used=`awk 'BEGIN{printf"%.0f\n",('$mem_used' / '$mem_total')*100}'`

#主机信息
date_time=`date "+%Y-%m-%d %H:%M:%S"`
ip_addr=`ifconfig $ifconfig | grep "inet" |awk 'NR==1{ print $2}'`

# wehook url
webhook_url="https://open.feishu.cn/open-apis/bot/v2/hook/xxxxxxx"

msg="资源耗尽警告！\n巡查时间：${date_time}\nIP地址：${ip_addr}\n资源状况:\n【CPU负载：${cpu_load}】\n【磁盘使用率：${disk_used}%】\n【内存使用率：${mem_used}%】"

function send_message(){

   curl -s $webhook_url -X POST  -H "Content-Type: application/json" -d '{"msg_type":"text","content":{"text": "'"$msg"'"}}'
}

function check(){
   #根据机器的不同配置进行修改
   if [[ "$cpu_load" > 4 ]] || [[ "$disk_used" >20 ]] || [[ "$mem_used" > 80 ]];then
      send_message
   fi

}
check
