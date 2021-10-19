import streamlit as st
st.set_page_config(page_title='Escrow App', layout='wide', initial_sidebar_state='auto')
import datetime
from multiapp import MultiPage
import home

app = MultiPage()

# Title of the main page
st.title("Escrow transaction")

#st.header("")
st.write("""Developed by:
- Data Science Manager - Anade Davis [[Linkedin](https://www.linkedin.com/in/anadedatascientist/)]
- Financial Data Scientist - Moxú [[Linkedin](https://www.linkedin.com/in/dairenkonmajime/)]
"""
)


st.markdown('---')

custom_green = 'rgb(124, 230, 110)'
custom_red = 'rgb(230, 134, 110)'
custom_blue = 'rgb(110, 186, 230)'
custom_orange = 'rgb(230, 172, 110)'

home.app()

#app.run()

