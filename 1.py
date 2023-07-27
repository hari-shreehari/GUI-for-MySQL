from tkinter import *
from tkinter import messagebox
import tkinter
import mysql.connector as mc

#creating window
ws = Tk()
ws.title('My SQL Table Creator')
ws.geometry('1920x1080')
ws.config(bg='#82E0AA')

#To set the primary key
def pkey():
    global cur, liname,tbg,pop_win,opti
    pop_win=Toplevel()
    pop_win.geometry("150x75")
    pop_win.config(bg='#FFF226')
    opti=tkinter.StringVar(pop_win)
    opti.set("Select primary key : ")
    pk=tkinter.OptionMenu(pop_win,opti ,*liname)
    pk.grid(row=50,column=50)
    
    (Button(pop_win,text=" Set primary key ", command=build_table,highlightbackground="#141414",highlightthickness=2)).grid(row=70,column=50)

#To insert values into tabel created
def create():
    global cur, tbg,re,ce,liname,con,v,ve
    t=[]
    for i in re:
        col_entries=[]
        for j in i:
            col_entries.append(eval(j.get()))
        t.append(col_entries)
        
    ve=[]
    for a in range(len(t[0])):
        v=[]
        for b in range(len(t)):
            v.append(t[b][a])
        ve.append(list(v))

    for i in ve:
        col=list(liname)
        for j in i:
            if (str(j).upper())=='NULL' :
                ind=i.index(j)
                col.pop(ind)
                i.pop(ind)
            s=str(col)
            ls=list(s)
            for a in range(ls.count("'")):
                ls.remove("'")
            for b in range(ls.count("[")):
                ls.remove("[")
                ls.remove("]")
            covl=''.join(ls)
        que=f"insert into {tbg} ({covl}) values {tuple(i)}"
        cur.execute(que)

    con.commit()
    messagebox.showinfo("Success","Table created succesfully !! ")
    ws.destroy()

#Table layout
def build_table():
    global cur, rng,cng,ce,re,liname,pop_win,opti
    pn=opti.get()
    q=f"alter table {tbg} add primary key ({pn})"
    cur.execute(q)
    pop_win.destroy()
    
    popup_win=Toplevel()
    popup_win.geometry('1920x1080')
    popup_win.config(bg='#44F2EF')

    re=[]
    for k in range(len(liname)):
        t=liname[k]
        lb=Label(popup_win,text=t,highlightbackground="#141414",highlightthickness=2)
        lb.grid(row=0,column=(k+5)*5)
        ce=[]
        for i in range(int(rng)):
            e=Entry(popup_win,highlightbackground="#141414",highlightthickness=2)
            e.grid(row=i+2,column=(k+5)*5)
            ce.append(e)
        re.append(ce)
        
    Button(popup_win, text=" Create table ", command=create).grid(row=(int(rng)+10),column=(int(cng)+10)*5)
            
#Use entered details            
def fetch():
    global cur, licon, liname,q,tbg,popup_win2
    licon=[]
    liname=[]
    for i in cconstlst:
        licon.append(i.get())
    for j in cnamelst:
        liname.append(j.get())
    q='create table '
    if len(liname)==len(licon):
        for i in range(len(licon)):
            if licon[i] == 'String':
                licon[i]='Varchar(225)'
        qm=str(tbg)+' ('
        for a in range(len(liname)):
            qm+=liname[a]+' '+licon[a]+', '
        q=q+qm[:-2]+')'
        cur.execute(q)
    popup_win2.destroy()
    pkey()

#Get details about column       
def entry():
    global con,cur,dbe,tbe,cne,rne,cconstlst,cnamelst,dbg,tbg,cng,rng,popup_win2,une,pwe
    ung=une.get()
    pwg=pwe.get()
    dbg=dbe.get()
    tbg=tbe.get()
    cng=cne.get()
    rng=rne.get()

    con=mc.connect(host='localhost', username=ung, password=pwg)
    cur=con.cursor()
    cur.execute("Show databases")
    d=cur.fetchall()
    if (dbg,) not in d:
        cur.execute(f'create database {dbg}')
    cur.execute(f'use {dbg}')
    
    cur.execute("Show tables")
    t=cur.fetchall()
    if (tbg,) in t:
        messagebox.showinfo("Error",f"Table named {tbg} already exists in provided database !! ")
    else:
        popup_win2=Toplevel()
        popup_win2.wm_title("Column headers ")
        s=str(cng*100)
        g='500x'+s
        popup_win2.geometry(g)
        popup_win2.config(bg='#A569BD')
        cnamelst=[]
        cconstlst=[]
        choices=['Tinyint','Smallint','Integer','Bigint','Float','String','Date','Datetime','Year']
        for i in range(int(cng)):
            l=Label(popup_win2,text=f"Enter column {(i+1)} name : ",highlightbackground="#141414",highlightthickness=2)
            l.grid(row=20+(5*i), column=50)
            e=tkinter.Entry(popup_win2,highlightbackground="#141414",highlightthickness=2)
            e.grid(row=20+(5*i), column=150)
            opt=tkinter.StringVar(popup_win2)
            opt.set("Select data type constraints : ")
            c=tkinter.OptionMenu(popup_win2,opt ,*choices)
            c.grid(row=20+(5*i), column=250)
            cconstlst.append(opt)
            cnamelst.append(e)
        (Button(popup_win2,text="OK", command=(fetch))).grid(row=((int(cng)+int(10))*int(100)),column=200)
    con.commit()

#Get details on connection
def register():
    global cur, dbe,tbe,cne,rne,une,pwe
    (Label(ws,text="Enter the required details : ",font='Magneto 30 bold',highlightbackground="#141414",highlightthickness=2).place(x=300,y=30))
    (Label(ws,text="Enter your mysql user_name : ",font='Castellar 12 bold',highlightbackground="#141414",highlightthickness=2).place(x=300,y=120))
    une=tkinter.Entry(ws,highlightbackground="#141414",highlightthickness=2)
    une.place(x=800,y=120)
    (Label(ws,text="Enter your mysql password : ",font='Castellar 12 bold',highlightbackground="#141414",highlightthickness=2).place(x=300,y=160))
    pwe=tkinter.Entry(ws,highlightbackground="#141414",highlightthickness=2)
    pwe.place(x=800,y=160)
    (Label(ws,text="Enter a database name : ",font='Castellar 12 bold',highlightbackground="#141414",highlightthickness=2).place(x=300,y=200))
    dbe=tkinter.Entry(ws,highlightbackground="#141414",highlightthickness=2)
    dbe.place(x=800,y=200)
    (Label(ws,text="Enter a new table name : ",font='Castellar 12 bold',highlightbackground="#141414",highlightthickness=2).place(x=300,y=240))
    tbe=tkinter.Entry(ws,highlightbackground="#141414",highlightthickness=2)
    tbe.place(x=800,y=240)
    (Label(ws,text="Enter a number of Columns (below 10) : ",font='Castellar 12 bold',highlightbackground="#141414",highlightthickness=2).place(x=300,y=280))
    cne=tkinter.Entry(ws,highlightbackground="#141414",highlightthickness=2)
    cne.place(x=800,y=280)
    (Label(ws,text="Enter a number of Rows (below 25) : ",font='Castellar 12 bold',highlightbackground="#141414",highlightthickness=2).place(x=300,y=320))
    rne=tkinter.Entry(ws,highlightbackground="#141414",highlightthickness=2)
    rne.place(x=800,y=320)
    (Button(ws,highlightbackground="#141414",highlightthickness=2,text="Confirm", command=entry)).place(x=600,y=380)

#Main
register()
con.commit()
ws.mainloop()
con.close()
