from dotenv import load_dotenv 
load_dotenv() 
import streamlit as st 
import os 
import google.generativeai as genai 
import psycopg2

# Configure API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-2.0-flash")

# Database connection
def connect_db():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT")
    )

def create_table():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS query_logs (
        id SERIAL PRIMARY KEY,
        user_input TEXT,
        bot_response TEXT
    );
    """)
    conn.commit()
    cur.close()
    conn.close()

def log_query(user_input, bot_response):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO query_logs (user_input, bot_response) VALUES (%s, %s);", (user_input, bot_response))
    conn.commit()
    cur.close()
    conn.close()

def my_output(query):
    response = model.generate_content(query) 
    return response.text 

#### UI Development using streamlit 

st.set_page_config(page_title="QUERY_BOT")
st.header("QUERY_BOT") 
input = st.text_input("Input " , key = "input")  
submit = st.button("Ask your query") 

create_table()

if submit:
    response = my_output(input) 
    log_query(input, response)
    st.subheader("The Response is=")
    st.write(response)
