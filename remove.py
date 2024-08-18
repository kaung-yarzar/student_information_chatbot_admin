import pandas as pd
import streamlit as st
from db_connection import connect_training_data_collection
from bson.objectid import ObjectId


##### 

def remove():

    collection_data = connect_training_data_collection()

##### text view
    documents = collection_data.find({}, {"_id": 1, "text": 1})
    col1, col2 = st.columns(2)
    with col1:
        st.subheader('Question')
    with col2:
        st.subheader('Answer')
    for i, doc in enumerate(documents):
        with col1 if i % 2 == 0 else col2:
            with st.container(border=True, height=190):
                #st.write(f"ID: {doc['_id']}")
                st.text_area(f"Text : {doc['_id']}", value=f"{doc['text']}", disabled =True, label_visibility="collapsed")


##### text delete
                if st.button(f"Delete", key =doc['_id'], use_container_width=True, type='primary'):
                    try:

                        result = collection_data.delete_one({"_id": ObjectId(doc['_id'])})
                        if result.deleted_count == 1:
                            #st.success("Document deleted successfully.")
                            st.toast('DELETED SUCCESSFULLY', icon='🗑️')
                            st.rerun()
                        else:
                            st.toast("Document not found or deletion failed.", icon='‼️')
                    except Exception as e:
                        st.error(f"Error during deletion: {e}")
                   
##### delete function end



# def remove():
#     collection_data = connect_training_data_collection()

#     # Display data in two columns
#     documents = collection_data.find({}, {"_id": 1, "text": 1})
#     col1, col2 = st.columns(2)
#     with col1:
#         st.subheader('Question')
#     with col2:
#         st.subheader('Answer')
#     for i, doc in enumerate(documents):
#         with col1 if i % 2 == 0 else col2:
#             with st.container(border=True, height=180):
#                 st.write(f"ID: {doc['_id']}")
#                 st.write(f"Text: {doc['text']}")

#                 # Delete button for each document
#                 if st.button(f"Delete {doc['_id']},{i}"):
#                     try:

#                         result = collection_data.delete_one({"_id": ObjectId(doc['_id'])})
#                         if result.deleted_count == 1:
#                             #st.success("Document deleted successfully.")
#                             #st.toast('DELETED SUCCESSFULLY', icon='🗑️')
#                             st.rerun()
#                         else:
#                             st.warning("Document not found or deletion failed.")
#                     except Exception as e:
#                         st.error(f"Error during deletion: {e}")
