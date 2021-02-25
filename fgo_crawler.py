import requests
import sys
from bs4 import BeautifulSoup
import json,os,re
def fun(a):
    for i in range(len(a)):
        if a[i]!='':
            break
    else:
        i+=1
        print('false')
    return i
def update_servant():
    url1=r'https://fgo.wiki/w/%E8%8B%B1%E7%81%B5%E5%9B%BE%E9%89%B4'
    url_all=r'https://fgo.wiki/w/'
    url_all2=r'https://fgo.wiki'
    all_file_path=r'F:\jupyter_notebook_my_code\pictures\fgo_cal\servant_detail'
    b=BeautifulSoup(requests.get(url1).text,'html5lib')
    aa=re.findall(r'sort_hp\\n1,(.*?)"; *\n',str(b))
    d=aa[0].split(',')
    e=[]
    for i in range(44,46):
        e.append([['id',i+1],['chinese_name',d[i*34+4]],['japanese_name',d[i*34+2]],['star_num',d[i*34]],['hp',d[i*34+9]],['atk',d[i*34+10]],['class',d[i*34+11]],
           ['hidden_attr',d[i*34+7]],['np_type',d[i*34+19]],['np_color',d[i*34+18]]],)
        normal_servant=True if d[i*34+10]!='—' else False
        print(e[-1])
        filepath=all_file_path+'\\'+e[-1][1][1]
        ##        if not os.path.exists(filepath):
        ##            os.mkdir(filepath)
        image_path=filepath+'\\image'
        ##        if not os.path.exists(image_path):
        ##            os.mkdir(image_path)
        ##        print(d[i*34+12])
        ##        img=requests.get(url_all2+d[i*34+12]).content
        ##        r=re.findall(r'/([^/.]*\.jpg)',d[i*34+12])
        ##        with open(image_path+'\\'+r[0],'wb') as f:
        ##            f.write(img)
        print(-1)
        print(normal_servant)
        if normal_servant:
            print(0)
            html_all = requests.get(url_all+e[-1][1][1])
            print(0.33)
            htmltxt_all=html_all.text
            print(0.66)
            soup_all = str(BeautifulSoup(htmltxt_all,'html5lib'))
            print(1)
            data={}
            data['属性']=re.findall(r'title="属性：(.*?)"',soup_all)
            data['隐藏属性']=re.findall(r'title="隐藏属性：(.*?)"',soup_all)
            data['card']=re.findall('img alt="(.*?).png"',re.findall(r'指令卡(.*?)Hit信息',soup_all,re.S)[0])
            r=re.findall('Hit信息(.*?)NP获得率',soup_all,re.S)
            r1=re.findall(r'<th>(.*?)\n*</th>',r[1],re.S)
            r2=re.findall('<td.*?>(.*?)\n*</td>',r[1])
            l=[]
            print(2)
            print('range(len(r2)):',range(len(r2)))
            for j in range(len(r2)):
                if '—' not in r2[j]:
                    k=re.findall('\d+',r2[j])
                    l.append([r1[j],k[0],k[1:]])
                else:
                    l.append([r1[j],'0',None])
            data['Hit数_伤害分布']=l
            r=re.findall('NP获得率(.*?)出星率(.+)',soup_all,re.S)
            r1=re.findall('<th>(.*?)\n*</th>',r[0][0])
            r2=re.findall('<td>(.*?)\n*</td>',r[0][0])
            data['np率']=[[r1[j],r2[j]] for j in range(len(r1))]
            r1=re.findall('(.*?)特性(.+)',r[0][1],re.S)
            r2=re.findall('<th.*?>(.*?)\n*</th>',r1[0][0])
            r3=re.findall('<td.*?>(.*?)\n*</td>',r1[0][0])
            print(3)
            print('range(len(r2)):',range(len(r2)))
            for i in range(len(r2)):
                data[r2[i]]=r3[i]
            r2=re.findall('(.*?)<h2><span id="技能">(.+)',r1[0][1],re.S)
            l=[]
            #print(r2[0][0])
            if 'tabbertab' in r2[0][0]:
                r3=re.findall('<div class="tabbertab" title="(.*?)">.*?img alt="(.*?).png".*?<big>(.*?)</big>(.*?)</table>',r2[0][0],re.S)
                for j in r3:
                    r4=re.findall('<th.*?class="(.*?)".*?>(.*?)\n.*?<tr>(.*?)</tr>',j[3],re.S)
                    l.append([j[0],j[1],j[2],[]])
                    for k in r4:
                        r5=re.findall('<td.*?>(.*?)\n*</td>',k[2])
                        l[-1][-1].append([k[0],k[1],r5])
            else:
                r3=re.findall('.*?img alt="(.*?).png".*?<big>(.*?)</big>(.*?)</table>',r2[0][0],re.S)
                for j in r3:
                    r4=re.findall('<th colspan="5" class="(.*?)">(.*?)\n.*?<tr>(.*?)</tr>',j[2],re.S)
                    l.append([j[0],j[1],j[2],[]])
                    for k in r4:
                        r5=re.findall('<td.*?>(.*?)\n*</td>',k[2])
                        l[-1][-1].append([k[0],k[1],r5])
            print(4)
            data['noble_phantasm']=l
            #print(data)
            return r2[0][1]
            r1=re.findall('(.*?)职阶技能(.+)',r2[0][1],re.S)
            r3=re.findall('(技能\d)（|<div class="tabbertab".*?title="(.*?)">|<table class="wikitable nomobile logo" style="text-align:center;width:750px">(.*?)</tbody>',r1[0][0],re.S)
            l=[]
            print(5)
            print('range(len(r3)):',range(len(r3)))
            for i in range(len(r3)):
                #print(r3[i])
                if fun(r3[i])==1:
                    if fun(r3[i+1])==0:
                        l.append([r3[i][1]])
                    elif fun(r3[i+1])==2:
                        l[-1][-1].append([r3[i][1]])
                    else:
                        print('error')
                elif fun(r3[i])==0:
                    if len(l)==0:
                        l.append(['a'])
                    l[-1].append([r3[i][0]])
                elif fun(r3[i])==2:
                    l1=[]
                    r4=re.findall('充能时间：(\d+)→.*?lang="ja".*?>(.*?)\n*</td>(.*)',r3[i][2],re.S)
                    r5=re.findall('<th colspan="10">(.*?)\n*</th></tr>(.*?</td>)</tr>',r4[0][2],re.S)
                    for i in r5:
                        r6=re.findall('<td.*?>(.*?)\n*</td>',i[1])
                        l1.append([i[0],r6])
                    if(len(l[-1][-1]))==1:
                        l[-1][-1].append(['b'])
                    l[-1][-1][-1]+=[['name',r4[0][1]],['cd',r4[0][0]],l1]
                #print(l)
            data['skill']=l
            with open(filepath+'\\detail_view.json','w',encoding='utf-8') as f:
                json.dump(data,f,ensure_ascii=False)
        with open(filepath+'\\general_view.json','w',encoding='utf-8') as f:
            json.dump(e[-1],f,ensure_ascii=False)
            
