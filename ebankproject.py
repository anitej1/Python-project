import mysql.connector as sqltor
import random

#function to check python Mysql connection
def connectioncheck():
    print()
    print(" "*30, "Welcome to E-BANK Site")
    print()
    while True:
        username=input("Enter database username:")
        password=input("Enter database password:")
        db=sqltor.connect(host="localhost", user=username, passwd=password, db="bank")
        cur=db.cursor()
        if db.is_connected():
            print()
            print("Congratulations, your MySQL connection is succesfull!")
            print()
            return username, password
            break
        else:
            print()
            print("Database username/password not correct. Please try again")
            print()
#function to create table
def createtable():
    db=sqltor.connect(host="localhost", user=userr, passwd=pas, db="bank")
    cur=db.cursor()
    st='''create table if not exists accounts(ID varchar(5), Name varchar(20), Password varchar(20),
Balance int, Loan_amt varchar(15) default 'NULL',Deposit_amt varchar(15) default 'NULL',
LInterest varchar(4) default 'NULL', DInterest varchar(4) default 'NULL');'''  #Loan_amt is the principal amount
    cur.execute(st)

#admin menu function
def admin():
    print()
    db=sqltor.connect(host="localhost", user=userr, passwd=pas, db="bank")
    cur=db.cursor()
    print("Login as administrator succesfull.")
    print()
    while True:
        print()
        print("*"*33, end=" ")
        print("Administrator MENU", end=" ")
        print("*"*32)   
        print("*"," "*81,"*")
        print("*"," "*27,"1. Display all accounts"," "*29,"*")
        print("*"," "*27,"2. Check number of E-Bank accounts"," "*18,"*")
        print("*"," "*27,"3. Delete  an account"," "*31,"*")
        print("*"," "*27,"4. Change admin password"," "*28,"*")
        print("*"," "*27,"5. Return to login menu"," "*29,"*")
        print("*"," "*81,"*")
        print("*"*85)
        n=int(input("Enter your choice from 1 to 5:"))
        print()
        if n==1:
            cur.execute("select * from accounts;")
            data=cur.fetchall()
            for i in range(len(data)):
                print("Account", (i+1))     
                print("ID-", data[i][0])
                print("Name-", data[i][1])
                print("Password-", data[i][2])
                print("Balance-", data[i][3])
                print("Loan_amount-", data[i][4])
                print("Deposit_amount-", data[i][5])                    
                print("Loan Interest rate(%)-", data[i][6])
                print("Deposit Interest rate(%)-", data[i][7])
                print()
        elif n==2:
            cur.execute("select count(*) from accounts;")
            data=cur.fetchall()
            print("Number of E-Bank accounts:", data[0][0])
        elif n==3:
            delete()
        elif n==4:
            new=input("Enter new password:")
            adminpas[0]=new
        elif n==5:
            login()
        else:
            print("Please enter a valid choice(1-8):")
    
#function to create table
def createacc():
    db=sqltor.connect(host="localhost", user=userr, passwd=pas, db="bank")
    cur=db.cursor()
    print("*"*30, "Create Account Menu", "*"*29) 
    a=input("Enter new acc ID (5 charecters all integers):")
    b=input("Enter new acc Name (max charecters=20):")
    c=input("Create new password (max charecters=20):")
    d=int(input("Enter bank account balance as verified offline(max charecters=11):"))
    values=(a,b,c,d)
    sql="INSERT INTO accounts(ID, Name, Password, Balance) VALUES(%s, %s, %s, %s)"
    cur.execute(sql ,values)
    cur.execute("COMMIT")
    cur.close()
    print("New account created succesfully")
    print()

#login menu function
def login():
    while True:
        print()
        print("*"*37, end=" ")
        print("Login MENU", end=" ")
        print("*"*35, end="\n")
        print()
        print("1. Login")
        print("2. Exit")
        n=int(input("Enter choice(1/2):"))
        if n==1:
            a=input("Enter ID for login :")
            b=input("Enter password for login:")
            if a=="admin" and b==adminpas[0]:
                admin()
            db=sqltor.connect(host="localhost", user=userr, passwd=pas, db="bank")
            cur=db.cursor()
            cur.execute("select * from accounts;")
            data=cur.fetchall()
            ex=0
            for i in data:
                if a in i:
                    if b in i:
                        print("Login succesfull!")
                        if menu(a,b)=="ex":
                            break
                    else:
                        print("Wrong password/ID. Please try again.")
    
        elif n==2:
            break

