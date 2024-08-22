
import streamlit as st
from db_connection import connect_training_data_collection

collection_data = connect_training_data_collection()

def insert_data(input_text):

    collection_data = connect_training_data_collection()

    if input_text != '':
        document ={'text': input_text}

        insert_document = collection_data.insert_one(document)
        st.write(insert_document.inserted_id)
    else:
        st.warning('Please insert your data')


def add():
    st.header('Create new training data')
    with st.form('insert_data'):
        question = st.text_input('What is your question?')
        

        answer = st.text_input('What is your answer?')
        
        
        if st.form_submit_button('Commit', type='primary'):
            if question and answer:
                if '?' not in question:
                    question += '?'

                if '//:' not in answer:
                    if '.' not in answer:
                        answer += '.'
                insert_data(question)
                insert_data(answer)
                st.write(question)
                st.write(answer)
                st.success('Data inserted successfully!')
            else:
                st.error('Both Question and Answer are Required!')
