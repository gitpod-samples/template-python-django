from hashlib import sha256
import time
from cryptography.fernet import Fernet
from mysite.client import CreateCustomer

def app():
    client = CreateCustomer()()
    #REPLACE WITH STREAMLIT INPUT                                                       
    profileID = st.sidebar.text_input("Please enter your new account ID", key='10')              #Enters the new account ID.
    hashedProfileID = sha256(profileID.encode()).hexdigest()                                #Hashes it and turns it into hex string

    query = f"SELECT EXISTS(SELECT * FROM UserLoginData WHERE hashedUsername = \"{hashedProfileID}\") "       #Prepares SQL query

    queryResult = client.SQL_execute_twoway_statement(query)[0][0]                                            #Because the function returns an array with tuples, we want the first registry and the first element from the tuple.

    if queryResult:                                                                     #If the account is already registered, display message and continue in loop.
        st.error("This account ID is already registered, please try another one")
    elif profileID:
        with st.sidebar.form(key='sigup_form'):
            sign_up_form(profileID, hashedProfileID, client)

def sign_up_form(profileID, hashedProfileID, client):
    #REPLACE WITH STREAMLIT INPUT 
    profileName = st.text_input("Please enter your full name:", key='20')                                #Enters the person name.
    #REPLACE WITH STREAMLIT INPUT 
    profileAge = st.text_input("Please enter your age (Must be greater or equal than 18):", key='30')             #Enters the person age with bounds.
    #REPLACE WITH STREAMLIT INPUT 
    profileSex = st.text_input("Please enter the letter corresponding to your sex (Male = M) (Female = F):", key='40')                                       #Enters the person sex.
    #REPLACE WITH STREAMLIT INPUT 
    profilePassword = sha256(st.text_input("Please enter your password, must be minimum 6 characters long, maximum 30:", 
                                            type='password', 
                                            key='50', 
                                            max_chars=30).encode()).hexdigest()   #Enters the new account password with length bounds and hashes it.
    #REPLACE WITH STREAMLIT INPUT 
    #server = Server('https://horizon.stellar.org')
    server = Server('https://horizon-testnet.stellar.org')
    publicKey = st.text_input("Please your public key:", key='60')
    privateKey = st.text_input("Please your private key:", key='70', type='password')
    submit_but = st.form_submit_button('Sign Up') 

    #Prepares data into a hashMap (Dictionary)
    if submit_but:
        if not profileName or not profileAge or not profileSex or not profilePassword or not publicKey or not privateKey:
            st.warning('Please, fill all the fields to succesfuly sign up!')
        if int(profileAge) < 18:
            st.warning('You have to be greater than 18yo for sign up!')

        try:
            server.accounts().account_id(publicKey).call()
        except:
            #InputManager.display_message(message = "Invalid Stellar public key")
            error = st.error('We cannot found your Public Key!')
            st.stop()

        profileData = {
                "Username": profileID,
                "HashedUsername": hashedProfileID,
                "Name": profileName,
                "Age": profileAge,
                "Sex": profileSex,
                "Password": profilePassword,
                "PublicKey": publicKey,
                "PrivateKey": privateKey,
            }
        client.process_data(profileData)