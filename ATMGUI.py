from glob import glob
import urllib.request
from tkinter.ttk import *
from tkinter import ttk
from tkinter import *
from venv import create
from PIL import Image, ImageTk

from cmath import pi
# from distutils.util import copydir_run_2to3
import email
from http import server
from itertools import count
from math import lgamma
from operator import concat
from tkinter import INSERT
from tkinter.messagebox import NO
from tokenize import Name
import random
import ast
import itertools
import datetime
import smtplib
import string
from matplotlib.style import use
import mysql.connector
from numpy import count_nonzero, insert
from tkinter import messagebox
from tkcalendar import DateEntry
import guisql
import cv2


import base64
from PIL import Image
import pyqrcode
from pyzbar.pyzbar import decode
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet


import os
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart




root = Tk()
root.geometry("1850x1100")
root.maxsize(1850, 1100)
root.minsize(1800, 1000)
root.title("SBM BANK")


# Adding Background Image
load = Image.open("20602.jpg")
# resize_image = load.resize((1200, 600),Image.ANTIALIAS)
bg = ImageTk.PhotoImage(load)

# Create Canvas
canvas1 = Canvas(root, width=1850, height=1100)
canvas1.pack(fill="both", expand=True)
# Display image
canvas1.create_image(0, 0, image=bg, anchor="nw")


# *****************************Creating Status Bar**************************************


def internet_check():

    def connect(host='http://google.com'):
        try:
            urllib.request.urlopen(host)
            return True
        except:
            return False
    global internetsatus
    internetsatus = "Connecting...."
    if connect():
        internetsatus = "Connected"
    else:
        internetsatus = "Disconnected"
        messagebox.showerror("Internet Status", "Please Connect Internet")


internet_check()

fnamel2 = Label(root, text=f"Internet Status : {internetsatus}",
                font="comicsansms 10 bold", bg="white", relief=SUNKEN, fg="#2e3772", padx=1850, pady=20)
fnamel2.pack()
canvas1.create_window(130, 980, window=fnamel2)


# *******************************************FUNCATION************************************


# *****************************Checking a data in database******************************
mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    password='12345678',
    database='bank'
)
mycursor = mydb.cursor()


# *************************************QR AND Encoding*************************************************************
def generate_fernet_key(master_key, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA512(),
        length=32,
        salt=salt.encode(),
        iterations=100000,
        backend=default_backend()
        )
    
    
    key = base64.urlsafe_b64encode(kdf.derive(master_key.encode()))
    return key.decode("utf-8")
def decrypt_text(hash, key):
    decryptor = Fernet(key)
    text = decryptor.decrypt(hash.encode())
    return text.decode()

def encrypt_text(text, key):
    encryptor = Fernet(key)
    hash = encryptor.encrypt(text.encode())
    return hash.decode()

def generate_qr(matric_number, key):
    hashed_matric = encrypt_text(matric_number, key)
    qr = pyqrcode.create(hashed_matric)
    qr.png(custm_id + ".png", scale=6)
    

    
    
    
def account_balence():
    # *********************Finding Account Balence********************

    sql = f"SELECT SUM(ammount) FROM {user_id} WHERE txn_type='Credit'"
    mycursor.execute(sql)
    totalCr = mycursor.fetchone()
    if totalCr[0] == None:
        totalCr = 0
    else:
        totalCr = totalCr[0]

    sql = f"SELECT SUM(ammount) FROM {user_id} WHERE txn_type='Dedit'"
    mycursor.execute(sql)
    totalDr = mycursor.fetchone()
    if totalDr[0] == None:
        totalDr = 0
    else:
        totalDr = totalDr[0]
    account_bal = totalCr-totalDr

    sql = "UPDATE accounnt_data SET account_bal = %s WHERE custm_id = %s"
    val = (account_bal, user_id)

    mycursor.execute(sql, val)
    mydb.commit()

    return account_bal

# ************************loginwindow********************************


def loginwindow():
    # **********************LOG IN PAGE*******************************
    labelframe3 = LabelFrame(root, text="WELCOME TO SBM BANK", font="comicsansms 20 bold", borderwidth=3,
                             relief=SUNKEN, bg="#2e3772", fg="white", height=300, width=500)
    labelframe3.pack(fill="both", expand="yes")
    global uservalue
    global passvalue
    user = Label(labelframe3, text="Username",
                 font="comicsansms 12 bold", bg="#2e3772", fg="white")
    user.place(x=80, y=80)
    uservalue = StringVar()
    userentry = Entry(labelframe3, textvariable=uservalue)
    userentry.place(x=200, y=82)
    password = Label(labelframe3, text="Password",
                     font="comicsansms 12 bold", bg="#2e3772", fg="white")
    password.place(x=80, y=120)
    passvalue = StringVar()
    passvalue = Entry(labelframe3, textvariable=passvalue)
    passvalue.place(x=200, y=122)

    sbmt3 = Button(labelframe3, text="LOG IN", fg="white", bg="#2e3772", padx=10,
                   command=lambda: next6(labelframe3, uservalue.get(), passvalue.get()))
    sbmt3.place(x=222, y=170)

    canvas1.create_window(950, 500, window=labelframe3)


def check_data1(data, column1, tables):
    sql = f"SELECT {column1} FROM {tables}"
    mycursor.execute(sql)
    
    myresult = mycursor.fetchall()
    
    for x in myresult:
        if x[0] == data:
            return True
        
    return False
    # ******************************table Empty or not**********************


def empty(tables):
    sql = f"SELECT COUNT(*) FROM {tables}"
    mycursor.execute(sql)
    myresult = mycursor.fetchone()
    if myresult[0] == 0:
        return True
    else:
        return False


# ********************************Gen. Custm_id*******************************
def custm_id1():
    list1 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

    custm_id = ""
    while len(custm_id) != 8:
        custm_id = custm_id + str(random.choice(list1)) + \
            random.choice(string.ascii_letters)

    empt = empty("customer")
    if empt:
        return custm_id
    else:
        check_data = check_data1(custm_id, "custm_id", "customer")

        if check_data:
            custm_id1()
        else:
            return custm_id


# ***************Gen. password******************


def gen_pass():
    list3 = ['#', '@', '&', '$']
    
    list2 = [str(random.choice(list3)), random.choice(
        string.ascii_letters), random.randint(1, 9)]
    
    list4 = [random.choice(string.ascii_letters), random.randint(
        1, 9), str(random.choice(list3))]
    
    password = ""
    while len(password) != 8:
        password = password + str(random.choice(list2)) + \
            str(random.choice(list4))
            
    empt = empty("user_deta")
    if empt:
        return password
    else:
        check_data = check_data1(password, "password", "user_deta")
        if check_data:
            gen_pass()
        else:
            return password
