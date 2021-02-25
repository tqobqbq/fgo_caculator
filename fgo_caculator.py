import sys
sys.path.append(r'F:\Anaconda8\Lib\site-packages')
sys.path.append(r'F:\Anaconda8\pkgs')
from scipy.optimize import linprog
import json,os,re,math
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
import numpy as np
import xlrd

class FGO_caculator:
    def __init__(self,master):
        self.master=master
        self.servant_name_list=[]
        self.servant_ascention_skill_item=[]
        self.servant_pic=[]
        self.servant_tkpic=[]
        self.servant_image=[]
        self.item_pic=[]
        self.item_tkpic=[]
        self.item_image=[]
        self.top_servant_detail=None
        self.servant_text=[]
        self.item_detail=[]
        self.ft1 = tkFont.Font(family='Fixdsys', size=20, weight=tkFont.BOLD)
        self.read_data()
        self.init_widgets()
        
        
    def init_widgets(self):
        self.servant_num_per_row=3
        b=math.ceil(len(self.servant_name_list)/self.servant_num_per_row)
        self.servant_cv=tk.Canvas(self.master,width=400,height=700,scrollregion=(0,0,450,b*150))
        self.servant_cv.place(x=0,y=0)
        self.servant_cv_scrollbar=tk.Scrollbar(self.servant_cv,orient='vertical',command=self.servant_cv.yview)
        self.servant_cv_scrollbar.place(x=400,width=50,height=700)
        self.servant_cv.config(yscrollcommand=self.servant_cv_scrollbar.set)
        
        self.caculate_button=tk.Button(text='caculate',command=self.calculate).place(x=420,y=10)
        self.map_button=tk.Button(text='map',command=self.map).place(x=500,y=10)
        
        #self.repository_button=tk.Button(text='repository',command=self.repository).place(x=450,y=10)
        for i in range(len(self.servant_name_list)):
            x,y=((i%self.servant_num_per_row)*137+5),(int(i/self.servant_num_per_row)*150)
            self.servant_pic.append(Image.open(r'F:\jupyter_notebook_my_code\pictures\fgo_cal\servant_image'+'\\'+self.servant_name_list[i]+'.jpg'))
            self.servant_tkpic.append(ImageTk.PhotoImage(master=self.servant_cv,image=self.servant_pic[i]))
            self.servant_image.append(self.servant_cv.create_image(x,y,anchor=tk.NW,image=self.servant_tkpic[i]))
            self.servant_cv.tag_bind(self.servant_image[i],'<Button-1>',lambda event,i=i:self.servant_detail(event,i))
            m=self.servant_achievement[i]
            self.servant_text.append(self.servant_cv.create_text(x+70,y+130,text=str(m[0])+' '+str(m[1])+' '+str(m[2])+' '+str(m[3]),font=self.ft1))
        
#         self.item_cv=tk.Canvas(self.master,width=400,height=700,scrollregion=(0,0,400,len(self.item_list)*90))
#         self.item_cv.place(x=700,y=30)
#         self.item_cv_scrollbar=tk.Scrollbar(self.item_cv,orient='vertical',command=self.item_cv.yview)
# #         self.item_cv_scrollbar=tk.Scrollbar(itemtree,orient='vertical',command=self.item_cv.yview)
#         self.item_cv_scrollbar.place(x=380,width=20,height=700)
#         self.item_cv.config(yscrollcommand=self.item_cv_scrollbar.set)
        
        frame=tk.Frame(self.master,width=100,height=700)
        frame.place(x=1030,y=50)
        #cv2.create_window((0,0), window=frame)

        self.cv2=tk.Canvas(frame,width=100,height=700,scrollregion=(0,0,670,90*len(self.item_list)+30))
        self.cv2.place(x=0,y=0)
        
        s=ttk.Style()
        s.configure('Treeview',rowheight=90)
        adad=('name','value','all_needed','repository','already_used','remain','surplus')
        
        self.tree = ttk.Treeview(self.master, column=adad, height=7)#绝对不要show属性
        #cv2.create_window((0,40),window=self.tree)
        self.tree.place(x=430,y=40)
        