#function to display all accounts
def display(x,y):
    db=sqltor.connect(host="localhost", user=userr, passwd=pas, db="bank")
    cur=db.cursor()
    cur.execute("select * from accounts;")
    data=cur.fetchall()
    print("Account details:")
    print()
    for i in data:
        if x and y in i:
            print("ID:", i[0])
            print("Name:", i[1])
            print("Balance:", i[3])
            print("Loan principal amount(if applicable):", i[4])
            print("Deposit principal amount(if applicable):", i[5])
            print("Loan interest rate(if applicable)(%):", i[6])
            print("Deposite interest rate(if applicable)(%):", i[7])
            
#transfer funds functions            
def transfer(x,y):
    print()
    print("Accounts to which you can transfer:")
    db=sqltor.connect(host="localhost", user=userr, passwd=pas, db="bank")
    cur=db.cursor()
    st="select Name, ID from accounts WHERE NOT ID=%s AND NOT Password=%s;"
    values=(x, y)
    cur.execute(st, values)  #only show other accounts not user's own account
    data=cur.fetchall()
    print(data)
    for i in range(len(data)):
        print("Account", (i+1))     
        print("ID-", data[i][0])
        print("Name-", data[i][1])
    cur.close()
    ID=input("Enter ID of recipient:")
    amt=int(input("Enter amount you wish to transfer:"))
    cur=db.cursor()
    cur.execute("select * from accounts;")
    data=cur.fetchall()
    print()
    for i in data:
        if x in i and y in i:
            print("Current balance in your account:", i[3])
            r=list(i)
            new_bal=int(r[3])-amt
            print("Your new balance:", new_bal)
            st1="UPDATE accounts SET balance=%s WHERE ID=%s;"
            values=(new_bal, x)
            cur.execute(st1, values)  #deducting balance from user account
            db.commit()
    for i in data:
        if ID in i:
            l=list(i)
            bal=int(r[3])+amt
            print("Recipients new balance:", bal)
            st2="UPDATE accounts SET balance=%s WHERE ID=%s;"
            values1=(bal, ID)
            cur.execute(st2, values1)  #adding balance to recipient account
            db.commit()
            cur.close()

#retrieve balance function            
def retrieve(x,y):
    db=sqltor.connect(host="localhost", user=userr, passwd=pas, db="bank")
    cur=db.cursor()
    cur.execute("select * from accounts;")
    data=cur.fetchall()
    for i in data:
        if x in i and y in i:
                print("Current balance:", i[3])
                n=int(input("Enter amount you want to retrieve:"))
                r=list(i)
                new_bal=int(r[3])-n
                print("New Balance:", new_bal)
                st1="UPDATE accounts SET Balance=%s WHERE ID=%s;"
                values=(new_bal, x)
                cur.execute(st1, values)  #updating account with new balance
                db.commit()
                cur.close()
                print()

#delete account function
def delete():
    print()
    a=input("Enter account ID to delete :")
    b=input("Enter account password:")
    db=sqltor.connect(host="localhost", user=userr, passwd=pas, db="bank")
    cur=db.cursor()
    cur.execute("select * from accounts;")
    data=cur.fetchall()
    for i in data:
        if a in i:
            if b in i:
                print("Account found !Now deleting:")
                st="delete from accounts where ID=%s and Password=%s;"
                values=(a, b)
                cur.execute(st, values)
                db.commit()
                cur.close()
                print("Account deleted")
                break
            else:
                print("Wrong password. Please try again.")
        else:
            print("No such ID exists. Please try again.")
            print()