# *********************Gen account_no************************


def gen_ac():
    account_no = "7412"
    while len(account_no) != 12:
        account_no = account_no + str(random.randint(1, 9))
    empt = empty("accounnt_data")
    if empt:
        return account_no
    else:
        check_data = check_data1(account_no, "account_no", "accounnt_data")
        if check_data:
            gen_ac()
        else:
            return account_no


def check_valid(data):

    if data == "" or data == " ":
        return True
    return False


def display_invalid_message(dataname):
    a = messagebox.askretrycancel("Notification",
                                  f"Please Enter valid {dataname}")


# ***********************************random Number(OTP)********************
def randm_num():
    
    list1 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

    rndm_num = ""
    while len(rndm_num) != 6:
        rndm_num = rndm_num + str(random.choice(list1)) + \
            random.choice(string.ascii_letters)
    return rndm_num


def next9(labelframe11, Cramnt):
    labelframe11.destroy()
    sql = f"INSERT INTO {user_id} (txn_date,ammount,txn_type) VALUES(NOW(),{Cramnt},'Credit')"
    mycursor.execute(sql)
    mydb.commit()
    labelframe12 = LabelFrame(root, text="WELCOME TO SBM BANK", font="comicsansms 20 bold", borderwidth=3,
                              relief=SUNKEN, bg="#2e3772", fg="white", height=500, width=700)
    labelframe12.pack(fill="both", expand="yes")
    account_bal = account_balence()
    Label(labelframe12, text=f"NOw Your Account Balence is {account_bal}", bg="#2e3772", fg="white",
          font="comicsansms 18 bold").place(x=240, y=20)

    canvas1.create_window(950, 500, window=labelframe12)


def next8(labelframe9, Dramnt):
    labelframe9.destroy()
    labelframe10 = LabelFrame(root, text="WELCOME TO SBM BANK", font="comicsansms 20 bold", borderwidth=3,
                              relief=SUNKEN, bg="#2e3772", fg="white", height=500, width=700)
    labelframe10.pack(fill="both", expand="yes")

    account_bal = account_balence()

    if (Dramnt > account_bal):
        a = messagebox.showerror("Notification", "Insufficient Balance")
    else:
        sql = f"INSERT INTO {user_id} (txn_date,ammount,txn_type) VALUES(NOW(),{Dramnt},'Dedit')"
        mycursor.execute(sql)
        mydb.commit()
        account_bal = account_balence()
        Label(labelframe10, text=f"Now your account Balence is {account_bal}", bg="#2e3772", fg="white",
              font="comicsansms 18 bold").place(x=240, y=20)
    canvas1.create_window(950, 500, window=labelframe10)


def next7(labelframe7, input1):
    if input1 == "1":
        labelframe7.destroy()

        labelframe8 = LabelFrame(root, text="WELCOME TO SBM BANK", font="comicsansms 20 bold", borderwidth=3,
                                 relief=SUNKEN, bg="#2e3772", fg="white", height=500, width=700)
        labelframe8.pack(fill="both", expand="yes")
        account_bal = account_balence()
        Label(labelframe8, text=f"Your Account Balence is {account_bal}", bg="#2e3772", fg="white",
              font="comicsansms 18 bold").place(x=150, y=60)

        # Label(labelframe8,text="Select Your Options", bg="#2e3772", fg="white",
        #         font="comicsansms 18 bold").place(x=240,y=40)

        canvas1.create_window(950, 500, window=labelframe8)

    if input1 == "2":
        labelframe7.destroy()

        labelframe9 = LabelFrame(root, text="WELCOME TO SBM BANK", font="comicsansms 20 bold", borderwidth=3,
                                 relief=SUNKEN, bg="#2e3772", fg="white", height=500, width=700)
        labelframe9.pack(fill="both", expand="yes")
        account_bal = account_balence()
        EntrLabel = Label(labelframe9, text="Enter Your Withdrawal Ammount", bg="#2e3772", fg="white",
                          font="comicsansms 18 bold")
        EntrLabel.place(x=150, y=60)
        drAmmount = IntVar()
        drentry = Entry(labelframe9, textvariable=drAmmount, width=30)
        drentry.place(x=250, y=150)
        sbmt7 = Button(labelframe9, text="NEXT", fg="white", bg="#2e3772",
                       padx=10, width=8, command=lambda: next8(labelframe9, drAmmount.get()))
        sbmt7.place(x=310, y=250)

        canvas1.create_window(950, 500, window=labelframe9)

    if input1 == "3":
        labelframe7.destroy()

        labelframe11 = LabelFrame(root, text="WELCOME TO SBM BANK", font="comicsansms 20 bold", borderwidth=3,
                                  relief=SUNKEN, bg="#2e3772", fg="white", height=500, width=700)
        labelframe11.pack(fill="both", expand="yes")
        account_bal = account_balence()
        EntrLabel = Label(labelframe11, text="Enter Your Deposit Ammount", bg="#2e3772", fg="white",
                          font="comicsansms 18 bold")
        EntrLabel.place(x=150, y=60)
        crAmmount = IntVar()
        crentry = Entry(labelframe11, textvariable=crAmmount, width=30)
        crentry.place(x=250, y=150)
        sbmt7 = Button(labelframe11, text="NEXT", fg="white", bg="#2e3772",
                       padx=10, width=8, command=lambda: next9(labelframe11, crAmmount.get()))
        sbmt7.place(x=310, y=250)

        canvas1.create_window(950, 500, window=labelframe11)

    if input1 == "4":
        labelframe7.destroy()

        labelframe13 = LabelFrame(root, text="WELCOME TO SBM BANK", font="comicsansms 20 bold", borderwidth=3,
                                  relief=SUNKEN, bg="#2e3772", fg="white", height=500, width=700)
        labelframe13.pack(fill="both", expand="yes")
        Label(labelframe13, text="Mini statement", bg="#2e3772", fg="white",
              font="comicsansms 18 bold").place(x=240, y=20)

        sql = f"SELECT * FROM {user_id} LIMIT 5"
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        transcation_list = []
        for x in myresult:
            transcation_list.append(x)

        Label(labelframe13, text="Sl.No   Date           Time        Amount    Type", bg="#2e3772", fg="white",
              font="comicsansms 18 bold").place(x=120, y=80)
        Label(labelframe13, text=f"{transcation_list[0][0]}       {transcation_list[0][1]}      {transcation_list[0][2]}           {transcation_list[0][3]}", bg="#2e3772", fg="white",
              font="comicsansms 18 bold").place(x=120, y=130)
        Label(labelframe13, text=f"{transcation_list[1][0]}       {transcation_list[1][1]}      {transcation_list[1][2]}           {transcation_list[1][3]}", bg="#2e3772", fg="white",
              font="comicsansms 18 bold").place(x=120, y=180)
        Label(labelframe13, text=f"{transcation_list[2][0]}       {transcation_list[2][1]}      {transcation_list[2][2]}           {transcation_list[2][3]}", bg="#2e3772", fg="white",
              font="comicsansms 18 bold").place(x=120, y=230)
        Label(labelframe13, text=f"{transcation_list[3][0]}       {transcation_list[3][1]}      {transcation_list[3][2]}           {transcation_list[3][3]}", bg="#2e3772", fg="white",
              font="comicsansms 18 bold").place(x=120, y=280)
        Label(labelframe13, text=f"{transcation_list[4][0]}       {transcation_list[4][1]}      {transcation_list[4][2]}           {transcation_list[4][3]}", bg="#2e3772", fg="white",
              font="comicsansms 18 bold").place(x=120, y=330)

        canvas1.create_window(950, 500, window=labelframe13)