#         r=re.findall(r'div class="graphpicker.*\n',soup_all)
#         if len(r):
#             r1=re.findall(r'img alt="(.*?)".*?data-src="(.*?)"',r[0])
#             for j in r1:
#                 img=requests.get(url_all2+j[1]).content
#                 with open(image_path+'\\'+j[0],'wb') as f:
#                     f.write(img)
#         else:
#             print(1,e[-1][0][1])
#         r=re.findall(r'各阶段图标与战斗形象</span></h2>.*?成长曲线',str(soup_all),re.S)
#         if len(r)>0:
#             r1=re.findall(r'img alt="(.*?)".*?data-src="(.*?)"',r[0])
#             for j in r1:
#                 img=requests.get(url_all2+j[1]).content
#                 with open(image_path+'\\'+j[0],'wb') as f:
#                     f.write(img)
#         else:
#             print(2,e[-1][0][1])
    with open(all_file_path+'\\general_view.json','w',encoding='utf-8') as f:
        json.dump(e,f,ensure_ascii=False)
def update_lizhuang():
    url_all2=r'https://fgo.wiki'
    url_lizhuang=r'https://fgo.wiki/w/%E7%A4%BC%E8%A3%85%E5%9B%BE%E9%89%B4'
    all_file_path=r'F:\jupyter_notebook_my_code\pictures\fgo_cal\lizhuangtujian'
    b=BeautifulSoup(requests.get(url_lizhuang).text,'html5lib')
    r=re.findall(r'var raw_str = "(.*?)\\n(.*?)";',str(b))
    d=r[0][0].split(',')
    e=r[0][1].split(r'\n')
    list1=[]
    list2=[]
    for i in e[350:]:
        g=i.split(',')
        g[3]=g[3].replace('/','_').replace(':','_')
        filepath=all_file_path+'\\'+g[0]+'_'+g[3]
        if not os.path.exists(filepath):
            os.mkdir(filepath)
        list2=[]
        for j in range(len(g)):
            list2.append([d[j],g[j]])
        with open(filepath+'\\detail.json','w',encoding='utf-8') as f:
            json.dump(list2,f,ensure_ascii=False)
        img=requests.get(url_all2+g[13]).content
        with open(filepath+'\\'+'礼装'+g[0]+'.jpg','wb') as f:
            f.write(img)
