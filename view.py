
import streamlit as st


import pandas as pd
from db_connection import connect_training_data_collection
from wordcloud import WordCloud
from collections import Counter
import re

st.cache_resource
def view():
    collection_data = connect_training_data_collection()
    data = collection_data.find()
    df = pd.DataFrame(data)
    #st.dataframe(df, width=1000, hide_index=True)
    #table
    df_copy = df.copy()

    ######## sentences
    st.title('Training Data')
    question_mark_count = df['text'].str.count(r'\?$').sum()
    image = df['text'].str.count(r's+\.$').sum()
    df_wo_i = df[~df['text'].str.contains(r'https')]
    fullstop = df_wo_i['text'].str.count(r'\.$').sum()
    exclimation=df_wo_i['text'].str.count(r'!$').sum()
    


    st.write(f"Questions count: **{question_mark_count}**")
    st.write(f"Text Answers count: **{fullstop+exclimation}**")
    st.write(f"Image Answers count: **{image}**")
    #################


    st.divider()

    ###### bar chart

    # Remove links from the text
    df['text'] = df['text'].apply(lambda x: re.sub(r'http\S+', '', x))

    # Tokenize the text and count word frequencies
    word_counts = Counter(" ".join(df['text']).split())

    # Create a DataFrame from the word counts
    word_df = pd.DataFrame(word_counts.items(), columns=['Word', 'Frequency'])

    # Sort by frequency (optional)
    word_df.sort_values(by='Frequency', ascending=False, inplace=True)

    # Streamlit app
    st.title("Word Frequency Bar Chart")
    st.bar_chart(word_df.set_index('Word'))


    st.divider()

    # Optionally, you can display the raw data as well
    st.title("Word Frequencies Table")
    st.dataframe(word_df, use_container_width=True)


    
    ###########

    st.divider()

    ###### Wdord Cloud

    # Assuming you have a DataFrame 'df' with a 'text' column
    # Concatenate all text into a single string
    all_text = ' '.join(df['text'])

    # Create the WordCloud
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(all_text)

    # Display the word cloud
    st.title("Word Cloud")
    #st.markdown("<h1 style='text-align: center;'>Student Information Chatbot</h1>", unsafe_allow_html=True)

    st.markdown("        ")
    st.image(wordcloud.to_array())
    
    #st.dataframe(df, width=800, height=400)

    ################

    st.divider()

    ####### Sentences
    st.title('Training Sentences')
    st.dataframe(df_copy[['text']], hide_index=True, use_container_width=True)