def next6(labelframe3, userId, password):
    global user_id
    user_id = userId
    sql = "SELECT custm_id,password FROM user_deta WHERE custm_id= %s"
    val = (userId,)
    mycursor.execute(sql, val)
    myresult = mycursor.fetchone()
    if myresult == None:
        display_invalid_message("User ID")
        # uservalue.set("")

    elif(myresult[1] != password):
        display_invalid_message("Password")
        # passvalue.set("")

    elif(myresult[0] == userId and myresult[1] == password):
        labelframe3.destroy()
        global afterLoginWin
        def afterLoginWin():
            labelframe7 = LabelFrame(root, text="WELCOME TO SBM BANK", font="comicsansms 20 bold", borderwidth=3,
                                    relief=SUNKEN, bg="#2e3772", fg="white", height=500, width=700)
            labelframe7.pack(fill="both", expand="yes")

            Label(labelframe7, text="Select Your Options", bg="#2e3772", fg="white",
                font="comicsansms 18 bold").place(x=240, y=20)

            s = StringVar(root, "1")

            Radiobutton(labelframe7, text="Check Your Balance", font="comicsansms 11 bold",
                        variable=s, value=1, width=20).place(x=250, y=130)
            Radiobutton(labelframe7, text="Withdrawal", font="comicsansms 11 bold",
                        variable=s, value=2, width=20).place(x=250, y=180)
            Radiobutton(labelframe7, text="Deposit", font="comicsansms 11 bold",
                        variable=s, value=3, width=20).place(x=250, y=250)
            Radiobutton(labelframe7, text="Mini Statement", font="comicsansms 11 bold",
                        variable=s, value=4, width=20).place(x=250, y=300)

            sbmt7 = Button(labelframe7, text="NEXT", fg="white", bg="#2e3772",
                        padx=10, width=8, command=lambda: next7(labelframe7, s.get()))
            sbmt7.place(x=310, y=390)

            canvas1.create_window(950, 500, window=labelframe7)
        afterLoginWin()


def next5(v, labelframe6):
    if v == "1":
        labelframe6.destroy()
        loginwindow()
    else:
        quit


def next4(lableframe5, aadhart, pant, addresst, pint, cityt, accountt, employmentlt, maritalt, statet, nationalityt):
    pan_check = check_data1(pantk.get(), "pancard_no", "customer")
    addhar_check = check_data1(aadhartk.get(), "aadhar_no", "customer")

    if pan_check and addhar_check:
        a = messagebox.askretrycancel(
            "Notification", "Aadhar Number and PAN Number already Exists")
        pantk.set("")
        aadhartk.set("")
    elif pan_check:
        a = messagebox.askretrycancel("Notification",
                                      "PAN Number already Exists")
        pantk.set("")
    elif addhar_check:
        a = messagebox.askretrycancel("Notification",
                                      "Aadhar Number already Exists")
        aadhartk.set("")
    elif aadhartk.get() == "" or aadhartk.get() == " " or len(str(aadhartk.get())) > 12 or len(str(aadhartk.get())) < 12:
        a = messagebox.askretrycancel("Notification",
                                      "Please Enter Valid Aadhar card No")
        aadhartk.set("")

    elif pantk.get() == "" or pantk.get() == " " or len(str(pantk.get())) > 10 or len(str(pantk.get())) < 10:
        a = messagebox.askretrycancel("Notification",
                                      "Please Enter valid PAN No.")
    elif check_valid(addresstk.get()):
        display_invalid_message("Address")

    elif check_valid(citytk.get()):
        display_invalid_message("City")

    # elif check_valid(pintk.get()):
    #     display_invalid_message("Pin No.")
    elif check_valid(stateentry.get()):
        display_invalid_message("State")

    elif check_valid(nationalitytk.get()):
        display_invalid_message("Nationalty")

    elif check_valid(maritalentry.get()):
        display_invalid_message("Marital Status")

    elif check_valid(employmentlentry.get()):
        display_invalid_message("Employment Status")

    elif check_valid(accounttkentry.get()):
        display_invalid_message("Account Type")

    else:

        lableframe5.destroy()
        global custm_id
        custm_id = custm_id1()

        sql = "INSERT INTO customer(custm_id,f_name,l_name,dob,address,pincode,city,state,nationality,aadhar_no,pancard_no,marital_status,employment_type,email_id,contact_no) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        val = [(custm_id, str(fname1), str(lname1), str(dob1), str(addresst), str(pint), str(cityt), str(statet), str(nationalityt),
                str(aadhart), str(pant), str(maritalt), str(employmentlt), str(email1), str(contact1))]
        
        mycursor.executemany(sql, val)

        password = gen_pass()

        sql = "INSERT INTO user_deta(custm_id,password) VALUES (%s,%s)"
        val = (custm_id, password)
        mycursor.execute(sql, val)

        account_no = gen_ac()

        sql = "INSERT INTO accounnt_data(custm_id,account_no,account_type) VALUES (%s,%s,%s)"
        val = (custm_id, int(account_no), str(accountt))
        mycursor.execute(sql, val)

        

        # ***********************TXN Data*************************
        mycursor.execute(f"CREATE TABLE {custm_id} (sl_no INT AUTO_INCREMENT PRIMARY KEY,txn_date DATETIME,ammount BIGINT, txn_type VARCHAR(255))")
        
        mydb.commit()
        # **************************************Creating QR Code*************************
        
        master_key = "server master key"
        server_salt = "server salt"
        server_fernet_key = generate_fernet_key(master_key, server_salt)
        matric_number = password
        generate_qr(matric_number, server_fernet_key)
        
        # *********************Sending Mail********************
        def SendMail(ImgFileName):
       
            with open(ImgFileName, 'rb') as f:
                img_data = f.read()

            msg = MIMEMultipart()
            msg['Subject'] = 'SBM - Bank '
            msg['From'] = 'sbm.pvt.lmt@gmail.com'
            msg['To'] = emailtk.get()

            text = MIMEText(f'Welcome To SBM Bank \n Your Account is has been Successfully Opened\n Your Account Number is- {account_no}\n User Id- {custm_id}\n password- {password}')
            msg.attach(text)
            image = MIMEImage(img_data, name=os.path.basename(ImgFileName))
            msg.attach(image)

            s = smtplib.SMTP('smtp.gmail.com',587)
            s.ehlo()
            s.starttls()
            s.ehlo()
            s.login('sbm.pvt.lmt@gmail.com', 'Hmt@2295')
            s.sendmail('sbm.pvt.lmt@gmail.com', emailtk.get(), msg.as_string())
            s.quit()
            
        image= custm_id+".png"
        SendMail(image)
        
        
        
        messagebox.showinfo(
            "Notification", "Your Account has been Opened Successfuly \n User Id ,Password QR code & A/C Number has been sent on Your Email Id")

        labelframe6 = LabelFrame(root, text="WELCOME TO SBM BANK", font="comicsansms 20 bold", borderwidth=3,
                                 relief=SUNKEN, bg="#2e3772", fg="white", height=500, width=700)
        labelframe6.pack(fill="both", expand="yes")

        Label(labelframe6, text=f"Your Account has been Successfully Opned \n Your Account No. is {account_no}", bg="#2e3772", fg="white",
              font="comicsansms 12 bold").place(x=200, y=20)

        Label(labelframe6, text="What do you want Log In OR Exit", bg="#2e3772", fg="white",
              font="comicsansms 12 bold").place(x=200, y=100)

        s = StringVar(root, "1")

        Radiobutton(labelframe6, text="LOG IN", variable=s,
                    value=1).place(x=300, y=150)
        Radiobutton(labelframe6, text="EXIT", variable=s,
                    value=2).place(x=300, y=220)

        sbmt7 = Button(labelframe6, text="NEXT", fg="white", bg="#2e3772",
                       padx=10, command=lambda: next5(v.get(), labelframe6))
        sbmt7.place(x=310, y=300)

        canvas1.create_window(950, 500, window=labelframe6)


