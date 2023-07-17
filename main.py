from tkinter import *
from tkinter import messagebox as mb
from PIL import ImageTk,Image  
import mysql.connector as mysql
import random
import datetime
from mysql.connector import Error




connection = mysql.connect(
    host='localhost',
    user='root',
    password='lmaosql@101',
    port=3306,
)

mycursor = connection.cursor()


mycursor = connection.cursor()


if connection.is_connected():
    
    print("SUCCESSFULLY CONNECTED TO THE DATABASE")
    
else:
    
    print("PROBLEM IN CONNECTING TO THE DATABASE")


def drop_car():
    try:
        mycursor.execute('DROP database CarParking')

        Label(admin_page_1,text="Dropped Database successfully",fg="green").grid(column=5,row=6)
    except:
        mb.showerror("Database Error", "Database already dropped")
        
  
def drop_bike():

    try:
        mycursor.execute('DROP database BikeParking')

        Label(admin_page_2,text="Dropped Database successfully",fg="green").grid(column=5,row=6)
    except:
        mb.showerror("Database Error", "Database already dropped")
        

def createdatabase_car():
    try:
        mycursor.execute('CREATE database CarParking')

        mycursor.execute('USE CarParking')

        Label(admin_page_1,text="Created Database successfully",fg="green").grid(column=5,row=4)
    except:
        mb.showerror("Database Error", "Database already created")
        

def createdatabase_bike():

    try:
        mycursor.execute('CREATE database BikeParking')

        mycursor.execute('USE BikeParking')

        Label(admin_page_2,text="Created Database successfully",fg="green").grid(column=5,row=4)
    except:
        mb.showerror("Database Error", "Database already created")




def cost():
    

    a=cost_1.get()
    cost1=int(a)

    b=cost_2.get()
    cost2=int(b)
    

    sql = 'INSERT INTO Cost values(%s,%s)'

    mycursor.execute(sql,(cost1,cost2))
    connection.commit()



def tables_car():
    try:
        mycursor.execute('CREATE table Customer(Vehicle_Number INT UNIQUE,Entry_Time TIME,Exit_Time TIME DEFAULT NULL,Parking_Spot INT,Availability Varchar(3))')
        mycursor.execute('CREATE table NumberOfSpots(Parking_Spot_Number INT NOT NULL,Availability VARCHAR(3))')

        mycursor.execute('CREATE table Spots(NumberOfSpots INT NOT NULL)')
        mycursor.execute('CREATE table EntryTime(CarNumber INT(4),Entry DOUBLE)')
        mycursor.execute('CREATE table Cost(Initial INT,Supplementary INT)')
        Label(admin_page_1,text="Created tables successfully",fg="green").grid(column=5,row=8)
    except:
        mb.showerror("Table Error", "Tables already created/No database selected")
        

def tables_bike():
    try:
        mycursor.execute('CREATE table Customer(Vehicle_Number INT UNIQUE,Entry_Time TIME,Exit_Time TIME DEFAULT NULL,Parking_Spot INT,Availability Varchar(3))')
        mycursor.execute('CREATE table NumberOfSpots(Parking_Spot_Number INT NOT NULL,Availability VARCHAR(3))')

        mycursor.execute('CREATE table Spots(NumberOfSpots INT NOT NULL)')
        mycursor.execute('CREATE table EntryTime(CarNumber INT(4),Entry DOUBLE)')
        mycursor.execute('CREATE table Cost(Initial INT,Supplementary INT)')
        
        Label(admin_page_2,text="Created tables successfully",fg="green").grid(column=5,row=8)
    except:
        mb.showerror("Table Error", "Tables already created/No database selected")

                    
def admin():
    parking_spots=spots.get()
    num=int(parking_spots)
    
    sql1 = 'INSERT INTO NumberOfSpots values(%s,%s)'

    for i in range(1,num+1):

        i = (i,'YES')
        
        mycursor.execute(sql1,i)


    num = (num,)
    sql = 'INSERT INTO Spots values(%s)'
    mycursor.execute(sql,num)

    connection.commit()
    
    mycursor.execute("SELECT * FROM Spots")
    op = mycursor.fetchall()
    
    global x
    x=0

    global numspots
    numspots=op[0][0]

    

    connection.commit()
    