#main menu function
def menu(x,y):
    while True:
        print()
        print("*"*33, end=" ")
        print("E-Bank Site MENU", end=" ")
        print("*"*34, end="\n")
        print("*"," "*81,"*")
        print("*", " "* 25,"Logged in ID:", x, " "*35,"*")
        print("*"," "*81,"*")
        print("*", " "* 25,"Choose 1 to display account details"," "*19,"*")
        print("*", " "* 25,"Choose 2 to transfer funds to another account"," "*9,"*")
        print("*", " "* 25,"Choose 3 to retrieve amount"," "*27,"*")
        print("*", " "* 25,"Choose 4 for loan application", " "*25,"*")
        print("*", " "* 25,"Choose 5 for fixed deposit application"," "*16,"*")
        print("*", " "* 25,"Choose 6 to create new account"," "*24,"*")
        print("*", " "* 25,"Choose 7 to participate in lottery"," "*20,"*")
        print("*", " "* 25,"Choose 8 for help", " "*37,"*")
        print("*", " "* 25,"Choose 9 to logout(You will be returned to login menu)","","*")
        print("*", " "*25,"Choose 10 to exit software"," "*28,"*")
        print("*"," "*81,"*")
        print("*"*85, end="\n")
        n=int(input("Enter a choice from 1-10 :"))
        if n==1:
            display(x,y)
        elif n==2:
            transfer(x,y)
        elif n==3:
            retrieve(x,y)
        elif n==4:
            loan(x,y)
        elif n==5:
            fd(x,y)
        elif n==6:
            createacc()
        elif n==7:
            lottery(x,y)
        elif n==8:
            print('''Please visit our main bank site help page where documentation
of this ebanking software can be read or you can contact customer care''')
        elif n==9:
            return "ex"
            break
        elif n==10:
            exit()
        else:
            print("Please enter a valid choice(1-10):")

def buy_ticket(x,y):
    db=sqltor.connect(host="localhost", user=userr, passwd=pas, db="bank")
    cur=db.cursor()
    cur.execute("select * from accounts;")
    data=cur.fetchall()
    for i in data:
        if x and y in i:
                r=list(i)
                new_bal= int(r[3])-100  #ticketprice=50
                st='UPDATE accounts SET Balance=%s WHERE ID=%s;'
                values=(new_bal, x)
                cur.execute(st, values)
                cur.execute("COMMIT")
                cur.close()

def prize_win(x,y):
    print()
    print("Congratulations! You have won the lottery! ")
    print("5000 rupees will be credited to you bank balance")
    db=sqltor.connect(host="localhost", user=userr, passwd=pas, db="bank")
    cur=db.cursor()
    cur.execute("select * from accounts;")
    data=cur.fetchall()
    for i in data:
        if x and y in i:
                new_bal= (int(list(i)[3])+5000) #prize=5000
                st='UPDATE accounts set Balance= %s WHERE ID=%s;'
                values=(new_bal, x)
                cur.execute(st, values)
                cur.execute("COMMIT")
                cur.close()
                print()

#lottery game function
def lottery(x,y):
    print()
    print("*"*28, "Lottery Game", "*"*28) 
    print()
    print("Fee for entering lottery is 50 rupees")
    lotto_play= input("Would you like to play lottery? Press Y for yes and N to return to menu:")
    if lotto_play in 'Yy':
        db=sqltor.connect(host="localhost", user=userr, passwd=pas, db="bank")
        cur=db.cursor()
        cur.execute("select * from accounts;")
        data=cur.fetchall()
        for i in data:
            if x and y in i:
                    buy_ticket(x,y)
                    p=random.randint(1,20)
                    q=random.randint(1,20)
                    if p is q:
                        prize_win(x,y)
                    else:
                        print("Sorry, you didn't win the prize. Better luck next time")
                        print("Ticket number=", p)
                        print("Lottery number=", q)
                        print()

