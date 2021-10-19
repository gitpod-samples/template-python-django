import streamlit as st
import requests

def app():
    with st.expander('Click here for more information'):
        st.text('''
        This form will only works if you are already logged into https://escrow.com
        Then, you can use your password or you API Key for making transactions and trade
        cryptocurrencies or whatever you want to trade! This app is consuming the escrow.com API.
        ''')
    
    with st.form('Fill this form to make a transaction!'):
        field1, field2 = st.columns((2,2))
        with field1:
            escrow_email = st.text_input('Your Escrow.com email')
            first_customer = st.text_input("The customer email. If it's not you, put the email", value='me')
            your_role = st.selectbox('Your role in this transaction', options=['buyer', 
                                                                                'seller', 
                                                                                'broker', 
                                                                                'partner'])
        with field2:
            api_or_password = st.text_input('Your Escrow API or Password', type='password')
            second_customer = st.text_input('The destinatary email for the transaction')
            other_part_role = st.selectbox('The other part role in this transaction', options=['buyer', 
                                                                                                'seller', 
                                                                                                'broker', 
                                                                                                'partner'])
        description = st.text_area('Do you want to let any message or description of the transaction?', 
                                    max_chars=30)
        
        field11, field22 = st.columns((2,2))
        with field11:
            title = st.text_input('Title')
            currency = st.selectbox('The currency for this transaction', options=['usd', 
                                                                                    'euro',
                                                                                    'aud', 
                                                                                    'gbp'])
        
            quantity = st.number_input(label='How many items do you want to trade?', min_value=1)
            who_pays = st.text_input(label="Who is gonna pay for this transaction? If it's you, put 'me'")  
        with field22:
            item_type = st.selectbox('What type of item do you want to trade?', options=['Domain names',
                                                                                    'General Merchandise',
                                                                                    'Motor Vehicles',
                                                                                    'Services']) 
            amount = float(st.text_input(label='Specify the amount for your item. Ex.: 1000 or 1250.25', value=0))
            who_receive = st.text_input(label='Put the email of the one who is gonna receive the payment')

            item_description = st.text_area('Describe your item')
        
        submit = st.form_submit_button('Make transaction')
    
        if submit:


            request = requests.post(
                'https://api.escrow.com/2017-09-01/transaction',
                auth=(escrow_email, api_or_password),
                json={
                    "parties": [
                        {
                            "role": your_role,
                            "customer": first_customer
                        },
                        {
                            "role": other_part_role,
                            "customer": second_customer
                        }
                    ],
                    "currency": currency,
                    "description": description,
                    "items": [
                        {
                            "title": title,
                            "description": item_description,
                            "type": item_type,
                            "inspection_period": 259200,
                            "quantity": quantity,
                            "schedule": [
                                {
                                    "amount": amount,
                                    "payer_customer": who_pays,
                                    "beneficiary_customer": who_receive
                                }
                            ]
                        }
                    ]
                },
            )
            st.success(request.content)