def car_admin_save_button():
    try:
        
        admin()
        cost()
        Label(admin_page_1,text="Updated successfully",fg="green",width=30).grid(column=5,row=20)
    except:
        mb.showerror("Entry Error!", "Invalid entries")
        

def bike_admin_save_button():
    
    try:
        
        admin()
        cost()
        Label(admin_page_2,text="Updated successfully",fg="green",width=30).grid(column=5,row=20)
    except:
        mb.showerror("Entry Error!", "Invalid entries")

        
def EntryPoint():
    if a.get()=="Car":
        mycursor.execute('USE CarParking')
    elif a.get()=="Bike":
        mycursor.execute('USE BikeParking')
    
    entry_1=en.get()
    Vehiclenumber=int(entry_1)
    x+=1

    while x<=numspots:
    
        if entry_1=="":
            mb.showerror("Entry Error", "Entry must be filled")
        elif not(entry_1.isdigit()):
            mb.showerror("Entry Error", " The Entry must be in digits")
        elif len(entry_1)!=6 :
            mb.showerror("Entry Error", " The Entry must have 6 digits")
        mycursor.execute("select Vehicle_Number from Customer")
        data=mycursor.fetchall()
        if (Vehiclenumber,) in data:
            mb.showerror("Entry Error", " duplicate entry!!!")
        else:
            CurrentTime = datetime.datetime.now()
            hour = CurrentTime.hour
            minute = CurrentTime.minute
    
            time = hour+(minute/60)
            Time = round(time,2)

            sql = 'INSERT INTO EntryTime values(%s,%s)'
            mycursor.execute(sql,(Vehiclenumber,Time))

            mycursor.execute("SELECT * FROM Spots")
            output = mycursor.fetchall()
            y=0

            for x in output:

                NumberOfSpots = x

                y = int(NumberOfSpots[0])

            random1 = random.randint(0,y)
            random1 = (random1,)

            sql = 'SELECT Availability FROM NumberOfSpots WHERE Parking_Spot_Number=%s'

            mycursor.execute(sql,random1)
            output = mycursor.fetchall()
        
            for x in output:

                y = str(x[0])



            if y == 'YES':
        
                sql = "UPDATE NumberOfSpots SET Availability='NO' WHERE Parking_Spot_Number=%s"

                mycursor.execute(sql,random1)

            else:

                while y != 'YES':

                    sql = 'SELECT Availability FROM NumberOfSpots WHERE Parking_Spot_Number=%s'

                    mycursor.execute(sql,random1)

                    output = mycursor.fetchall()

                    for x in output:

                        y = str(x[0])

                else:

                    sql = "UPDATE NumberOfSpots SET Availability='NO' WHERE Parking_Spot_Number=%s"

                    mycursor.execute(sql,random1)



            for x in random1:

                random1 = int(x)
            mb.showinfo('The spot is:',random1)

            sql = 'INSERT INTO Customer(Vehicle_Number,Entry_Time,Parking_Spot) values(%s,%s,%s)'
    
            mycursor.execute(sql,(Vehiclenumber,CurrentTime,random1))

            connection.commit()

            entry_pg.withdraw()

            entry_page()
            
    else:

        mb.showerror("Full", "No parking spot available")


