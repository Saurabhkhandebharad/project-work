import mysql.connector as m
depdatabase = m.connect(host = 'localhost', user ='root',password = 'saurabh',database = 'bank2')# ,database = 'bank3'
cursor=depdatabase.cursor()
# cursor.execute("create database bank2")   #execute just once while creating database
# cursor.execute("create table acc(accno int primary key auto_increment,accname varchar(20),balance float )")#execute just once while creating table
### cursor.execute("alter table acc auto_increment=1000;") 
# while giving input of first customer, one must start with the value in mind and auto_increment
# will add other values on its own for ex, you put in 1000 as acc.no for first customer, then,
# program will automatically select 1001 as next value


def create_acc():
    query = "insert into acc(accname, balance) values(%s,%s)"
    while True:
        accname = input("enter account holder's name: ")
        balance = input("enter balance: ")
        try:
            float(balance)
        except ValueError:
            print("Invalid input for balance. Please enter a number.")
            continue
        cursor = depdatabase.cursor()
        cursor.execute(query, [accname, balance])
        print("customer's account has been created.")
        depdatabase.commit()
        ans = input("Do you wish to continue? (y/n): ")
        if(ans == "n"):
            passbook()

def statement():
    query = "select * from acc"
    # acc_name = input("enter customer's account name: ") 
    cursor = depdatabase.cursor()
    cursor.execute(query)
    result=cursor.fetchall()     
    for record in result:
        print(record)
    end() 
    
def check_balance():
    query = "select accname, balance from acc where accno=%s"
    try:
        acc_no = int(input("enter customer's account number: "))
        cursor = depdatabase.cursor()
        cursor.execute(query, [acc_no])
        result = cursor.fetchall()
        if len(result) == 0:
            print("Account number not found.")
        else:
            for record in result:
                print("customer's total balance is: ", record)
    except ValueError:
        print("Invalid account number.")
    end()
        
def make_deposit():
    query = "update acc set balance = balance+%s where accno = %s"
    acc_no = int(input("enter customer's account number: "))
    amount = input("enter the amount: ")
    try:
        amount = float(amount)
        if amount < 0:
            print("Invalid amount.")
            make_deposit()
        else:
            cursor = depdatabase.cursor()
            cursor.execute(query, [amount, acc_no])
            depdatabase.commit()
            end()
    except ValueError:
        print("Invalid amount.")
        make_deposit()
    except m.Error as error:
        print("Error writing data to MySQL table", error)
        end()
    
def withdraw():
    val = "select balance from acc where accno=%s"
    acc_no = int(input("enter customer's account number: "))
    paisado=int(input("enter money: "))
    cursor = depdatabase.cursor()
    cursor.execute(val,(acc_no,))
    result = cursor.fetchall()
    a = result[0][0]
    b=a-paisado
    if b < 0:
        print("insufficient balance")
    else:
        query = "update acc set balance = balance-%s where accno = %s"
        # acc_no = int(input("enter customer's account number: "))
        # amount = input("enter the amount: ")
        cursor = depdatabase.cursor()
        cursor.execute(query, [paisado, acc_no])
        depdatabase.commit() 
    # check_balance()
    end()    
# withdraw()

def drop():
    query1 = "delete from acc where accno =%s"
    # query2 = set @accno = 0;UPDATE your_table SET id = @num := (@num+1);ALTER TABLE tableName AUTO_INCREMENT = 1;
    acc_no = int(input("enter customer's account number: "))
    cursor = depdatabase.cursor()
    cursor.execute(query1, [acc_no])
    depdatabase.commit() 
    # check_balance()
    end()   
    
def search_by_name():
    query = "select * from acc where accname like %s"
    acc_name = input("enter customer's account name: ") 
    cursor = depdatabase.cursor()
    cursor.execute(query, [acc_name])
    result=cursor.fetchall()       
    if len(result) == 0:
        print("No results found.")
    else:
        print("Customer/Customers is/are: ")
        for record in result:
            print(record)
    end()    

def end():
    bye = input('do you wish to continue?(y/n): ')
    if bye == 'y':
        passbook()
    else:
        print("transaction has ended.")
        exit()
# exit()

def passbook():
    print("*** BANK MANAGEMENT SYSTEM ***")
    ans = input("what would you like to do?\n1 -Create account\n2 -Check balance\n3 -Deposit an amount\n4 -Withdraw an amount\n5 -drop an account\n6 -statement\n7 -Search by Name: ")
    if(ans=="1"):
        create_acc()
    elif(ans=='2'):
        check_balance()
    elif(ans=='3'):
        make_deposit()
    elif(ans=='4'):
        withdraw()
    elif(ans=='5'):
        drop()
    elif(ans == '6'):
        statement()
    elif(ans == '7'):
        search_by_name()
    else:
        exit()
passbook()        
