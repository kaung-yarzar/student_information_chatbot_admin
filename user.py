import pandas as pd
import streamlit as st
from db_connection import connect_user_collection
#from bson.objectid import ObjectId

import re

collection_user = connect_user_collection()


def validate_email(e):
    email_check = collection_user.find_one({'email' : e}, {'_id' : 0, 'username' :0, 'password' : 0})
    if email_check == None:
        return True   # True means user can create account



## checking username is already exists in database
def validate_username(u):
    username_check = collection_user.find_one({'username' : u}, {'_id' : 0, 'email' :0, 'password' : 0})
    if username_check == None:
        return True   # True means user can create account



## Checking email is in true format
def check_email(e):
    # pattern = "^[a-z0-9_]+@[a-z0-9]+\.[a-z]{1,3}$"
    pattern = "^[a-z0-9_]+@tumeiktila\.edu\.mm$"
    if re.match(pattern, e):
        return True



## Checking username is in true format
def check_username(u):
    pattern = "^[a-zA-Z0-9]*$"
    if re.match(pattern, u):
        return True
    

def check_password(p):
    pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[_@$!?*&^%#:;]).{8,}$"
    return bool(re.match(pattern, p))



##### user create function
def insert_user(e, u, p, q, a):
    

    if u and e and p != '':
        document ={'username': u, 'email': e, 'password': p , 'security_question': q, 'security_answer': a}

        insert_document = collection_user.insert_one(document)
        st.success('User inserted successfully!')
        #st.write(insert_document.inserted_id)
    else:
        st.warning('Please insert your data')



def user():
##### user create form
    st.subheader('User Accounts')
    with st.form('insert_user', clear_on_submit=True):
        e = st.text_input('Email : ')
        u = st.text_input('Username :')
        p = st.text_input('Password : ', type = 'password')
        q = st.selectbox(
            "Security Question :",
            ("Who is your favourite teacher?",
            "What is the name of your first pet?",
            "What is your favourite book?",
            "Waht is your favorite movie?",
            "What is your favorite song?",
            "Who is your first love?",
            "Where is your home town?",
            "What is your dream?",
            "Who is your favourite star?"), )
        a = st.text_input( label ='Answer :')
        if st.form_submit_button('Create', type='primary'):
            # Assuming you have an `insert_data` function that handles database insertion
            if u and e and p and q and a:  
                if check_email(e) == True:
                    if validate_email(e) == True:
                        if check_username(u) ==True:
                            if validate_username(u) == True:
                                if len(u) > 3:
                                    if check_password(p):
                                        if len(a) > 2:
                                            #hashed_password = stauth.Hasher([confirm_password]).generate()
                                            #insert_user(email, username, hashed_password[0]) # hashed password က array အနေနဲ့ထွက်လာလို့ 0 index ထောက်
                                            insert_user(e, u, p, q, a)
                                            st.toast('Account Created Successfully. Please Login...',icon='✅')
                                        else:
                                            st.toast("Please Answer Security Question", icon ='❌')
                                    else:
                                        st.toast('Password should contains at least 8 characters, one uppercase letter, one lowercase letter, one digit and one special character', icon ='❌')
                                else:
                                    st.toast('Username Should Have At Least 4 Characters', icon ='❌')
                            else:
                                st.toast('Username Already Exists', icon ='❌')
                        else:
                            st.toast('Username Should be Alphabets or Numbers', icon ='❌')
                    else:
                        st.toast('Your Account Is Already Exist. Please Try to Login Instead', icon ='❌')
                else:
                    st.toast('Enter a TU Meiktila Edu Email Address', icon ='❌')
            else:
                st.toast('Please fill out all **Required** fields', icon ='❌')












            



##### user view


    collection_user = connect_user_collection() # db connect

    documents = list(collection_user.find({}, {})) # query

    col1, col2 = st.columns(2)

    for i, doc in enumerate(documents): # make card for each user
        with col1 if i % 2 == 0 else col2:
            with st.container(border=True, height=340):
                doc_id = doc['_id']
                updated_username = st.text_input("username : ", value=doc['username'])
                updated_email = st.text_input("email : ", value=doc['email'])
                updated_password = st.text_input("password : ", value=doc['password'])
                #if st.button(f"Update {doc_id}"):
                

##### user update
                co1, co2 = st.columns(2)
                with co1:
                    if st.button(f"Update", key=f'update{doc_id}', use_container_width=True, type='primary'):
                        try:
                            # Update the user in MongoDB
                            result = collection_user.update_one(
                                {"_id": doc_id},
                                {"$set": {"username": updated_username, "email": updated_email, "password": updated_password}}
                            )

                            if result.modified_count == 1:
                                st.toast(f"User with ID {doc_id} updated successfully!", icon='📤')
                            else:
                                st.toast(f"User with ID {doc_id} update failed.", icon='❌')
                        except Exception as e:
                            st.toast(f"Error during update: {e}")


##### user delete              
                with co2:
                    if st.button(f"Delete", key=f'delete{i}', use_container_width=True, type='primary'):
                        try:
                            
                            result = collection_user.delete_one({"_id": doc_id})

                            if result.deleted_count == 1:
                                st.toast(f"User with ID {doc_id} deleted successfully!", icon='🗑️')
                                st.rerun()
                            else:
                                st.toast(f"User with ID {doc_id} deletion failed.", icon='❌')
                        except Exception as e:
                            st.toast(f"Error during deletion: {e}")


##### user function end