# ***********************verifying otp*************************
def next3(otp, otpinpt, lableframe4, fname):

    if otp != otpinpt:
        messagebox.showerror("Notification", "WRONG OTP")

    else:
        messagebox.showinfo("Notification", "MAIL VERIFIED")
        lableframe4.destroy()
        labelframe5 = LabelFrame(root, text="WELCOME TO SBM BANK", font="comicsansms 20 bold", borderwidth=3,
                                 relief=SUNKEN, bg="#2e3772", fg="white", height=700, width=1000)
        labelframe5.pack(fill="both", expand="yes")

        txtl = Label(labelframe5, text="Fill Your Details",
                     font="comicsansms 10 bold", bg="#2e3772", fg="white")
        txtl.place(x=20, y=10)

        # creating Varivale
        global pantk
        global aadhartk
        global pintk
        global addresstk
        global citytk
        global statetk
        global nationalitytk
        global maritaltk
        global employmenttk
        global account_typtk

        pantk = StringVar()
        aadhartk = IntVar()
        pintk = IntVar()
        addresstk = StringVar()
        citytk = StringVar()
        statetk = StringVar()
        nationalitytk = StringVar()
        maritaltk = StringVar()
        employmenttk = StringVar()
        account_typttk = StringVar()
# ***********************************Line 1**************************************
        aadharl = Label(labelframe5, text="Aadhar No.",
                        font="comicsansms 12 bold", bg="#2e3772", fg="white")
        aadharl.place(x=100, y=100)
        aadhrentry = Entry(labelframe5, textvariable=aadhartk)
        aadhrentry.place(x=300, y=100)

        panl = Label(labelframe5, text="Pan NO.",
                     font="comicsansms 12 bold", bg="#2e3772", fg="white")
        panl.place(x=550, y=100)
        panlentry = Entry(labelframe5, textvariable=pantk)
        panlentry.place(x=700, y=100)

        addressl = Label(labelframe5, text="Address ",
                         font="comicsansms 12 bold", bg="#2e3772", fg="white")
        addressl.place(x=100, y=200)
        addressentry = Entry(labelframe5, textvariable=addresstk)
        addressentry.place(x=300, y=200)

        cityl = Label(labelframe5, text="City",
                      font="comicsansms 12 bold", bg="#2e3772", fg="white")
        cityl.place(x=550, y=200)
        cityentry = Entry(labelframe5, textvariable=citytk)
        cityentry.place(x=700, y=200)

        pinl = Label(labelframe5, text="Pin Code",
                     font="comicsansms 12 bold", bg="#2e3772", fg="white")
        pinl.place(x=100, y=300)
        pinentry = Entry(labelframe5, textvariable=pintk)
        pinentry.place(x=300, y=300)

        statel = Label(labelframe5, text="State",
                       font="comicsansms 12 bold", bg="#2e3772", fg="white")
        statel.place(x=550, y=300)

        global stateentry
        stateentry = ttk.Combobox(labelframe5,
                                  values=[
                                      "Arunachal Pradesh",
                                      "Assam",
                                      "Bihar",
                                      "Chhattisgarh",
                                      "Goa",
                                      "Gujarat",
                                      "Haryana",
                                      "Himachal Pradesh",
                                      "Jharkhand",
                                      "Karnataka",
                                      "Kerala",
                                      "Madhya Pradesh",
                                      "Maharashtra",
                                      "Manipur",
                                      "Meghalaya",
                                      "Mizoram",
                                      "Nagaland",
                                      "Odisha",
                                      "Punjab",
                                      "Rajasthan",
                                      "Sikkim",
                                      "Tamil Nadu",
                                      "Telangana",
                                      "Tripura",
                                      "Uttarakhand",
                                      "Uttar Pradesh",
                                      "West Bengal",
                                      "Andaman & Nicobar Islands",
                                      "Dadra and Nagar Haveli and Daman & Diu",
                                      "Jammu & Kashmir",
                                      "Lakshadweep",
                                      "Chandigarh",
                                      "Delhi",
                                      "Ladakh",
                                      "Puducherry"])

        # stateentry = Entry(labelframe5, textvariable=statetk)
        stateentry.place(x=700, y=300)


        nantionalityl = Label(labelframe5, text="Nationality",
                              font="comicsansms 12 bold", bg="#2e3772", fg="white")
        nantionalityl.place(x=100, y=400)

        nantionalityentry = Entry(labelframe5, textvariable=nationalitytk)
        nantionalityentry.place(x=300, y=400)

        maritall = Label(labelframe5, text="Merital Status",
                         font="comicsansms 12 bold", bg="#2e3772", fg="white")
        maritall.place(x=550, y=400)

        global maritalentry
        maritalentry = ttk.Combobox(labelframe5,
                                    values=[
                                        "Single",
                                        "Married",
                                        "Divorced"
                                    ])

        # maritalentry = Entry(labelframe5, textvariable=maritaltk)
        maritalentry.place(x=700, y=400)

        employmentl = Label(labelframe5, text="Employment type",
                            font="comicsansms 12 bold", bg="#2e3772", fg="white")
        employmentl.place(x=100, y=500)

        global employmentlentry
        employmentlentry = ttk.Combobox(labelframe5,
                                        values=[
                                            "Student",
                                            "Private",
                                            "Government",
                                            "Self Employed"])

        # employmentlentry = Entry(labelframe5, textvariable=employmenttk)
        employmentlentry.place(x=300, y=500)

        accounttkl = Label(labelframe5, text="Account Type",
                           font="comicsansms 12 bold", bg="#2e3772", fg="white")
        accounttkl.place(x=550, y=500)

        global accounttkentry
        accounttkentry = ttk.Combobox(labelframe5,
                                      values=["Saving", "Current"])

        # accounttkentry = Entry(labelframe5, textvariable=account_typttk)
        accounttkentry.place(x=700, y=500)

        sbmt5 = Button(labelframe5, text="SUBMIT", fg="white", bg="#2e3772", padx=10,
                       command=lambda: next4(labelframe5, aadhartk.get(), pantk.get(), addresstk.get(), pintk.get(), citytk.get(), accounttkentry.get(), employmentlentry.get(), maritalentry.get(), stateentry.get(), nationalitytk.get()))
        sbmt5.place(x=480, y=575)

        canvas1.create_window(950, 500, window=labelframe5)