#loan function
def loan(x,y):
    print()
    print("Thank you for applying for loan.")
    print("Please choose your plan:")
    print()
    print("1. 2 Year Loan, Interest=8%")
    print("2. 5 Year Loan, Interest=12%")
    print("3. 10 Year Loan, Interest=16%")
    n=int(input("Enter choice from 1 to 3:"))
    p=int(input("Enter principal amount for loan:"))
    if n==1:
        A=p*(1+0.08)**2
        print("Final amount payable after time period elapsed:", A)
        print("Calculated compound interest:", A-p)
        chk=input("Are you sure you want to apply for loan? Enter Y for yes and N to return to menu:")
        if chk=="Y":
            loanapp(x,y,p,8)
    if n==2:
        A=p*(1+0.12)**5
        print("Final amount payable after time period elapsed:", A)
        print("Calculated compound interest:", A-p)
        chk=input("Are you sure you want to apply for loan? Enter Y for yes and N to return to menu:")
        if chk=="Y":
            loanapp(x,y,p,12)
    if n==3:
        A=p*(1+0.16)**10
        print("Final amount payable after time period elapsed:", A)
        print("Calculated compound interest:", A-p)
        chk=input("Are you sure you want to apply for loan? Enter Y for yes and N to return to menu:")
        if chk=="Y":
            loanapp(x,y,p,16)
#loan app
def loanapp(x,y,p,q):
    db=sqltor.connect(host="localhost", user=userr, passwd=pas, db="bank")
    cur=db.cursor()
    cur.execute("select * from accounts;")
    data=cur.fetchall()
    for i in data:
        if x and y in i:
                print("Current balance:", i[3])
                print("Adding loan amount:", p, "from bank balance")
                r=list(i)
                new_bal=int(r[3])+p
                st1="UPDATE accounts SET Balance=%s, Loan_amt=%s, LInterest=%s WHERE ID=%s;"
                values=(new_bal, p, q, x)
                cur.execute(st1, values)  #updating account with new balance
                db.commit()
                cur.close()
                print()
#deposit function
def fd(x,y):
    print()
    print("Thank you for applying for fixed deposit.")
    print("Please choose your plan:")
    print()
    print("1. 2 Year FD, Interest=5%")
    print("2. 5 Year FD, Interest=10%")
    print("3. 10 Year FD, Interest=12%")
    n=int(input("Enter choice from 1 to 3:"))
    p=int(input("Enter principal amount for loan:"))
    if n==1:
        A=p*(1+0.05)**2
        print("Final amount deducted after time period elapsed:", A)
        print("Calculated compound interest:", A-p)
        chk=input("Are you sure you want to apply for loan? Enter Y for yes and N to return to menu:")
        if chk=="Y":
            fdapp(x,y,p,5)
    if n==2:
        A=p*(1+0.10)**5
        print("Final amount deducted after time period elapsed:", A)
        print("Calculated compound interest:", A-p)
        chk=input("Are you sure you want to apply for loan? Enter Y for yes and N to return to menu:")
        if chk=="Y":
            fdapp(x,y,p,10)
    if n==3:
        A=p*(1+0.12)**10
        print("Final amount deducted after time period elapsed:", A)
        print("Calculated compound interest:", A-p)
        chk=input("Are you sure you want to apply for loan? Enter Y for yes and N to return to menu:")
        if chk=="Y":
            fdapp(x,y,p,12)

def fdapp(x,y,p,q):
    db=sqltor.connect(host="localhost", user=userr, passwd=pas, db="bank")
    cur=db.cursor()
    cur.execute("select * from accounts;")
    data=cur.fetchall()
    for i in data:
        if x and y in i:
                print("Current balance:", i[3])
                print("Deducting FD amount:", p, " from bank balance")
                r=list(i)
                new_bal=int(r[3])-p
                st1="UPDATE accounts SET Balance=%s, Deposit_amt=%s, DInterest=%s WHERE ID=%s;"
                values=(new_bal, p, q, x)
                cur.execute(st1, values)  #updating account with new balance
                db.commit()
                cur.close()
                print()
    
    
    
print("*"*34, "E-Bank Software", "*"*33)  #85

adminpas=["adminbanke2356"] #admin password
L=list(connectioncheck())
userr=L[0]  #intializing database password and username
pas=L[1]

createtable()
db=sqltor.connect(host="localhost", user=userr, passwd=pas, db="bank")
cur=db.cursor()
cur.execute("select * from accounts;")
data=cur.fetchall()

if data==[]:
    createacc()   #if accounts exist then user is prompted to login otherwise create account
    
    login()
else:
    login()

        
                
                
                
    
    
    
    
    


    
