import pandas as pd
import streamlit as st
from db_connection import connect_training_data_collection
#from bson.objectid import ObjectId



def edit():
    # Connect to your MongoDB collection
    collection_data = connect_training_data_collection()

    # Fetch all documents
    documents = list(collection_data.find({}, {"_id": 1, "text": 1}))





    # Display data in two columns
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader('Question')
    with col2:
        st.subheader('Answer')

    for i, doc in enumerate(documents):
        with col1 if i % 2 == 0 else col2:
            with st.container(border=True, height=190):
                doc_id = doc['_id']
                #updated_text = st.text_input(f"ID : {doc_id}", value=doc['text'])
                updated_text = st.text_area(f"Text : {doc['_id']}", value=f"{doc['text']}", label_visibility="collapsed")


                #if st.button(f"Update {doc_id}"):
                if st.button("Update",key =doc_id , use_container_width=True, type='primary'):
                    try:
                        # Update the document in MongoDB
                        result = collection_data.update_one(
                            {"_id": doc_id},
                            {"$set": {"text": updated_text}}
                        )

                        if result.modified_count == 1:
                            st.toast(f"Document with ID {doc_id} updated successfully!",icon='✅')
                        else:
                            st.toast(f"Document with ID {doc_id} not found or update failed.",icon='❌')
                    except Exception as e:
                        st.error(f"Error during update: {e}")




# def edit():
#     # Connect to your MongoDB collection
#     collection_data = connect_training_data_collection()

#     # Fetch all documents
#     documents = list(collection_data.find({}, {"_id": 1, "text": 1}))

#     # Display data in two columns
#     col1, col2 = st.columns(2)
#     with col1:
#         st.subheader('Question')
#     with col2:
#         st.subheader('Answer')

#     for i, doc in enumerate(documents):
#         with col1 if i % 2 == 0 else col2:
#             with st.container(border=True, height=160):
#                 doc_id = doc['_id']
#                 updated_text = st.text_input(f"ID : {doc_id}", value=doc['text'])

#                 #if st.button(f"Update {doc_id}"):
#                 if st.button(f"Update {doc_id}", use_container_width=True):
#                     try:
#                         # Update the document in MongoDB
#                         result = collection_data.update_one(
#                             {"_id": doc_id},
#                             {"$set": {"text": updated_text}}
#                         )

#                         if result.modified_count == 1:
#                             st.success(f"Document with ID {doc_id} updated successfully!")
#                         else:
#                             st.warning(f"Document with ID {doc_id} not found or update failed.")
#                     except Exception as e:
#                         st.error(f"Error during update: {e}")