def nex2(email, contact, fname, lname, dob, labelframe2):
    global email1
    email1 = email
    global contact1
    contact1 = contact

    global dob1
    dob1 = dob

    global fname1
    fname1 = fname
    global lname1
    lname1 = lname

    email_check = check_data1(email, "email_id", "customer")
    contact_check = check_data1(contact, "contact_no", "customer")

    if email_check and contact_check:
        a = messagebox.askretrycancel(
            "Notification", "Email Id and Contact Number already Exists\n Try With another Email and Contact Number")
        emailtk.set("")
        contacttk.set("")
    elif email_check:
        a = messagebox.askretrycancel("Notification",
                                      "Email Id already Exists\n Try With another Email Id")
        emailtk.set("")
    elif contact_check:
        a = messagebox.askretrycancel("Notification",
                                      "Contact Number already Exists\n Try With Another Contact Number")
        contacttk.set("")
    elif fname == "" or lname == "":
        a = messagebox.askretrycancel("Notification",
                                      "Name can not to be Empty")
    elif fname == " " or lname == " ":
        a = messagebox.askretrycancel("Notification",
                                      "Enter a Valid Name")
    elif email == "" or email == " ":
        a = messagebox.askretrycancel("Notification",
                                      "Email can not be Empty")
    elif contact == "" or contact == " ":
        a = messagebox.askretrycancel("Notification",
                                      "Contact can not be Empty")
    elif len(str(contact)) > 10 or len(str(contact)) < 10:
        a = messagebox.askretrycancel("Notification",
                                      "Enter a valid Contact")
        contacttk.set("")
    elif type(contact) == str:
        a = messagebox.askretrycancel("Notification",
                                      "Enter a valid Contact")
    else:
        # ******************************OTP VERIFY WINDOW********************************
        labelframe2.destroy()
        # ****************************sending OTP****************************************
        otp = randm_num()
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login('sbm.pvt.lmt@gmail.com', 'Hmt@2295')
        server.sendmail('sbm.pvt.lmt@gmail.com', email,
                        f"Welocme To SBM Bank \n Your OTP is {otp}")

# ***********************************************************************************************************
        messagebox.showinfo(
            "Notification", "OTP has been sent to your Mail Id ")

        labelframe4 = LabelFrame(root, text="WELCOME TO SBM BANK", font="comicsansms 20 bold", borderwidth=3,
                                 relief=SUNKEN, bg="#2e3772", fg="white", height=300, width=500)
        labelframe4.pack(fill="both", expand="yes")

        labelotptxt = Label(labelframe4, text="Submit your OTP",
                            font="comicsansms 15 bold", bg="#2e3772", fg="white")
        labelotptxt.place(x=50, y=20)
        global otpinpt
        otpinpt = StringVar()
        labelotpinpttxt = Label(
            labelframe4, text=" OTP", font="comicsansms 11 bold", bg="#2e3772", fg="white")
        labelotpinpttxt.place(x=150, y=90)
        otpentry = Entry(labelframe4, textvariable=otpinpt)
        otpentry.place(x=200, y=90)

        sbmt4 = Button(labelframe4, text="SUBMIT", fg="white", bg="#2e3772", padx=10,
                       command=lambda: next3(otp, otpinpt.get(), labelframe4, fname))
        sbmt4.place(x=225, y=150)

        canvas1.create_window(950, 500, window=labelframe4)

       
