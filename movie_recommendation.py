
import pandas as pd
import numpy as np
import random
import re
from tkinter import *


movies= pd.read_csv("movies.csv",usecols=['movieId','title'])
movies


ratings=pd.read_csv("ratings.csv",usecols=['userId','movieId','rating'])
ratings


def cosine(test,fd):
    test=test.to_numpy()
    tp=fd.to_numpy()
    k=len(tp[0])-1
    simi=[]
    for i in range(len(tp)):
        c=0
        for j in range(len(tp[0])-2):
            c+=tp[i][j]*test[j]
        cosine=c/float(tp[i][k]*test[k])
        simi.append(1-cosine)
    id=fd.index.tolist()
    simi=list(zip(id,simi))
    return simi


def KNN(mn,n,fd):
    cd=cosine(mn,fd)
    distance=list(cd)
    distance.sort(key=lambda x: x[1])
    nb = []
    for i in range(n):
        nb.append(distance[i+1][0])
    frame = []
    for i in nb:
        idx=movies[movies['movieId']==i].index
        frame.append(movies.iloc[idx]['title'])
    frame=np.array(frame)
    df=pd.DataFrame(frame,index=range(1,n+1),columns=['Title'])
    return df


def name(mn):
    t=mn.split()
    mn=''
    for i in range(len(t)):
        mn+=t[i].capitalize()+' '
    return mn


def getRecommendation(movie_name,movie_count):
    movie_name=name(movie_name)
    movie_list=movies[movies['title'].str.contains(movie_name)]
    if len(movie_list):
        fd=ratings.pivot(index='movieId',columns='userId',values='rating')
        fd.fillna(0,inplace=True)
        temp=np.square(fd)
        temp=temp.sum(axis=1)
        temp=np.sqrt(temp)
        temp=temp.to_numpy()
        fd['sum']=temp
        movie_idx=movie_list.iloc[0]['movieId']
        movie_recommended=KNN(fd.loc[movie_idx],movie_count,fd)
        return movie_recommended
    else:
        return 'No Movie Found !!!\n\nCheck Your Movie Name....'


def avg():
    mx=ratings.pivot(index='movieId',columns='userId',values='rating')
    n=mx.count()
    u_avg=mx.sum(axis=0)
    u_avg=u_avg.div(n)
    for i in range(1,len(u_avg)+1):
        mx.loc[:,i].fillna(u_avg[i],inplace=True)
    mx=round(mx,1)
    c=len(mx.columns)
    m_avg=mx.sum(axis=1)
    m_avg=m_avg.div(c)
    m_avg=round(m_avg,1)
    m_avg.sort_values(inplace=True,ascending=False)
    m_avg=m_avg.loc[m_avg[:]>3.7]
    midx=m_avg.index.tolist()
    res=[]
    for i in midx:
        mid=movies[movies['movieId']==i].index
        res.append(movies.iloc[mid]['title'])
    res=np.array(res)
    return res


def randomcolor():
    color='#'
    for i in range(6):
        color+=random.choice('0123456789ABCDEF')
    return color


root = Tk()
root.geometry("800x800")
root.title('Recommendation System')
root.resizable(False,False)
root.configure(bg=randomcolor())
root.iconbitmap('icon.ico')

frame=Frame(root).place(x=20,y=0,height=400,width=760)

l1= Label(frame,text="MOVIE RECOMMENDATION SYSTEM",font=("Impact",30,"bold","italic","underline"),fg=randomcolor())
l1.place(x=100,y=10)
l2= Label(frame,text="Enter Your Favourite Movie : ",font=("Impact",20,'underline'),fg=randomcolor())
l2.place(x=120,y=75)
l3= Label(frame,text="Enter No of Movies : ",font=("Impact",20,'underline'),fg=randomcolor())
l3.place(x=120,y=145)

e1=Entry(frame,fg=randomcolor(),borderwidth=5,width=40,font=("Tisa",15))
e1.place(x=450,y=80,height=40,width=200)
e2=Entry(frame,fg=randomcolor(),borderwidth=5,font=("Tisa",15))
e2.place(x=450,y=150, height=40,width=80)