def update_formulation():
    url=r'https://fgo.wiki/w/%E6%B8%B8%E6%88%8F%E6%95%B0%E6%8D%AE%E5%9F%BA%E7%A1%80'
    b=str(BeautifulSoup(requests.get(url).text,'html5lib'))
    filepath=r'F:\jupyter_notebook_my_code\pictures\fgo_cal\formulation_data'
    
    
    r=re.findall('行动优先度.+职阶克制关系',b,re.S)
    r1=re.findall('<tr>.*?</tr>',r[0],re.S)
    #print(r1)
    d={}
    l=['伤害系数','集星权重','掉星率','充能格数','从者行动次数','行动优先度']
    for i in r1:
        r2=re.findall('.+title="(.*?)"(.+)',i,re.S)
        r3=re.findall('<td>(.*?)\n*</td>',r2[0][1],re.S)
        d[r2[0][0]]=[[l[j],r3[j]] for j in range(len(l))]
    with open(filepath+r'\class_detail.json','w',encoding='utf-8') as f:
        json.dump(d,f,ensure_ascii=False)
            
    r=re.findall('攻\\\\防(.*?)</tr>(.+)',b,re.S)
    fang=re.findall('title="(.*?)"',r[0][0])
    #r=re.findall(
    r1=re.findall('(.*?)克制关系图.+',r[0][1],re.S)
    r2=re.findall('<tr>(.*?)</tr>',r1[0],re.S)
    gong=[]
    counter=[]
    for i in r2:
        gong.append(re.findall('title="(.*?)"',i)[0])
        counter.append(re.findall('<td.*?>(.*?)\n*</td>',i,re.S))
    with open(filepath+r'\class_counter_relationship.json','w',encoding='utf-8') as f:
        json.dump([fang,gong,counter],f,ensure_ascii=False)

        
    r=re.findall('隐藏属性克制关系.*?攻\\\\防(.*?)</tr>(.+)',b,re.S)
    fang=re.findall('<th>(.*?)\n*</th>',r[0][0])
    r1=re.findall('(.*?)</tbody>.+',r[0][1],re.S)
    r2=re.findall('<tr>(.*?)</tr>',r1[0],re.S)
    gong=[]
    counter=[]
    for i in r2:
        gong.append(re.findall('<th>(.*?)\n*</th>',i)[0])
        counter.append(re.findall('<td.*?>(.*?)\n*</td>',i,re.S))
    with open(filepath+r'\hidden_attr_counter_relationship.json','w',encoding='utf-8') as f:
        json.dump([fang,gong,counter],f,ensure_ascii=False)
    



    r=re.findall('.+每一hit结算时会抛弃小数点后两位后的所有位(.*?)NP敌补正',b,re.S)
    r1=re.findall('<tr>(.*?)</tr>',r[0],re.S)
    l=[]
    l.append(re.findall('<th>(.*?)\n*</th>',r1[0]))
    for i in r1[1:]:
        l.append(re.findall('<td>(.*?)\n*</td>',i))
    with open(filepath+r'\color_order_np_rate.json','w',encoding='utf-8') as f:
        json.dump(l,f,ensure_ascii=False)


        
    r=re.findall('.+全体宝具对多个目标伤害分别计算(.*?)一次攻击的各hit单独计算，再求和',b,re.S)
    r1=re.findall('<tr>(.*?)</tr>',r[0],re.S)
    l=[]
    l.append(re.findall('<th>(.*?)\n*</th>',r1[0]))
    for i in r1[1:]:
        l.append(re.findall('<td>(.*?)\n*</td>',i))
    with open(filepath+r'\color_order_damage_rate.json','w',encoding='utf-8') as f:
        json.dump(l,f,ensure_ascii=False)
r1=update_servant()