def nextqr1(labelframeqr1,userId):
    global user_id
    user_id = userId
    sql = "SELECT custm_id,password FROM user_deta WHERE custm_id= %s"
    val = (userId,)
    mycursor.execute(sql, val)
    myresult = mycursor.fetchone()
    if myresult == None:
        display_invalid_message("User ID")
    else:

        labelframeqr1.destroy()
        
        cap = cv2.VideoCapture(0)
    # initialize the cv2 QRCode detector
        detector = cv2.QRCodeDetector()
        while True:
            _, img = cap.read()
            # cv2.imshow("QRCODEscanner", img)
            data = decode(img)
            
            # data, bbox, _ = detector.detectAndDecode(img)
            if data:
                a=data[0].data.decode("utf-8")
                break  
            cv2.imshow("QRCODEscanner", img)
            if cv2.waitKey(1) == ord("q"):
                break
       
            
        master_key = "server master key"
        server_salt = "server salt"
        server_fernet_key = generate_fernet_key(master_key, server_salt)
        passowrd = decrypt_text(a,server_fernet_key )
        
        cap.release()
        cv2.destroyAllWindows()
        
        if myresult[1]!=passowrd:
            a = messagebox.askretrycancel("Notification",
                                  "Invalid QR code")
        elif myresult[1]==passowrd:
            labelframe7 = LabelFrame(root, text="WELCOME TO SBM BANK", font="comicsansms 20 bold", borderwidth=3,
                                    relief=SUNKEN, bg="#2e3772", fg="white", height=500, width=700)
            labelframe7.pack(fill="both", expand="yes")

            Label(labelframe7, text="Select Your Options", bg="#2e3772", fg="white",
                font="comicsansms 18 bold").place(x=240, y=20)

            s = StringVar(root, "1")

            Radiobutton(labelframe7, text="Check Your Balance", font="comicsansms 11 bold",
                        variable=s, value=1, width=20).place(x=250, y=130)
            Radiobutton(labelframe7, text="Withdrawal", font="comicsansms 11 bold",
                        variable=s, value=2, width=20).place(x=250, y=180)
            Radiobutton(labelframe7, text="Deposit", font="comicsansms 11 bold",
                        variable=s, value=3, width=20).place(x=250, y=250)
            Radiobutton(labelframe7, text="Mini Statement", font="comicsansms 11 bold",
                        variable=s, value=4, width=20).place(x=250, y=300)

            sbmt7 = Button(labelframe7, text="NEXT", fg="white", bg="#2e3772",
                        padx=10, width=8, command=lambda: next7(labelframe7, s.get()))
            sbmt7.place(x=310, y=390)

            canvas1.create_window(950, 500, window=labelframe7)
            
        
        
    
    
    

def nextqr(labelframeqr,opt):
    labelframeqr.destroy()
    if opt=="1":
        loginwindow()
    else:
        labelframeqr1 = LabelFrame(root, text="WELCOME TO SBM BANK", font="comicsansms 20 bold", borderwidth=3,
                                  relief=SUNKEN, bg="#2e3772", fg="white", height=300, width=500)
        labelframeqr1.pack(fill="both", expand="yes")
        global uservalue
        
        user = Label(labelframeqr1, text="Username",
                 font="comicsansms 12 bold", bg="#2e3772", fg="white")
        user.place(x=80, y=80)
        uservalue = StringVar()
        userentry = Entry(labelframeqr1, textvariable=uservalue)
        userentry.place(x=200, y=82)
        sbmt3 = Button(labelframeqr1, text="LOG IN", fg="white", bg="#2e3772", padx=10,
                   command=lambda: nextqr1(labelframeqr1, uservalue.get()))
        sbmt3.place(x=222, y=170)
        
        
        canvas1.create_window(950, 500, window=labelframeqr1)
    

def next1():
    labelframe1.destroy()

    if v.get() == "1":

        # ***********************************register page 1*********************************************
        labelframe2 = LabelFrame(root, text="WELCOME TO SBM BANK", font="comicsansms 20 bold",
                                 borderwidth=3, relief=SUNKEN, bg="#2e3772", fg="white", height=300, width=500)
        labelframe2.pack(fill="both", expand="yes")
        # creating Variable
        global fnametk
        fnametk = StringVar()
        global lnametk
        lnametk = StringVar()
        global dobtk
        dobtk = StringVar()
        global emailtk
        emailtk = StringVar()
        global contacttk
        contacttk = IntVar()

        # Creating Name Label
        fnamel = Label(labelframe2, text="First Name",
                       font="comicsansms 10 bold", bg="#2e3772", fg="white")
        fnamel.place(x=20, y=20)
        fnameentry = Entry(labelframe2, textvariable=fnametk)
        fnameentry.place(x=110, y=20)

        lnamel = Label(labelframe2, text="Last Name",
                       font="comicsansms 10 bold", bg="#2e3772", fg="white")
        lnamel.place(x=250, y=20)
        lnameentry = Entry(labelframe2, textvariable=lnametk)
        lnameentry.place(x=330, y=20)

        dobl = Label(labelframe2, text="DOB(YYYY-MM-DD)",
                     font="comicsansms 10 bold", bg="#2e3772", fg="white")
        dobl.place(x=20, y=70)
        cal = DateEntry(labelframe2, selectmode='day')
        cal.place(x=150, y=70)

        # dobentry = Entry(labelframe2, textvariable=dobtk)
        # dobentry.place( x =150, y = 70)

        contactl = Label(labelframe2, text="CONTACT NO",
                         font="comicsansms 10 bold", bg="#2e3772", fg="white")
        contactl.place(x=20, y=120)
        contactentry = Entry(labelframe2, textvariable=contacttk)
        contactentry.place(x=150, y=120)

        emaill = Label(labelframe2, text="EMAIL ID",
                       font="comicsansms 10 bold", bg="#2e3772", fg="white")
        emaill.place(x=20, y=170)
        emailentry = Entry(labelframe2, textvariable=emailtk)
        emailentry.place(x=150, y=170)

        sbmt2 = Button(labelframe2, text="NEXT", fg="white", bg="#2e3772", padx=10, command=lambda: nex2(
            emailtk.get(), contacttk.get(), fnametk.get(), lnametk.get(), cal.get(), labelframe2))
        sbmt2.place(x=220, y=225)

        canvas1.create_window(950, 500, window=labelframe2)

    else:

        labelframeqr = LabelFrame(root, text="WELCOME TO SBM BANK", font="comicsansms 20 bold", borderwidth=3,
                                  relief=SUNKEN, bg="#2e3772", fg="white", height=300, width=500)
        labelframeqr.pack(fill="both", expand="yes")
        txt_label = Label(labelframeqr, text="Please Select Your Options",
                          bg="#2e3772", fg="white", font="comicsansms 15 bold", pady=20, padx=100)


        txt_label.pack(fill="both", expand="yes")


        opt_qr = StringVar(root, "1")

        Radiobutton(labelframeqr, text="With User id & Password",
                    variable=opt_qr, value=1).pack(side=TOP, pady=20)
        Radiobutton(labelframeqr, text="With QR Code", variable=opt_qr,
                    value=2).pack(side=TOP, pady=10)

        sbmt = Button(labelframeqr, text="NEXT", fg="white",
                    bg="#2e3772", padx=10, command=lambda : nextqr(labelframeqr,opt_qr.get()))
        sbmt.pack(pady=10)

        canvas1.create_window(950, 500, window=labelframeqr)

        


