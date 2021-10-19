import requests
import psycopg2
from hashlib import sha256
import time
from cryptography.fernet import Fernet
import streamlit as st
import pandas as pd
import os

class CreateCustomer:
    def __init__(self):
        self.email = ''
        self.first_name = ''
        self.middle_name = ''
        self.last_name = ''
        self.city = ''
        self.state = ''
        self.country = ''
        self.phone_number = ''
        self.sessionID = ""
        self.hashedSessionID = ""
        self.sessionPassword = ""
        self.privateKey = ""
        self.encryptKey = ""
        self.sex = ""
        self.age = ""
        self.balances = ""

        self.posSQLConfig = {
                    'user': '',
                    'password': '',
                    'host': '',
                    'database': ''
                    }

        self.public_network_passphrase=Network.PUBLIC_NETWORK_PASSPHRASE
        self.SQL_initialize()
        


    def SQL_initialize(self):
        #self.connection = mysql.connector.connect(**self.mySQLConfig)
        
        self.connection = psycopg2.connect(**self.posSQLConfig)

    def SQL_execute_oneway_statement(self,query):
        try:
            statement = self.connection.cursor()

            statement.execute(query)

            self.connection.commit()

            statement.close()

            queryExecuted = True
        except TypeError as e:
            # InputManager.display_message(f"Error: {e}")
            queryExecuted = False

        
        return queryExecuted
    
    def SQL_execute_twoway_statement(self,query):
        try:
            statement = self.connection.cursor()

            statement.execute(query)

            data = []

            queryResult = statement.fetchone()

            while (queryResult != None):
                registry = queryResult
                data.append(registry)

                queryResult = statement.fetchone()
            
            # print(data)
            
            statement.close()
        except Exception as e:
            #InputManager.display_message(f"Error: {e}")
            data = "Error in query"
        return st.erro(data)
    
    def process_data(self, profileData):                                                                                     #<---------- Handles all data required inputs for account creation ---------->
        

        encryptKey = Fernet.generate_key()  #Generates a unique encryption key
        fernetKey = Fernet(encryptKey)      #Generates a Fernet object for encrypting things with the key in bytes format
        encryptKey = encryptKey.decode()     #Passes the key to a string

        #STARTS QUERIES FOR UserLoginData TABLE

        query = f"INSERT INTO UserLoginData VALUES(\"{profileData['HashedUsername']}\" , \"{profileData['Password']}\", \"{encryptKey}\")"  #Prepares the SQL query
        queryResult = self.SQL_execute_oneway_statement(query)                                                                              #Executes the SQL query

        if not queryResult:                                                                                 #If this query wasn't successful, print error.
            st.error("There was an error while creating your account, query 1")
            return

        #FINISHES QUERIES FOR UserLoginData TABLE

        usernameSpecialHash = profileData["Username"]+"WDSI"                                                    #We salt the username with a 'WSDI' string for more security
        usernameSpecialHash = sha256(usernameSpecialHash.encode()).hexdigest()                                  #We hash the username

        bytesPrivateKey = profileData["PrivateKey"].encode()                                                    #Gets the private key and pass it into a bytes format
        encryptedPrivateKey = fernetKey.encrypt(bytesPrivateKey).decode()                                       #Encrypts the private key and pass it to string

        bytesName = profileData["Name"].encode()                                                                #Passes the name and pass it into bytes format
        encryptedName = fernetKey.encrypt(bytesName).decode()                                                   #Encrypts the name and pass it to string

        balances = "{}"

        #STARTS QUERIES FOR UserData TABLE

        query2 = f"INSERT INTO UserData VALUES(\"{usernameSpecialHash}\",\"{encryptedPrivateKey}\",\"{encryptedName}\", \"{profileData['Sex']}\", {profileData['Age']},\"{balances}\")" #Prepares SQL query
        queryResult2 = self.SQL_execute_oneway_statement(query2)

        if not queryResult2:                                                                                    #If this query wasn't successful, print error.
            st.error("There was an error while creating your account, query 2")
            return

        #FINISHES QUERIES FOR UserData TABLE


        #STARTS QUERIES FOR UserPublicKey TABLE
    
        query3 = f"INSERT INTO UserPublicKey VALUES(\"{profileData['Username']}\",\"{profileData['PublicKey']}\")"
        queryResult3 = self.SQL_execute_oneway_statement(query3)

        #FINISHES QUERIES FOR UserPublicKey TABLE

        if not queryResult3:
            st.error(message = "There was an error while creating your account, query 2")
            return

        #st.info(f"Encrypt Key: {encryptKey}")                                         #If no errors, display successful creation
        st.success("Account succesfully created")                                        #If no errors, display successful creation