def ExitPoint():

    if b.get()=="Car":
        mycursor.execute('USE CarParking')
    elif b.get()=="Bike":
        mycursor.execute('USE BikeParking')

    CurrentTime = datetime.datetime.now()
    hour = CurrentTime.hour
    minute = CurrentTime.minute
    
    time = hour+(minute/60)
    Time = round(time,2)
    
    entry_2=ex.get()
    Vehiclenumber=int(entry_2)

    if entry_2=="":
        mb.showerror("Entry Error", "Entry must be filled")
    elif len(entry_2)!=6:
        mb.showerror("Entry Error", " The length of entry must be 6")
    elif not(entry_2.isdigit()):
        mb.showerror("Entry Error", " The Entry must be in digits")
    elif len(entry_2)==6 and entry_2.isdigit():

        sql = 'UPDATE Customer SET Exit_Time=%s WHERE Vehicle_Number=%s'
        mycursor.execute(sql,(CurrentTime,Vehiclenumber))

        A="Out"
    

        sql = 'UPDATE Customer set Availability=%s WHERE Vehicle_Number=%s'
        mycursor.execute(sql,(A,Vehiclenumber))
    
        Vehiclenumber = (Vehiclenumber,)

        sql = 'SELECT Entry from EntryTime where CarNumber=%s'
        mycursor.execute(sql,Vehiclenumber)

        output = mycursor.fetchall()

        for x in output:

            Time1 = float(x[0])

        FinalTime = Time1-Time

        connection.commit()

        sql = 'SELECT * from Cost'
        mycursor.execute(sql)

        output = mycursor.fetchall()

        for x in output:

            Cost1 = float(x[0])

            Cost2 = float(x[1])

        FinalCost = Cost1+((FinalTime-1)*Cost2)

        FinalCost = int(FinalCost)

        A="Out"
        Vehiclenumber=int(entry_2)

        sql = 'UPDATE Customer set Availability=%s WHERE Vehicle_Number=%s'
        mycursor.execute(sql,(A,Vehiclenumber))

        mb.showinfo('The cost is',FinalCost)
        
        exit_pg.withdraw()

        exit_page()
    




def login():
    mainpage.withdraw()
    global log
    log=Tk()
    log.title("log")
    log.geometry("400x400")

    global username
    global password

    Label(log,text="").pack()
    Label(log,text="").pack()
    Label(log,text="").pack()
    Label(log,text="").pack()
    

    Label(log,text="USERNAME",font="bold",width="50",).pack()
    username = Entry(log,width="30")
    username.pack()
    Label(log,text="").pack()

    Label(log,text="PASSWORD",font="bold",width="50",).pack()
    password=Entry(log,width="30",show="*")
    password.pack()
    
    Label(log,text="").pack()
    Button(log,text="LOGIN",font="bold",width="20",bg="black",fg="white",command=_login_btn_clicked).pack()
    Label(log,text="").pack()
    Label(log,text="").pack()
    Label(log,text="").pack()
    Button(log,text="MAINPAGE",font="bold",width="12",bg="red",fg="white",command=log_to_mainpage).pack()
    Label(log,text="").pack()
    Label(log,text="").pack()
    Label(log,text="").pack()


def _login_btn_clicked():
    u = username.get()
    p = password.get()

    if u == "admin" and p == "password":
        car_or_bike()
    elif u=="" and p=="":
        mb.showerror("Login Error","Please enter your username and password!")
    elif u=="":
        mb.showerror("Login Error","Please enter your username!")
    elif p=="":
        mb.showerror("Login Error","Please enter your password!")
    else:
        mb.showerror("Login Error", "Incorrect Username or Password")

    
def quit1():
    if mb.askokcancel("QUIT","You want to quit "):
        mainpage.destroy()


def car_or_bike():
    log.withdraw()
    global c_or_b_pg 
    global user_pg
    c_or_b_pg=Tk()
    c_or_b_pg.title("Vehicle page")
    c_or_b_pg.geometry("320x300")
    
    Label(c_or_b_pg,text="").pack()
    Label(c_or_b_pg,text="").pack()
    Button(c_or_b_pg,text="Car Management",font="bold",width="20",bg="black",fg="white",command=car_admin_pg).pack()
    Label(c_or_b_pg,text="").pack()

    Label(c_or_b_pg,text="OR",font="bold").pack()
    Label(c_or_b_pg,text="").pack()


    Button(c_or_b_pg,text="Bike Management",font="bold",width="20",bg="black",fg="white",command=bike_admin_pg).pack()
    Label(c_or_b_pg,text="").pack()
    Button(c_or_b_pg,text="Find a vehicle",font="bold",width="10",bg="green",fg="white",command=find_vehicle).pack()
    Label(c_or_b_pg,text="").pack()
    Label(c_or_b_pg,text="").pack()
    Button(c_or_b_pg,text="MAINPAGE",font="bold",width="10",bg="red",fg="white",command=vehicle_page_to_mainpage).pack()