# ************************************main*************************************************************
# Creating label
header = Label(root, text="SBM BANK", font="comicsansms 40 bold",
               bg="#34489f", fg="White")
header.pack()
canvas1.create_window(950, 5, anchor="n", window=header)


# DISPLAY FUNCATION
labelframe1 = LabelFrame(root, text="WELCOME TO SBM BANK", font="comicsansms 20 bold",
                         borderwidth=3, relief=SUNKEN, bg="#2e3772", fg="white")
labelframe1.pack(fill="both", expand="yes")
txt_label = Label(labelframe1, text="Please Select Your Options",
                  bg="#2e3772", fg="white", font="comicsansms 15 bold", pady=20, padx=100)
txt_label.pack(fill="both", expand="yes")


v = StringVar(root, "1")

Radiobutton(labelframe1, text="OPEN ACCOUNT",
            variable=v, value=1).pack(side=TOP, pady=20)
Radiobutton(labelframe1, text="LOG IN", variable=v,
            value=2).pack(side=TOP, pady=10)

sbmt = Button(labelframe1, text="NEXT", fg="white",
              bg="#2e3772", padx=10, command=next1)
sbmt.pack(pady=10)

canvas1.create_window(950, 500, window=labelframe1)

# END LABEL1 FRAME


# ******************************mainend***********************************




root.mainloop()

# **********************SQL************************


# def account_balence():
#     # *********************Finding Account Balence********************
#
#     sql = f"SELECT SUM(ammount) FROM {user_id} WHERE txn_type='Credit'"
#     mycursor.execute(sql)
#     totalCr = mycursor.fetchone()
#     if totalCr[0] == None:
#         totalCr = 0
#     else:
#         totalCr = totalCr[0]
#
#     sql = f"SELECT SUM(ammount) FROM {user_id} WHERE txn_type='Dedit'"
#     mycursor.execute(sql)
#     totalDr = mycursor.fetchone()
#     if totalDr[0] == None:
#         totalDr = 0
#     else:
#         totalDr = totalDr[0]
#     account_bal = totalCr - totalDr
#
#     sql = "UPDATE accounnt_data SET account_bal = %s WHERE custm_id = %s"
#     val = (account_bal, user_id)
#
#     mycursor.execute(sql, val)
#     mydb.commit()
#
#     return account_bal


