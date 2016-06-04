import queue
import time
import threading
import random
import os
import re
import shutil
import urllib.request
import urllib
from collections import deque
q=queue.Queue()

s_time=time.strftime('%Y-%m-%d',time.localtime(time.time()))

txtfile=("%s-pic-not-find.txt") % s_time
f = open(txtfile,"w",encoding='utf-8')
f.write(" ") 
f.close()




web_db="rightinthebox.com"
web_pic_e="E:\\zencart\\"			#图片下载保存地址






#加载
def pr():
	name=threading.current_thread().getName()
        
	print(name+"正在加载数据库图片地址......")
	f = open(r"images.txt","r",encoding='utf-8')
	try:
		all_the_text = f.readlines()
	finally:
		f.close()

	for tt in all_the_text:
		

		tt_flag=tt.replace("\n","")
		#print(tt)
		tt_flag_arr=tt_flag.split("****")
		tt_arr_one=0
		tt_arr_name=""
		#print(tt_flag_arr)
		for tt_arr in tt_flag_arr:
			qq=deque([])
			#print(tt_arr)
			if(tt_arr_one==0):
				if(len(tt_arr)>0):
					tt_arr_name_flag=tt_arr.split("/")[-1]
					tt_arr_name=tt_arr_name_flag.replace(".jpg","")
					qq.append(tt_arr)
					qq.append(tt_arr_name+".jpg")
					
			else:
				if(len(tt_arr)>0):
					tt_arr_name_other_flag=("%s_%s.jpg") % (tt_arr_name,tt_arr_one)
					qq.append(tt_arr)
					qq.append(tt_arr_name_other_flag)
					
			tt_arr_one+=1
			q.put(qq)
	print(name+"-------------pic_all.txt中的图片加载结束 ")



#拷贝
def co():
	name=threading.current_thread().getName()
	#time.sleep(1)
	print(name+"下载图片线程启动......")

	while True:
		print(name+"检测到剩余下载图片数量: ",q.qsize())
		data=q.get();
		img_old_name=data[0]
		img_new_name=data[1]
		#print("原图片文件：",img_old_name)
		#print("新图片文件：",img_new_name)
		img_name=img_old_name.split("/")[-1]
		
		#print(data)
		#print(img_name)
		
		web_name = "http://"
		savePath = img_old_name.replace(web_name,"",1).replace(img_name,"",1).replace("/","\\",50)
		savePath = savePath.replace("litbimg1.","")
		savePath = savePath.replace("litbimg2.","")
		savePath = savePath.replace("litbimg3.","")
		savePath = savePath.replace("litbimg4.","")
		savePath = savePath.replace("litbimg5.","")
		savePath = savePath.replace("litbimg6.","")
		savePath = savePath.replace("litbimg7.","")
		savePath = savePath.replace("litbimg8.","")
		savePath = savePath.replace("litbimg9.","")
		savePath = savePath.replace("rightinthebox.com\\","")
		savePath = savePath.replace("images\\","")
		savePath = savePath.replace("384x384\\","")
		savePath = web_pic_e + savePath
		
		filename = savePath+img_new_name
		if os.path.exists(filename):
			#取得目标文件夹目录
			print("图片已下载")

		else:

			#判断目标文件夹是否存在
			if not os.path.exists(savePath):
				os.makedirs(savePath)			#创建目录
			try:								#下载文件
			#if (1==1):
				urlopen=urllib.request.URLopener()
				#print(data)
				headers = ('User-Agent','Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11')
				urlopen.addheaders = [headers]
				#urlopen=urllib.request.URLopener(headers)
				fp = urlopen.open(img_old_name)
				img_data = fp.read()
				fp.close()
				
				file=open(savePath + img_new_name,'w+b')
				file.write(img_data)
				print ("下载成功："+ img_new_name)
				file.close()
			except IOError:
				print ("下载失败:")

				f = open(txtfile,"a",encoding='utf-8')
				f.write("\n"+img_old_name) 
				f.close()
		#time.sleep(5)


threading.Thread(target=pr,name=web_db).start()
for i in range(50):
	threading.Thread(target=co,name=web_db).start()