#         self.tree_scrollbar=tk.Scrollbar(self.tree,orient='vertical',command=self.tree.yview)
#         self.tree_scrollbar.place(x=580,width=10,height=700)
#         self.tree.config(yscrollcommand=self.tree_scrollbar.set)

        cv2_scrollbar=tk.Scrollbar(frame,orient='vertical',command=self.scrollbarcommand,width=10)
        cv2_scrollbar.place(x=0,height=700)
        self.cv2.config(yscrollcommand=cv2_scrollbar.set)
        
        self.tree.heading('#0', text=' Pic directory', anchor='center')
        self.tree.column('#0',width=100)
        for i in adad:
            self.tree.heading(i, text=i, anchor='w')
            self.tree.column(i, anchor='w', width=70)
#         self.tree.heading('B', text=' B', anchor='center')
#         self.tree.column('B', anchor='center', width=100)
        self.a=[]
        self.b=[]
        for i in range(len(self.item_list)):
            self.item_pic.append(Image.open(r'F:\jupyter_notebook_my_code\pictures\fgo_cal\item_image'+'\\'+self.item_list[i]+'.jpg'))
            self.item_tkpic.append(ImageTk.PhotoImage(master=self.tree,image=self.item_pic[-1]))
            self.tree.insert('', 'end', self.item_list[i],image=self.item_tkpic[-1],value=self.item_detail[i])
            e=tk.Entry(self.cv2,text=str(i),width=20)
            #e.place(x=0,y=80+i*90)
            e.place()
            e.bind('<Return>',lambda event,i=i,entry=e:self.repository(event,i,entry))
            #e.bind('<Button-1>',lambda event,e=e:e.focus_set)
            self.cv2.create_window((80,50+i*90),window=e)
            #e.insert()
        #print(self.tree.get_children())
            
    def repository(self,event,i,entry):
        self.item_detail[i][3]=entry.get()
        self.tree.item(self.item_list[i],values=self.item_detail[i])
        with open(r'F:\jupyter_notebook_my_code\pictures\fgo_cal\item_detail.json','w') as f:
            json.dump(self.item_detail,f,ensure_ascii=False)
        
    def map(self):
        self.top_map=tk.Toplevel(self.master)
        self.top_map.geometry('800x600+40+40')
        adad=('name','value','times')
        
        map_tree = ttk.Treeview(self.master, column=adad, height=7)#绝对不要show属性
        #cv2.create_window((0,40),window=self.tree)
        map_tree.place(x=0,y=0)
        
    def servant_detail(self,event,ii):
        
        filepath=r'F:\jupyter_notebook_my_code\pictures\fgo_cal\servant_detail'+'\\'+self.servant_name_list[ii]
        with open(filepath+'\\detail_view.json','r',encoding='UTF-8') as f:
            data1=json.load(f)
        if os.path.exists(filepath+'\\np_skill.json'):
            with open(filepath+'\\np_skill.json','r',encoding='UTF-8') as f:
                data2=json.load(f)
        else:
            #data2={'np_level':1,'np_type':0,'skill_level':[1,1,1],'skill_type':[0,0,0]}
            data2=[0,0,0,0,0]
        self.top_servant_detail=tk.Toplevel(self.master)
        self.top_servant_detail.geometry('800x600+40+40')
        j=0
        cv=tk.Canvas(self.top_servant_detail,width=800,height=600,scrollregion=(0,0,800,1600))
        cv.place(x=0,y=0)
        scrollbar=tk.Scrollbar(self.top_servant_detail,orient='vertical',command=cv.yview)
        scrollbar.place(x=750,width=30,height=600)
        cv.config(yscrollcommand=scrollbar.set)
        
        cv.create_window((50,10),window=tk.Label(cv,text='灵基再临'))
        a=self.servant_ascention_skill_item[ii][0]
        print(a)
        if a!=None:
            l=len(a)
            j+=30
            for k in range(l):
                s=a[k][0]+':'
                for m in range(1,len(a[k])):
                    s=s+'  '+a[k][m][0]+':'+a[k][m][1]
                cv.create_window((int(k/(math.ceil(l/2)))*350+100,(k%(math.ceil(l/2)))*30+j),window=tk.Label(cv,text=s))
            j+=30*math.ceil(l/2)+30
        self.np_label=[]
        self.skill_label=[[],[],[]]
        m=0
        d=[]
        for i in data1["noble_phantasm"]:
            d.append([])
            for k in i[3]:
                d[-1].append(k[1:])
        print(d)
        for i in range(len(data1["noble_phantasm"])):
            button=tk.Button(cv,text=data1["noble_phantasm"][i][0],command=lambda i=i,label_list=self.np_label,data=d,
                            point_list=data2,j=0,file=filepath+'\\np_skill.json':self.skill_change_type(i,label_list,data,point_list,j,file))
            cv.create_window((i*150+100,j),window=button)
            if m<len(data1["noble_phantasm"][i][3]):
                m=len(data1["noble_phantasm"][i][3])
        j+=30
        for i in range(m):
            label1=tk.Label(cv,width=100)
            cv.create_window((300,j),window=label1)
            j+=20
            label2=tk.Label(cv,width=100)
            cv.create_window((300,j),window=label2)
            j+=20
            self.np_label+=[label1,label2]
        m=[0,0,0]
        #print([k[3][1:] for k in data1["noble_phantasm"]])
        self.skill_change_type(i=data2[0],label_list=self.np_label,data=d,point_list=data2,j=0,file=filepath+'\\np_skill.json')
        for i in range(len(data1['skill'])):
            button=tk.Button(self.top_servant_detail,text=data1["skill"][i][0])
            cv.create_window((i*150+100,j),window=button)
            #self.skill_button[0]=button
            for k in range(3):
                for n in data1["skill"][i][1+k][1:]:
                    if m[k]<len(n[3]):
                        m[k]=len(n[3])
        j+=30
        for i in range(3):
            tk.Label(self.top_servant_detail,text=data1["skill"][0][1+i][0])
            for k in range(1,len(data1["skill"][0][1+i])):
                button=tk.Button(self.top_servant_detail,text=data1["skill"][0][1+i][k][0],command=lambda i=k-1,label_list=self.skill_label[i],
                                 data=[l[3] for l in data1["skill"][0][1+i][1:]],point_list=data2,j=0,
                                 file=filepath+'\\np_skill.json':self.skill_change_type(i,label_list,data,point_list,j,file))
                cv.create_window((k*150+100,j),window=button)
                #self.skill_button[1+i].append(button)
            j+=30
            for _ in range(m[i]):
                label1=tk.Label(self.top_servant_detail,width=100)
                cv.create_window((300,j),window=label1)
                j+=30
                label2=tk.Label(self.top_servant_detail,width=100)
                cv.create_window((300,j),window=label2)
                j+=30
                self.skill_label[i]+=[label1,label2]
            self.skill_change_type(i=data2[2+i],label_list=self.skill_label[i],data=[l[3] for l in data1["skill"][0][1+i][1:]],point_list=data2,j=2+i,file=filepath+'\\np_skill.json')
            
            
        b=self.servant_ascention_skill_item[ii][1]
        cv.create_window((100,j),window=tk.Label(self.top_servant_detail,text='技能强化'))
        if b != None:
            l=len(b)
            j+=20
            for k in range(l):
                s=b[k][0]+':'
                for m in range(1,len(b[k])):
                    s=s+'  '+b[k][m][0]+':'+b[k][m][1]
                cv.create_window((int(k/(math.ceil(l/3)))*250+120,(k%(math.ceil(l/3)))*30+j),window=tk.Label(self.top_servant_detail,text=s))
            j+=30*math.ceil(l/2)+30
        entry=[]
        label=[]
        for k in range(4):
            entry.append(tk.Entry(cv,width=3))
            cv.create_window((100,j),window=entry[k])
            label.append(tk.Label(cv,width=3))
            cv.create_window((150,j),window=label[k])
            label[k].config(text=str(self.servant_achievement[ii][k]))
            entry[k].bind('<Return>',lambda event,j=ii,k=k,label=label[k],entry=entry[k]:self.change_achievement(event,j,k,label,entry))
            j+=30
            
    def change_achievement(self,event,j,k,label,entry):
        s=int(entry.get())
        if s<=10 and s>=0:
            self.servant_achievement[j][k]=s
            label.config(text=str(s))
            print(j,s)
            with open(r'F:\jupyter_notebook_my_code\pictures\fgo_cal\current_achievement.json','w') as f:
                json.dump(self.servant_achievement,f,ensure_ascii=False)
            m=self.servant_achievement[j]
            self.servant_cv.itemconfig(self.servant_text[j],text=str(m[0])+' '+str(m[1])+' '+str(m[2])+' '+str(m[3]))
        
        
    def calculate(self):
        item_dict={}
        count=0
        length=len(self.item_list)
        all_needed=np.zeros(length)
        already_used=np.zeros(length)
        for i in self.servant_ascention_skill_item:
            #m1=np.zeros((len(i[0]),length))
            for j in i[0]:
                TF=int(j[0][0])<self.servant_achievement[count][0]
                for k in j[1:]:
                    if k[0] in self.item_list:
                        all_needed[self.item_list.index(k[0])]+=int(k[1])
                        if TF:
                            already_used[self.item_list.index(k[0])]+=int(k[1])
            for j in i[1]:
                b=self.servant_achievement[count]
                a=int(j[0][0])
                num=int(a<b[1])+int(a<b[2])+int(a<b[3])
                for k in j[1:]:
                    if k[0] in self.item_list:
                        all_needed[self.item_list.index(k[0])]+=int(k[1])*3
                        already_used[self.item_list.index(k[0])]+=int(k[1])*num
                
            count+=1
        repository=np.array([int(i[3]) for i in self.item_detail])
        remain=all_needed-already_used-repository
        
        workbook=xlrd.open_workbook(r"C:\Users\Administrator\Desktop\新建 XLS 工作表 (2).xls")
        worksheet=workbook.sheet_by_index(0)
        item_name_location=[[],[]]
        b=worksheet.row_values(1)
        for i in range(len(b)):
            if b[i] != '':
                item_name_location[0].append(b[i])
                item_name_location[1].append(i)
        map_name=[]
        map_dropping=[]
        nrows=worksheet.nrows  #获取该表总行数
        for i in range(nrows):
            b=worksheet.row_values(i)
            if b[0]!='' and b[1]!=None and b[0]!='エリア' and b[1]!='クエスト名':
                map_name.append(b[1])
                #print([b[j] for j in item_name_location[1]])
                map_dropping.append([1/b[j] if b[j]!='' else 0 for j in item_name_location[1]])
                                              
        self.map_dropping=np.array(map_dropping)
        bub=np.array([1]*len(map_dropping))
        res=linprog(bub,A_ub=-self.map_dropping.T,b_ub=-remain)#size(bub)=(地图数量),size(Aub_all)=(地图数量,装备数量),size(b_all)=(装备数量) res['x']为刷地图次数,res['slack']为装备余量
        res2=linprog(-remain,A_ub=self.map_dropping,b_ub=bub)#res2['slack']为地图价值比消耗体力低多少,res2['x']为装备价值
        print(res['fun'])
        print(res2['fun'])
        self.map_detail=[]
        for i in range(len(map_name)):
            if res['x'][i]>1:
                print(map_name[i],res['x'][i])
            v='%.1f' % np.dot(self.map_dropping[i],np.array(res2['x']))
            
            self.map_detail.append([map_name[i],v,'%.3f' % res['x'][i]])
        for i in range(len(self.item_list)):
            a=self.item_detail[i]
            a[1]='%.3f' % res2['x'][i]
            a[2]=str(all_needed[i])
            a[4]=str(already_used[i])
            a[5]=str(remain[i])
            a[6]='%.3f' % res['slack'][i]
            self.tree.item(self.item_list[i],values=self.item_detail[i])
        with open(r'F:\jupyter_notebook_my_code\pictures\fgo_cal\item_detail.json','w') as f:
            json.dump(self.item_detail,f,ensure_ascii=False)
        with open(r'F:\jupyter_notebook_my_code\pictures\fgo_cal\map_detail.json','w',encoding='utf-8') as f:
            json.dump(self.map_detail,f,ensure_ascii=False)
        
    def scrollbarcommand(self,*xx):
        self.cv2.yview(*xx)
        self.tree.yview(*xx)

    def np_change_type(self):
        pass
    def skill_change_type(self,i,label_list,data,point_list,j,file):
        point_list[j]=i
        with open(file,'w') as f:
            json.dump(point_list,f,ensure_ascii=False)
        for j in range(len(data[i])):
            label_list[2*j].config(text=data[i][j][0])
            s=''
            for k in data[i][j][1]:
                s+=k+'  '
            label_list[2*j+1].config(text=s)
        for j in label_list[2*len(data[i]):]:
            j.config(text='')
        
        
    def read_data(self):
        #for i in os.listdir(r'F:\jupyter_notebook_my_code\pictures\fgo_cal\servant'):
        with open(r'F:\jupyter_notebook_my_code\pictures\fgo_cal\servant_list.json','r') as f:
            self.servant_name_list=json.load(f)
        with open(r'F:\jupyter_notebook_my_code\pictures\fgo_cal\item_detail.json','r') as f:
            self.item_detail=json.load(f)
        with open(r'F:\jupyter_notebook_my_code\pictures\fgo_cal\current_achievement.json','r') as f:
            self.servant_achievement=json.load(f)
        print(len(self.servant_name_list),len(self.servant_achievement))
        if len(self.servant_name_list)>len(self.servant_achievement):
            self.servant_achievement+=[[0,1,1,1]]*(len(self.servant_name_list)-len(self.servant_achievement))
        count=0
        with open(r'F:\jupyter_notebook_my_code\pictures\fgo_cal\item_list.json','r') as f:
            self.item_list=json.load(f)
        for i in self.servant_name_list:
            self.servant_ascention_skill_item.append([None,None])
            with open(r'F:\jupyter_notebook_my_code\pictures\fgo_cal\servant'+'\\'+i+'.json') as f:
                data=json.load(f)
                for j in data:
                    if j[0]=="灵基":
                        self.servant_ascention_skill_item[-1][0]=j[1]
                    elif  j[0]=="技能":
                        self.servant_ascention_skill_item[-1][1]=j[1]
                    else:
                        print(i[0:-5],data)
#             x,y=((count%5)*137+5),(int(count/5)*150)
#             self.pic.append(Image.open(r'F:\jupyter_notebook_my_code\pictures\fgo_cal\servant_image'+'\\'+self.servant_name_list[count]+'.jpg'))
#             self.tkpic.append(ImageTk.PhotoImage(master=self.servant_cv,image=self.pic[count]))
#             self.image.append(self.servant_cv.create_image(x,y,anchor=tk.NW,image=self.tkpic[count]))
#             self.servant_cv.tag_bind(self.image[count],'<Button-1>',lambda event,i=count:self.servant_detail(event,i))
#             self.servant_text.append(self.servant_cv.create_text(x+80,y+130,text='0  000',font=self.ft1))
#             count+=1
        
                
                    
                
    
    

root=tk.Tk()
root.title("FGO计算器")
root.geometry('1100x700')
pcrc=FGO_caculator(root)
#a=pcrc.create_calculator()
root.mainloop()