# *****************************Checking a data in database******************************
# def check_data1(data, column1, tables):
#     sql = f"SELECT {column1} FROM {tables}"
#     mycursor.execute(sql)
#     myresult = mycursor.fetchall()
#     for x in myresult:
#         if x[0] == data:
#             return True
#     return False
#
#
# # ******************************table Empty or not**********************
# def empty(tables):
#     sql = f"SELECT COUNT(*) FROM {tables}"
#     mycursor.execute(sql)
#     myresult = mycursor.fetchone()
#     if myresult[0] == 0:
#         return True
#     else:
#         return False
#
#
# # ***********************************random Number(OTP)********************
# def randm_num():
#     list1 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
#
#     rndm_num = ""
#     while len(rndm_num) != 6:
#         rndm_num = rndm_num + str(random.choice(list1)) + random.choice(string.ascii_letters)
#     return rndm_num
#
#
# # ********************************Gen. Custm_id*******************************
# def custm_id1():
#     list1 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
#
#     custm_id = ""
#     while len(custm_id) != 8:
#         custm_id = custm_id + str(random.choice(list1)) + random.choice(string.ascii_letters)
#
#     empt = empty("customer")
#     if empt:
#         return custm_id
#     else:
#         check_data = check_data1(custm_id, "custm_id", "customer")
#
#         if check_data:
#             custm_id1()
#         else:
#             return custm_id
#     # ***************Gen. password******************
#
#
# def gen_pass():
#     list3 = ['#', '@', '&', '$']
#     list2 = [str(random.choice(list3)), random.choice(string.ascii_letters), random.randint(1, 9)]
#     list4 = [random.choice(string.ascii_letters), random.randint(1, 9), str(random.choice(list3))]
#     password = ""
#     while len(password) != 8:
#         password = password + str(random.choice(list2)) + str(random.choice(list4))
#     empt = empty("user_deta")
#     if empt:
#         return password
#     else:
#         check_data = check_data1(password, "password", "user_deta")
#         if check_data:
#             gen_pass()
#         else:
#             return password
#
#
# # *********************Gen account_no************************
# def gen_ac():
#     account_no = "7412"
#     while len(account_no) != 12:
#         account_no = account_no + str(random.randint(1, 9))
#     empt = empty("accounnt_data")
#     if empt:
#         return account_no
#     else:
#         check_data = check_data1(account_no, "account_no", "accounnt_data")
#         if check_data:
#             gen_ac()
#         else:
#             return account_no
#
#
# # *****************************input email_id*******************************
# def email_inpt():
#     email_id = input("Enter Your Email Id>>> ")
#     if empty("customer"):
#         return email_id
#     else:
#         check_data = check_data1(email_id, "email_id", "customer")
#         if check_data:
#             print("Email Already Exits \n Enter another Email>>>")
#             email_inpt()
#         else:
#             return email_id
#
#
# # *****************************input data*******************************
# def data_inpt(data, column1, tables, data_type):
#     inpt_data = data_type(input(f"Enter Your {data}>>> "))
#     if empty("customer"):
#         return inpt_data
#     elif (str(inpt_data) == "" or str(inpt_data) == " "):
#         print("Enter a Valid Data")
#         data_inpt(data, column1, tables, data_type)
#
#     else:
#         check_data = check_data1(inpt_data, column1, tables)
#         if check_data:
#             print(f"{data} Already Exits \n Enter another {data}>>>")
#             data_inpt(data, column1, tables, data_type)
#         else:
#             return inpt_data
#
#
# count1 = 0
#
#
# def display():
#     print(
#         "***************************WELCOME TO SBI******************\n*******************PLEASE SELECT YOUR OPTIONS*************************")
#     global count1
#
#     def recur():
#         global count1
#         count1 = count1 + 1
#         if (count1 == 4):
#             print("You tryed enough \n Have a Nice day")
#             exit()
#         print("*********************************\n 1.Open Account\n 2.Log In\n**********************************")
#         opt = int(input("Enter your options>>>> "))
#         if (opt == 1):
#             register()
#         elif (opt == 2):
#             log_in()
#         else:
#             print("Opps You entered a wrong input \n Try Again")
#             recur()
#
#     recur()
#
#
# def register():
#     fi_name = input("Enter Your First Name>>> ")
#     la_name = input("Enter Your Last Name>>> ")
#     dob = input("Enter Your Date Of Birth Format(date/month/year)>>>")
#     email_id = data_inpt("Email Id", "email_id", "customer", str)
#
#     # *******************Sending OTP On email***********************
#     otp = randm_num()
#     server = smtplib.SMTP('smtp.gmail.com', 587)
#     server.starttls()
#     server.login('sbm.pvt.lmt@gmail.com', 'Hmt@2295')
#     server.sendmail('sbm.pvt.lmt@gmail.com', email_id, f"Welocme To SBM Bank \n Your OTP is{otp}")
#     print("Loding.........")
#     inpt_otp = input("Enter Your OTP>>>>>")
#
#     if otp == inpt_otp:
#
#         contact = data_inpt("Contact No", "contact_no", "customer", int)
#
#         pan = data_inpt("Pan No", "pancard_no", "customer", str)
#
#         Adhhar_no = data_inpt("Aadhar No", "aadhar_no", "customer", int)
#         pincode_no = int(input("Enter Your Pincode NO.>>>>"))
#         address = input("Enter your address>>>>")
#         city = input("Enter Your city>>>")
#         state = input("Enter your State>>>")
#         nationality = input("Enter Your Nationality>>>")
#         marital_status = input("Enter Your Marital Statu>>")
#         employment_tp = input("Enter your employment type>>")
#         account_type = input("Enter acount type Saving / Cuurent>>>")
#
#         custm_id = custm_id1()
#         sql = "INSERT INTO customer(custm_id,f_name,l_name,dob,address,pincode,city,state,nationality,aadhar_no,pancard_no,marital_status,employment_type,email_id,contact_no) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
#         val = [(custm_id, fi_name, la_name, dob, address,
#                 pincode_no, city, state, nationality, Adhhar_no,
#                 pan, marital_status, employment_tp, email_id, contact)]
#         mycursor.executemany(sql, val)
#         # mydb.commit()
#         password = gen_pass()
#
#         sql = "INSERT INTO user_deta(custm_id,password) VALUES (%s,%s)"
#         val = (custm_id, password)
#         mycursor.execute(sql, val)
#         # mydb.commit()
#         account_no = gen_ac()
#
#         sql = "INSERT INTO accounnt_data(custm_id,account_no,account_type) VALUES (%s,%s,%s)"
#         val = (custm_id, int(account_no), account_type)
#         mycursor.execute(sql, val)
#         mydb.commit()
#
#         # ***********************TXN Data*************************
#         mycursor.execute(
#             f"CREATE TABLE {custm_id} (sl_no INT AUTO_INCREMENT PRIMARY KEY,txn_date DATETIME,ammount BIGINT, txn_type VARCHAR(255))")
#
#         # *********************Sending Mail********************
#         server = smtplib.SMTP('smtp.gmail.com', 587)
#         server.starttls()
#         server.login('sbm.pvt.lmt@gmail.com', 'Hmt@2295')
#         server.sendmail('sbm.pvt.lmt@gmail.com', email_id,
#                         f'Welcome To SBM Bank \n Your Account is has been Successfully Opened\n Your Account Number is- {account_no}\n User Id- {custm_id}\n password- {password}')
#
#         print("Loding.......")
#         print(
#             f"Your Account is Open Successfully\n your Account No. is :{account_no}\n  User Id and password has been sent on your Mail")
#
#         print("Do You Want To log in Yes/No")
#         opt = input("")
#         if (opt.lower() == "yes"):
#             log_in()
#         else:
#             print("*********THANK YOU*************\n HAVE A NICE DAY*****************")
#
#
#     else:
#         print("Invalid Otp Try Again")
#
#
# def log_in():
#     global user_id
#     global count2
#     count2 = 0
#
#     def user_pswd():
#         global user_id
#         global count2
#         user_id = input("Enter Your User_id : ")
#         password = input("Enter Your Password: ")
#         sql = "SELECT custm_id,password FROM user_deta WHERE custm_id= %s"
#         val = (user_id,)
#         mycursor.execute(sql, val)
#         myresult = mycursor.fetchone()
#
#         if myresult == None:
#             while count2 < 2:
#                 print("<<<<<Enter valid User id >>>")
#                 count2 = count2 + 1
#                 user_pswd()
#             print("*********You Have Tried Enough***********")
#
#         elif (myresult[1] != password):
#             while count2 < 2:
#                 print("<<<<<<<<Enter valid Password >>>>>>>")
#                 count2 = count2 + 1
#                 user_pswd()
#             print("**************You have tried enough*********")
#
#         elif (myresult[0] == user_id and myresult[1] == password):
#             print("1.Check Your Balance \n 2.Withdrawal \n 3.Deposit \n 4.Mini Statement ")
#             opt = int(input("Select your options>>>"))
#             if (opt == 1):
#                 Show_blance()
#
#             elif (opt == 2):
#                 debit()
#             elif (opt == 3):
#                 credit()
#             elif (opt == 4):
#                 mini_statement()
#
#     user_pswd()
#
#
# def debit():
#     amnt = int(input("Enter Your Ammount : >>>"))
#     account_bal = account_balence()
#
#     if (amnt > account_bal):
#         print("Insufficient Balance")
#     else:
#         sql = f"INSERT INTO {user_id} (txn_date,ammount,txn_type) VALUES(NOW(),{amnt},'Dedit')"
#         mycursor.execute(sql)
#         mydb.commit()
#
#     account_bal = account_balence()
#
#     print("Your Account Balence : ", account_bal)
#
#
# # *************************Credit*******************************
# def credit():
#     amnt = int(input("Enter Your Ammount"))
#     sql = f"INSERT INTO {user_id} (txn_date,ammount,txn_type) VALUES(NOW(),{amnt},'Credit')"
#     mycursor.execute(sql)
#     mydb.commit()
#     account_bal = account_balence()
#     print(account_bal)
#
#
# # ****************************Check Balence*************************
# def Show_blance():
#     account_bal = account_balence()
#
#     print("Your Account Balence : ", account_bal)
#     opt = input("Do You want to Exit(y/n)")
#     if opt == "y":
#         exit()
#     else:
#         print("1.Withdrawal \n 2.Deposit \n 3.Mini Statement")
#         opt = int(input("select your options >>>"))
#         if opt == 1:
#             debit()
#         elif opt == 2:
#             credit()
#         elif opt == 3:
#             mini_statement()
#
#
# def mini_statement():
#     sql = f"SELECT * FROM {user_id} LIMIT 5"
#     mycursor.execute(sql)
#     myresult = mycursor.fetchall()
#     for x in myresult:
#         print(x)

