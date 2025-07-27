import streamlit as st
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
                data = json.loads(fs.read())  # Load the data
        else:
            print("No such File exists")
    except Exception as e:
        print(f"An Error occurred as {e}")

    @staticmethod
    def __update():
        with open(Bank.database, 'w') as fs:
            fs.write(json.dumps(Bank.data))

    @classmethod
    def __AccountGenerate(cls):
        alpha = random.choices(string.ascii_letters, k=3)
        num = random.choices(string.digits, k=3)
        spchar = random.choices("!@#$%^&*", k=1)
        acc_id = alpha + num + spchar
        random.shuffle(acc_id)
        return "".join(acc_id)

    def CreateAccount(self, name, age, email, pin):
        info = {
            "name": name,
            "age": age,
            "email": email,
            "pin": pin,
            "AccountNo": Bank.__AccountGenerate(),
            "balance": 0
        }

        if age < 18:
            return "Sorry, you cannot create your account."
        elif len(str(pin)) != 4:
            return "Invalid Pin. Try again."
        else:
            Bank.data.append(info)
            Bank.__update()
            return f"Account created successfully!\nAccount Number: {info['AccountNo']}"

    def DepositMoney(self, accNo, pin, amount):
        userdata = [i for i in Bank.data if i['AccountNo'] == accNo and i['pin'] == pin]
        if not userdata:
            return "Sorry, No Data Found"
        elif amount > 10000:
            return "Please deposit below 10,000."
        elif amount < 0:
            return "Enter a valid amount."
        else:
            userdata[0]['balance'] += amount
            Bank.__update()
            return "Amount deposited successfully."

    def WithdrawMoney(self, accNo, pin, amount):
        userdata = [i for i in Bank.data if i['AccountNo'] == accNo and i['pin'] == pin]
        if not userdata:
            return "Sorry, No Data Found"
        elif userdata[0]['balance'] < amount:
            return "Sorry, Insufficient balance."
        else:
            userdata[0]['balance'] -= amount
            Bank.__update()
            return "Amount withdrawn successfully."

    def ShowDetails(self, accNo, pin):
        userdata = [i for i in Bank.data if i['AccountNo'] == accNo and i['pin'] == pin]
        if not userdata:
            return "Sorry, No Data Found"
        else:
            details = "\n".join([f"{k}: {v}" for k, v in userdata[0].items()])
            return details

    def UpdateDetails(self, accNo, pin, name, email, new_pin):
        userdata = [i for i in Bank.data if i['AccountNo'] == accNo and i['pin'] == pin]
        if not userdata:
            return "Sorry, No Data Found"
        else:
            if name:
                userdata[0]['name'] = name
            if email:
                userdata[0]['email'] = email
            if new_pin:
                userdata[0]['pin'] = int(new_pin)
            Bank.__update()
            return "Details updated successfully."

    def DeleteAccount(self, accNo, pin):
        userdata = [i for i in Bank.data if i['AccountNo'] == accNo and i['pin'] == pin]
        if not userdata:
            return "Sorry, No Data Found"
        else:
            Bank.data.remove(userdata[0])
            Bank.__update()
            return "Account deleted successfully."


# Initialize Bank instance
bank = Bank()

# Streamlit UI
st.title("Banking System")

menu = ["Create Account", "Deposit Money", "Withdraw Money", "Show Details", "Update Details", "Delete Account"]
choice = st.sidebar.selectbox("Select an Action", menu)

if choice == "Create Account":
    st.subheader("Create a new Bank Account")
    name = st.text_input("Enter Your Name")
    age = st.number_input("Enter Your Age", min_value=18)
    email = st.text_input("Enter Your Email")
    pin = st.text_input("Enter Your 4-Digit Pin", max_chars=4)
    if st.button("Create Account"):
        if name and email and pin:
            pin = int(pin)
            result = bank.CreateAccount(name, age, email, pin)
            st.success(result)
        else:
            st.error("Please fill all the fields.")

elif choice == "Deposit Money":
    st.subheader("Deposit Money")
    accNo = st.text_input("Enter Your Account Number")
    pin = st.text_input("Enter Your Pin", max_chars=4)
    amount = st.number_input("Enter Amount to Deposit", min_value=1)
    if st.button("Deposit Money"):
        result = bank.DepositMoney(accNo, int(pin), amount)
        st.success(result)

elif choice == "Withdraw Money":
    st.subheader("Withdraw Money")
    accNo = st.text_input("Enter Your Account Number")
    pin = st.text_input("Enter Your Pin", max_chars=4)
    amount = st.number_input("Enter Amount to Withdraw", min_value=1)
    if st.button("Withdraw Money"):
        result = bank.WithdrawMoney(accNo, int(pin), amount)
        st.success(result)

elif choice == "Show Details":
    st.subheader("View Account Details")
    accNo = st.text_input("Enter Your Account Number")
    pin = st.text_input("Enter Your Pin", max_chars=4)
    if st.button("Show Details"):
        result = bank.ShowDetails(accNo, int(pin))
        st.text(result)

elif choice == "Update Details":
    st.subheader("Update Account Details")
    accNo = st.text_input("Enter Your Account Number")
    pin = st.text_input("Enter Your Pin", max_chars=4)
    name = st.text_input("Enter New Name (leave blank to skip)")
    email = st.text_input("Enter New Email (leave blank to skip)")
    new_pin = st.text_input("Enter New Pin (leave blank to skip)", max_chars=4)
    if st.button("Update Details"):
        result = bank.UpdateDetails(accNo, int(pin), name, email, new_pin)
        st.success(result)

elif choice == "Delete Account":
    st.subheader("Delete Account")
    accNo = st.text_input("Enter Your Account Number")
    pin = st.text_input("Enter Your Pin", max_chars=4)
    if st.button("Delete Account"):
        result = bank.DeleteAccount(accNo, int(pin))
        st.success(result)
