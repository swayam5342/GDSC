from sqlconnect import connect_to_mysql
import os
from dotenv import load_dotenv
load_dotenv('.env')
config={
    'host':os.getenv('host'),
    'user':os.getenv('user'),
    'password':os.getenv('password'),
    'database':os.getenv('database')
}

con = connect_to_mysql(config)

def get_data():
    name=input("Enter the name : ")
    gender=input("Enter the gender : ")
    phone_number=int(input('Enter the Number if not')) or 1
    return name, gender , phone_number
data = con.cursor.execute("SELECT * FROM user_responses")
data=data.featchall()
for i in data:
    ...