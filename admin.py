import pandas as pd
import streamlit as st
from db_connection import connect_admin_collection
import re

##### admin create function
def insert_admin(n, u, p, r):
    collection_admin = connect_admin_collection()

    if n and u and p != '':
        document ={'name': n, 'username': u, 'password': p, 'role' : r}
        st.success('admin inserted successfully!')
        insert_document = collection_admin.insert_one(document)
        #st.write(insert_document.inserted_id)
    else:
        st.warning('Please insert your data')

def check_password(p):
    pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[_@$!?*&^%#:;]).{8,}$"
    return bool(re.match(pattern, p))





#check admin role
def superadmin():
##### admin create form
    st.subheader('Admin Accounts')
    with st.form('insert_admin', clear_on_submit=True):
        n = st.text_input('name :')
        u = st.text_input('username : ')
        p = st.text_input('Password : ', type="password")
        r  = st.radio(
            "What's is the admin role?",
            [":rainbow[Super Admin]",  "Admin"],
            index=1,)
        if st.form_submit_button('Create', type ='primary'):

            if n and u and p and r:
                if len(n) > 3:
                    if len(u) > 3:
                        if check_password(p):
                            insert_admin(n, u, p, r)
                            st.toast('Admin inserted Successfully', icon='✅')
                        else:
                            st.toast('Password should contains at least 8 characters, one uppercase letter, one lowercase letter, one digit and one special character', icon='❌')
                    else:
                
                        st.toast('Username is too short', icon='❌')
                else:
                    st.toast('Name is too short',icon='❌')
                
            else:
                st.toast('All fields are required', icon='❌')
            



##### admin view
    collection_admin = connect_admin_collection() # db connect

    documents = list(collection_admin.find({}, {})) # query

    col1, col2 = st.columns(2)

    for i, doc in enumerate(documents): # make card for each admin
        with col1 if i % 2 == 0 else col2:
            with st.container(border=True, height=370):
                doc_id = doc['_id']
                st.markdown(f"role : **{doc['role']}**")
                updated_name = st.text_input("name : ", value=doc['name'])
                updated_username = st.text_input("username : ", value=doc['username'])
                updated_password = st.text_input("password : ", value=doc['password'])
                
                #if st.button(f"Update {doc_id}"):
                

##### admin update
                co1, co2 = st.columns(2)
                with co1:
                    if st.button(f"Update", key=doc_id, use_container_width=True, type='primary'):
                        try:
                            # Update the admin in MongoDB
                            result = collection_admin.update_one(
                                {"_id": doc_id},
                                {"$set": {"name": updated_name, "username": updated_username, "password": updated_password}}
                            )

                            if result.modified_count == 1:
                                st.toast(f"admin with ID {doc_id} updated successfully!", icon ='📤')
                            else:
                                st.toast(f"admin with ID {doc_id}update failed.", icon='❌')
                        except Exception as e:
                            st.error(f"Error during update: {e}")


##### admin delete              
                with co2:
                    if st.button(f"Delete", key=i, use_container_width=True, type='primary'):
                        try:
                            
                            result = collection_admin.delete_one({"_id": doc_id})

                            if result.deleted_count == 1:
                                st.toast(f"admin with ID {doc_id} deleted successfully!", icon='🗑️')
                                st.rerun()
                            else:
                                st.toast(f"admin with ID {doc_id} deletion failed.", icon='❌')
                        except Exception as e:
                            st.error(f"Error during deletion: {e}")
#####  super admin function end


def normal_admin():
    st.subheader('Admin Accounts')
##### admin view
    collection_admin = connect_admin_collection() # db connect

    documents = list(collection_admin.find({}, {})) # query

    col1, col2 = st.columns(2)

    for i, doc in enumerate(documents): # make card for each admin
        with col1 if i % 2 == 0 else col2:
            with st.container(border=True, height=250):
                doc_id = doc['_id']
                st.markdown(f"role : **{doc['role']}**")
                st.text_input("name : ", value=doc['name'], disabled = True)
                st.text_input("username : ", value=doc['username'], disabled = True)
                #if st.button(f"Update {doc_id}"):
                
##### normal admin function end



def admin():

    admin_role = st.session_state['role']
    if 'Super' in admin_role:
        superadmin()
    else:
        normal_admin()
