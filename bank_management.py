import json
import random
import string
from pathlib import Path 

class Bank:
    database = 'data.json'
    data = []

    try:
        if Path(database).exists():
            with open(database) as fs:
                data = json.loads(fs.read()) # Load the data
        
        else:
            print("No such File exists")

    except Exception as e :
        print(f"An Error occured as {e}")

    @staticmethod
    def __update():
        with open(Bank.database, 'w') as fs:
            fs.write(json.dumps(Bank.data))

    @classmethod
    def __AccountGenerate(cls):
        alpha = random.choices(string.ascii_letters, k=3)
        num = random.choices(string.digits, k =3)
        spchar = random.choices("!@#$%^&*", k =1)
        id = alpha + num + spchar
        random.shuffle(id)
        return "".join(id)
        

    def CreateAccount(self):
        info = {
            "name" : input("Enter Your Name:"),
            "age" : int(input("Enter Your Age: ")),
            "email" : input("Enter Your Email: "),
            "pin" : int(input("Enter Your 4-Digit Pin: ")),
            "AccountNo" : Bank.__AccountGenerate,
            "balance" : 0
        }

        if (info["age"]<18 ):
            print("Sorry you cannot create your account")

        elif (len(str(info["pin"])) != 4):
            print("Invalid Pin Try again")

        else:
            print("Account has been created Successfully")
            for i in info:
                print(f"{i} : {info[i]}")
            print(f"Please note down your Account Number")


            Bank.data.append(info)
            Bank.__update()


    def DepositMoney(self):
        accNo = input("Please tell me your Account Number: ") 
        pin = int(input("Please Enter Your Pin : "))

        userdata = [i for i in Bank.data if i['AccountNo'] == accNo and i['pin'] == pin]
        if userdata == False:
            print("Sorry , No Data Found")

        else:
            amount = int(input("How Much do you want to Deposit: "))
            if (amount > 10000 ):
                print("Please Deposit Below 10,000")

            elif (amount < 0):
                print("Enter Valid Amount")

            else :
                userdata[0]['balance'] += amount
                Bank.__update()
                print("Amount Deposited Sucessusfully")

    def withdrawMoney():
        accNo = input("Please tell me your Account Number: ") 
        pin = int(input("Please Enter Your Pin : "))

        userdata = [i for i in Bank.data if i['AccountNo'] == accNo and i['pin'] == pin]
        if userdata == False:
            print("Sorry , No Data Found")

        else:
            amount = int(input("How Much do you want to Withdraw: "))
            if (userdata[0]['balance'] < amount):
                print("Sorry , Insufficient Balance")

            else :
                userdata[0]['balance'] -= amount
                Bank.__update()
                print("Amount Withdrew Sucessusfully")


    def showDetails(self):
        accNo = input("Please tell me your Account Number: ") 
        pin = int(input("Please Enter Your Pin : "))

        userdata = [i for i in Bank.data if i['AccountNo'] == accNo and i['pin'] == pin]
        print("Your Informaion \n\n")
        for i in userdata[0]:
            print(f"{i} : {userdata[0][i]}")
        
    def UpdateDetails(self):
        accNo = input("Please tell me your Account Number: ") 
        pin = int(input("Please Enter Your Pin : "))
        userdata = [i for i in Bank.data if i['AccountNo'] == accNo and i['pin'] == pin]

        if userdata == False :
            print("No Such user found")

        else :
            print("You cannot change the age , account Number and Balance")

            print("Fill the details for change or leave it empty for no change")

            newdata = {
                "name" : input("Please tell new Name or press Enter to skip: "),
                "email" : input("Please enter your new E-mail or press enter to Skip: "),
                "pin" : input("Enter New Pin or press enter to skip: ")
            }

            if newdata["name"] == "":
                newdata["name"] = userdata[0]['name']
                
            if newdata["email"] == "":
                newdata["email"] = userdata[0]['email']
                
            if newdata["pin"] == "":
                newdata["pin"] = userdata[0]['pin']
                
            newdata['age'] = userdata[0]['age']
            newdata['AccountNo'] = userdata[0]['AccountNo']
            newdata['balance'] = userdata[0]['balance']

            if type(newdata['pin']) == str:
                newdata['pin'] = int(newdata['pin'])

            for i in newdata:
                if newdata[i] == userdata[0][i]:
                    continue
                else:
                    userdata[0][i] = newdata[i]
            Bank.__update()
            print("Details Updated Successfully")

    def DeleteAccount():
        accNo = input("Please tell me your Account Number: ") 
        pin = int(input("Please Enter Your Pin : "))

        userdata = [i for i in Bank.data if i['AccountNo'] == accNo and i['pin'] == pin]

        if userdata == False:
             print("No Such user found")

        else:
            check = input("Press (Y) if you want to delete the account else press (N): ")

            if check == "N" or check =='n':
                print("Bypassed")

            else:
                index = Bank.data.index(userdata[0])
                Bank.data.pop(index)
                print("Account Deleted Successfully")
                Bank.__update()

user = Bank()
print("Press 1 for Creating and Account")
print("Press 2 for Depositing the Money in the Bank")
print("Press 3 for Withdrawing the Money")
print("Press 4 for Details")
print("Press 5 for Updating the Details")
print("Press 6 for Deleting your Account")

check = int(input("Tell Your Response :-"))

if check == 1:
    user.CreateAccount()
    
if check == 2:
    user.DepositMoney()

if check == 3:
    user.withdrawMoney()

if check == 4:
    user.showDetails()

if check == 5:
    user.UpdateDetails()

if check == 6:
    user.DeleteAccount()