def find_vehicle():
    
    c_or_b_pg.withdraw()
    global find_vehicle_pg
    find_vehicle_pg=Tk()
    find_vehicle_pg.title("Entry page")
    find_vehicle_pg.geometry("250x300")
    
    
    Label(find_vehicle_pg,text="").pack()
    Label(find_vehicle_pg,text="Enter the Vehicle number:",font="bold",width="20").pack()
    
    
    global find
    find=Entry(find_vehicle_pg,width="30")
    find.pack()
   
    Label(find_vehicle_pg,text="").pack()

    global a
    
    a=StringVar(find_vehicle_pg)
    a.set("Car")
    
    drop=OptionMenu(find_vehicle_pg,a,"Car","Bike")
    drop.pack()
    
   
    Label(find_vehicle_pg,text="").pack()
    
    Button(find_vehicle_pg,text="Find",font="bold",width="8",bg="green",fg="white",command=finding_vehicle).pack()
    Label(find_vehicle_pg,text="").pack()

    Button(find_vehicle_pg,text="Back",font="bold",width="8",bg="red",fg="white",command=back_findvehicle_pg).pack()
    


def finding_vehicle():
    if a.get()=="Car":
        mycursor.execute('USE CarParking')
    elif a.get()=="Bike":
        mycursor.execute('USE BikeParking')

    entry_1=find.get()
    VehicleNo=int(entry_1)

    if entry_1=="":
        mb.showerror("Entry Error", "Entry must be filled")
    elif len(entry_1)!=6:
        mb.showerror("Entry Error", " The length of entry must be 6")
    elif not(entry_1.isdigit()):
        mb.showerror("Entry Error", " The Entry must be in digits")
    elif len(entry_1)==6 and entry_1.isdigit():


        VehicleNo=(VehicleNo,)

        sql = 'SELECT Parking_Spot FROM Customer WHERE Vehicle_Number=%s'

        mycursor.execute(sql,VehicleNo)

        output = mycursor.fetchall()

        print(output)

        y=''
        for x in output:
        
            y = int(x[0])
            
            
        
        if len(output)>0:
            
            mb.showinfo('Vehicle at spot no.',y)
        else:
            
            mb.showinfo('Search failed','Vehicle not found!!!')

def bike_admin_pg():
    c_or_b_pg.withdraw()
    global admin_page_2  
    admin_page_2=Tk()
    admin_page_2.title("Admin page")
    admin_page_2.geometry("500x550")
    Label(admin_page_2,text="").grid(column=1,row=1)
    Label(admin_page_2,text="").grid(column=2,row=1)
    Label(admin_page_2,text="").grid(column=3,row=1)
    Label(admin_page_2,text="").grid(column=4,row=1)
    
    
    a=Label(admin_page_2,text="Editing options:",font="40",width="50",fg="red").grid(column=5,row=1)
    Label(admin_page_2,text="").grid(column=5,row=2)
    Button(admin_page_2,text="Create Database",font="bold",width="15",bg="black",fg="white",command=createdatabase_bike).grid(column=5,row=3)
    Label(admin_page_2,text="").grid(column=5,row=4)
        
    Button(admin_page_2,text="Drop Database",font="bold",width="15",bg="black",fg="white",command=drop_bike).grid(column=5,row=5)
    Label(admin_page_2,text="").grid(column=5,row=6)
    
    Button(admin_page_2,text="Create Tables",font="bold",width="15",bg="black",fg="white",command=tables_bike).grid(column=5,row=7)
    Label(admin_page_2,text="").grid(column=5,row=8)

    global spots
    global cost_1
    global cost_2
    
    Label(admin_page_2,text="Enter number of parking spots available",font="30").grid(column=5,row=9)
    
    
    spots=Entry(admin_page_2,width="15")
    spots.grid(column=5,row=11)
    Label(admin_page_2,text="").grid(column=5,row=12)
    
    Label(admin_page_2,text="Enter the cost for the first hour",font="30").grid(column=5,row=13)
    cost_1=Entry(admin_page_2,width="15")
    cost_1.grid(column=5,row=14)
    Label(admin_page_2,text="").grid(column=5,row=15)

    Label(admin_page_2,text="Enter the cost for trailing hours",font="30").grid(column=5,row=16)
    cost_2=Entry(admin_page_2,width="15")
    cost_2.grid(column=5,row=17)
    Label(admin_page_2,text="").grid(column=5,row=18)
    
    Button(admin_page_2,text="SAVE",font="bold",width="10",bg="green",fg="white",command=bike_admin_save_button).grid(column=5,row=19)
    Label(admin_page_2,text="").grid(column=5,row=20)
    Label(admin_page_2,text="").grid(column=5,row=21)
    
    Button(admin_page_2,text="BACK",font="bold",width="10",bg="red",fg="white",command=back_bike_pg).grid(column=5,row=22)
    