t=Text(root,borderwidth=5,wrap=WORD,padx=40,pady=40,font=("Tisa",15),state='disabled')
t.place(x=40,y=290,height=505,width=720)

r = IntVar()

def radio():
    if(r.get()):
        e1.configure(state='disabled')
        e2.configure(state='disabled')
    else:
        e1.configure(state='normal')
        e2.configure(state='normal')
        
r1=Radiobutton(frame,text='UCF',variable=r,value=1,borderwidth=5,font=("Impact",20),fg=randomcolor(),activeforeground=randomcolor(),command=radio)
r1.place(x=150,y=215)
r2=Radiobutton(frame,text='ICF',variable=r,value=0,borderwidth=5,font=("Impact",20),fg=randomcolor(),activeforeground=randomcolor(),command=radio)
r2.place(x=550,y=215)

def myClick():
    if(r.get()):
        res=avg()
        k=len(res)
        c=random.randint(0, k)
        t.configure(state='normal',fg=randomcolor(),font=("Tisa",15),pady=60,padx=80)
        t.delete(1.0,END)
        for i in range(10):
            l=str(10-i)
            if(len(l)!=1):
                 t.insert(0.0,l+'.  '+res[(c+i)%k][0]+'\n') 
            else:
                t.insert(0.0,' '+l+'.  '+res[(c+i)%k][0]+'\n')
    else:
        if(re.match("^[a-zA-Z]+[a-zA-Z0-9]*|^[0-9]+[a-zA-Z]+|^0+[a-bA-Z]*",e2.get()) ):
            t.configure(fg='red',padx=200,pady=100,font=("Tisa",18,'bold'),state='normal')
            t.delete(1.0,END)
            t.insert(0.0,'Wrong Count value!!!\n\nFill Correct Value...\n')
        else:
            if(e1.get()=='' or e2.get()==''):
                if(e1.get()=='' and e2.get()==''):
                    t.configure(fg='red',padx=200,pady=100,font=("Tisa",18,'bold'),state='normal')
                    t.delete(1.0,END)
                    t.insert(0.0,'Empty Response !!!\n\nFill Above Details...\n')
                elif(e1.get()==''):
                    t.configure(fg='red',padx=200,pady=100,font=("Tisa",18,'bold'),state='normal')
                    t.delete(1.0,END)
                    t.insert(0.0,'Empty Movie Name !!!\n\nFill Movie Name...\n')
                else:
                    t.configure(fg='red',padx=200,pady=100,font=("Tisa",18,'bold'),state='normal')
                    t.delete(1.0,END)
                    t.insert(0.0,'Empty Movies Count !!!\n\nFill Movies Count...\n')
            else:
                t.configure(state='normal')
                df=getRecommendation(e1.get(),int(e2.get()))
                if(isinstance(df,str)):
                    t.configure(fg='red',padx=200,pady=100,font=("Tisa",15,'bold'))
                    t.delete(1.0,END)
                    t.insert(0.0,df)
                else:
                    j=n=int(e2.get())+1
                    if(j>17):
                        t.configure(font=("Tisa",13),pady=30,padx=100)
                    else:
                        t.configure(font=("Tisa",15),pady=60,padx=80)
                    t.configure(fg=randomcolor())
                    t.delete(1.0,END)
                    for i in range(j-1):
                        k=str(j-i-1)
                        if(len(k)!=1):
                            t.insert(0.0,k+'.  '+df.iloc[i]['Title']+'\n') 
                        else:
                            t.insert(0.0,' '+k+'.  '+df.iloc[i]['Title']+'\n')
        t.configure(state='disabled')

b=Button(frame,text="Search",command=myClick,bg=randomcolor(),activebackground=randomcolor(),fg='white',borderwidth=7,font=("Impact",15))
b.place(x=350,y=220,width=80,height=40)

root.mainloop()

