from bs4 import BeautifulSoup
import lxml
import requests
import mysql.connector
import sys
import Internshala
import BigShyft
import TimesJobs

global mydb

def If_database_exist(host,user,password):
    global mydb
    def If_connection_established():
        try:
            global mydb 
            mydb=mysql.connector.connect(
            host=host,
            user=user,
            password=password
            )
            return mydb.is_connected()
        except mysql.connector.Error as err:
            print(f'Unable to Establish Connection: {err}')
            return False
    
    def Initiate_values(cur,table_name):
        global mydb
        cur=Internshala.insert_values(cur,table_name)
        mydb.commit()
        cur=TimesJobs.insert_values(cur,table_name)
        mydb.commit()
        cur=BigShyft.insert_values(cur,table_name)
        mydb.commit()
        return cur
    
    def ask_for_table(cur):
        global mydb
        opt=input(f"""
        Choose any one:
         1 :To Use existing table.
         2 :To Create a new table.
         3 :To Exit the program. 
        --> Your input: """)
        if opt=='1':
            table_name=input("Enter the name of the table: ")
            cur.execute('SHOW TABLES;')
            tables=[table[0] for table in cur.fetchall()]
            if table_name in tables:
                print(f'{table_name} Exists!!')
                print(f'Truncating {table_name}...')
                cur.execute(f'Truncate {table_name};')
                mydb.commit()
                print("Initiating Webscrapping!")
                cur=Initiate_values(cur,table_name)
                return cur
            else:
                print(f"{table_name} does not exists !")
                print("!!!!!!!!!!!!! OPT FOR CREATING A TABLE: !!!!!!!!!!!!!!!!!!!")
                print()
                ask_for_table(cur)
                return cur
        elif opt=='2':
            cur.execute('SHOW TABLES;')
            table_name=input('Enter the new name for the table: ')
            tables=[table[0] for table in cur.fetchall()]
            if table_name in tables:
                print(f'{table_name} Exists!!')
                print(f'Truncating {table_name}...')
                cur.execute(f'Truncate {table_name};')
                mydb.commit()
                print("Initiating Webscrapping!")
                cur=Initiate_values(cur,table_name)
                return cur
            else:
                print("Table doesn't exists....creating a new one")
                cur.execute(f"""
                CREATE TABLE {table_name}
                (JOB_TITLE VARCHAR(80),
                COMPANY_NAME VARCHAR(70),
                SKILLS VARCHAR(200) DEFAULT NULL,
                EXPERIENCE VARCHAR(50) DEFAULT NULL,
                SALARY VARCHAR(50),
                LOCATION VARCHAR(200));""")
                mydb.commit()
                print("Table Created!!")
                print("Initiating the Webscrapping!")
                cur=Initiate_values(cur,table_name)
                return cur
        else:
            print("Exiting the program!!")
            mydb.close()
            sys.exit(0)

    if If_connection_established():
        print("Connection Established!!")
        database=input("Enter the Database you wanna work on: ")
        print("Checking if Database Exists...")
        cur=mydb.cursor()
        cur.execute('SHOW DATABASES;')
        databases=[row[0] for row in cur.fetchall()]
        if database in databases:
            print("Database Already Exists!!")
            cur.close()
            cur=mydb.cursor()
            cur.execute(f"USE {database}")
            print('Ready to use database!!')
            cur=ask_for_table(cur)
            return cur
        else:
            print(f"Creating database {database}")
            # Assuming you have a cursor object after connecting to MySQL (not shown here)
            cur.execute(f"CREATE DATABASE {database}")
            # (Optional) Use the new database
            cur.execute(f"USE {database}")
            print(f'Ready to use {database}!!')
            cur=ask_for_table(cur)
            return cur
    else:
        print("Try to fix the code...Unable to connect")
        sys.exit(-1)


host='localhost'
print("Establishing Connection...")
user=input("Enter the Username of MySQL: ")
password=input("Enter the Password for given host: ")
cur=If_database_exist(host,user,password)
mydb.commit()
mydb.close()
print("Work done!!")