def car_admin_pg():
    c_or_b_pg.withdraw()
    global admin_page_1   
    admin_page_1=Tk()
    admin_page_1.title("Car management page")
    admin_page_1.geometry("500x550")
    Label(admin_page_1,text="").grid(column=1,row=1)
    Label(admin_page_1,text="").grid(column=2,row=1)
    Label(admin_page_1,text="").grid(column=3,row=1)
    Label(admin_page_1,text="").grid(column=4,row=1)
    
    
    a=Label(admin_page_1,text="Editing options:",font="40",width="50",fg="red").grid(column=5,row=1)
    Label(admin_page_1,text="").grid(column=5,row=2)
    Button(admin_page_1,text="Create Database",font="bold",width="15",bg="black",fg="white",command=createdatabase_car).grid(column=5,row=3)
    Label(admin_page_1,text="").grid(column=5,row=4)
        
    Button(admin_page_1,text="Drop Database",font="bold",width="15",bg="black",fg="white",command=drop_car).grid(column=5,row=5)
    Label(admin_page_1,text="").grid(column=5,row=6)
    
    Button(admin_page_1,text="Create Tables",font="bold",width="15",bg="black",fg="white",command=tables_car).grid(column=5,row=7)
    Label(admin_page_1,text="").grid(column=5,row=8)

    global spots
    global cost_1
    global cost_2
    
    Label(admin_page_1,text="Enter number of parking spots available",font="30").grid(column=5,row=9)
    
    
    spots=Entry(admin_page_1,width="15")
    spots.grid(column=5,row=11)
    Label(admin_page_1,text="").grid(column=5,row=12)
    
    Label(admin_page_1,text="Enter the cost for the first hour",font="30").grid(column=5,row=13)
    cost_1=Entry(admin_page_1,width="15")
    cost_1.grid(column=5,row=14)
    Label(admin_page_1,text="").grid(column=5,row=15)

    Label(admin_page_1,text="Enter the cost for trailing hours",font="30").grid(column=5,row=16)
    cost_2=Entry(admin_page_1,width="15")
    cost_2.grid(column=5,row=17)
    Label(admin_page_1,text="").grid(column=5,row=18)
    
    Button(admin_page_1,text="SAVE",font="bold",width="10",bg="green",fg="white",command=car_admin_save_button).grid(column=5,row=19)
    Label(admin_page_1,text="").grid(column=5,row=20)
    Label(admin_page_1,text="").grid(column=5,row=21)
    
    Button(admin_page_1,text="BACK",font="bold",width="10",bg="red",fg="white",command=back_car_pg).grid(column=5,row=22)
    
    
    
def user_page():
    mainpage.withdraw()
    global user_pg
    user_pg=Tk()
    user_pg.title("USER page")
    user_pg.geometry("300x300")
    
    Label(user_pg,text="").pack()
    Label(user_pg,text="").pack()
    Button(user_pg,text="ENTRY POINT",font="bold",width="20",bg="black",fg="white",command=entry_page).pack()
    Label(user_pg,text="").pack()

    Label(user_pg,text="OR",font="bold").pack()
    Label(user_pg,text="").pack()


    Button(user_pg,text="EXIT POINT",font="bold",width="20",bg="black",fg="white",command=exit_page).pack()
    Label(user_pg,text="").pack()
    Label(user_pg,text="").pack()
    Label(user_pg,text="").pack()
    Button(user_pg,text="MAINPAGE",font="bold",width="10",bg="red",fg="white",command=user_to_mainpage).pack()





def entry_page():
    
    user_pg.withdraw()
    global entry_pg
    entry_pg=Tk()
    entry_pg.title("Entry page")
    entry_pg.geometry("300x350")
    
    
    Label(entry_pg,text="").pack()
    Label(entry_pg,text="Enter the Vehicle number:",font="bold",width="20").pack()
    
    
    global en
    en=Entry(entry_pg,width="30")
    en.pack()
   
    Label(entry_pg,text="").pack()

    global a
    
    a=StringVar(entry_pg)
    a.set("Car")
    
    drop=OptionMenu(entry_pg,a,"Car","Bike")
    drop.pack()
    
   
    Label(entry_pg,text="").pack()

    Button(entry_pg,text="NEXT",font="bold",width="8",bg="blue",fg="white",command=EntryPoint).pack()
    Label(entry_pg,text="").pack()
    Button(entry_pg,text="BACK",font="bold",width="8",bg="red",fg="white",command=back_entry).pack()

    
    
    

def exit_page():
    user_pg.withdraw()
    global exit_pg
    exit_pg=Tk()
    exit_pg.title("Exit page")
    exit_pg.geometry("300x350")
    

    Label(exit_pg,text="").pack()
    Label(exit_pg,text="Enter the Vehicle number:",font="bold",width="20").pack()
    global ex
    ex=Entry(exit_pg,width="30")
    ex.pack()
    
    Label(exit_pg,text="").pack()
    global b
    b=StringVar(exit_pg)
    b.set("Car")
    
    drop=OptionMenu(exit_pg,b,"Car","Bike")
    drop.pack()
    Label(exit_pg,text="").pack()
    Button(exit_pg,text="ENTER",font="bold",width="8",bg="green",fg="white",command=ExitPoint).pack()
    Label(exit_pg,text="").pack()
    Label(exit_pg,text="").pack()
    Label(exit_pg,text="").pack()
    Button(exit_pg,text="NEXT",font="bold",width="8",bg="blue",fg="white",command=next_exit).pack()
    Label(exit_pg,text="").pack()
    Button(exit_pg,text="BACK",font="bold",width="8",bg="red",fg="white",command=back_exit).pack()
    
    



def next_exit():
    exit_pg.withdraw()
    exit_page()

    
def back_entry():
    entry_pg.withdraw()
    user_page()

    
def back_exit():
    exit_pg.withdraw()
    user_page()

    
def log_to_mainpage():
    log.withdraw()
    mainpage.deiconify()
    
def admin_to_mainpage():
    admin_page.withdraw()
    mainpage.deiconify()
    
def user_to_mainpage():
    user_pg.withdraw()
    mainpage.deiconify()

def vehicle_page_to_mainpage():
    c_or_b_pg.withdraw()
    mainpage.deiconify()

def back_car_pg():
    admin_page_1.withdraw()
    car_or_bike()

def back_bike_pg():
    admin_page_2.withdraw()
    car_or_bike()

def back_findvehicle_pg():
    find_vehicle_pg.withdraw()
    car_or_bike()
    
    
    
   
global mainpage
mainpage=Tk()
mainpage.title("Mainpage")
mainpage.geometry("430x360")

img = ImageTk.PhotoImage(Image.open("static/p.jfif"))

Label(mainpage,image=img,height="140").grid(column="5")
Label(mainpage,text="").grid(column="5")
Label(mainpage,text="").grid(column="5")
Button(mainpage,text="ADMIN",font="bold",width="16",bg="black",fg="white",command=login).grid(column="5")
Label(mainpage,text="").grid(column="5")

Label(mainpage,text="OR",font="bold").grid(column="5")
Label(mainpage,text="").grid(column="5")


Button(mainpage,text="USER",font="bold",width="16",bg="black",fg="white",command=user_page).grid(column="5")

Button(mainpage,text="QUIT",font="bold",width="10",bg="red",fg="white",command=quit1).grid(row="13")

mainpage.mainloop()