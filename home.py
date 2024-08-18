
import streamlit as st
st.set_page_config(page_title = 'Student Information Chatbot Admin Control', page_icon = '🕯️')

if "username" not in st.session_state:
    st.session_state.username = ''
if "role" not in st.session_state:
    st.session_state.role = ''

from streamlit_option_menu import option_menu

from db_connection import connect_admin_collection
from add import add
from view import view
from remove import remove
from edit import edit
from user import user
from admin import admin

collection = connect_admin_collection()

@st.cache_resource
def authenticate(username, password):
    
    admin = collection.find_one({"username": username, "password": password})
    if admin:
        st.session_state.role = admin['role']
    else:
        st.session_state.role = ''
    return admin is not None


def display_login_form():
    
    st.markdown("<h1 style='text-align: center;'>Student Information Chatbot</h1>", unsafe_allow_html=True)
    st.markdown(" ")
    with st.form("login_form"):
        # c1, c2, c3 = st.columns([2, 1, 2])
        # with c2:
        st.header("Admin Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        # c1, c2, c3, c4, c5 = st.columns([1,1.1,1,1,1])
        # with c3:
        if st.form_submit_button("Login", type = 'primary'):
            if authenticate(username, password):
                st.session_state['username'] = username  # Mark the user as logged in
                admin_role = collection.find_one({"username": username, "password": password})
                st.session_state.role = admin_role['role']

                st.rerun()
                st.balloons()
            else:
                st.error("Invalid credentials. Please try again.")

        return username






def display_after_login_successful():
    # st.header("Welcome Admin")
    # st.write("You are logged in. Enjoy your experience!")
    with st.sidebar:
        selected = option_menu("Admin Menu", ['Dashboard', 'Add', 'Edit', 'Remove','User', 'Admin'], 
            icons=[ 'graph-up', 'plus-lg', 'feather', 'trash2','people', 'wrench'], menu_icon="cast", default_index=0)
        #selected
    if selected == "Dashboard":
        view()
    if selected == "Add":
        add()
    if selected == "Edit":
        edit()
    if selected =="Remove":
        remove()
    if selected == "User":
        user()
    if selected == "Admin":
        admin()
    
    




def main():
    # Check if the user is already logged in
    
    if st.session_state['username']:
        st.sidebar.header(f"WELCOME {st.session_state['username'].upper()}") 
        st.sidebar.markdown(f"Logged in as : **{st.session_state['role']}**")
        display_after_login_successful()

        
        if st.sidebar.button("Refresh", use_container_width=True):
            st.rerun()

        if st.sidebar.button("Logout", use_container_width=True):                # Logout button
            # st.session_state.pop("logged_in")  # Clear the login status
            st.session_state.pop("username")
            st.session_state.pop("role")
            st.rerun()

        
    else:
        display_login_form()


if __name__ == "__main__":
    #st.markdown(st.session_state)
    main()

#     st.markdown(
#     """
#     <style>
#     div[data-testid="stButton"]{
#          text-align: center;
#             display: block;
#             margin-left: auto;
#             margin-right: auto;
#             width: 100%;
 
#     }
#     </style>
#     """,
#     unsafe_allow_html=True,
# )
    
    

    st.markdown(
    """
    <style>
    div[data-testid="stFormSubmitButton"]{
         text-align: center;
            display: block;
            margin-left: auto;
            margin-right: auto;
            width: 100%;
 
    }
    </style>
    """,
    unsafe_allow_html=True,
)
    
    st.markdown(
    """
    <style>
    div[data-testid="stHeadingWithActionElements"]{
         text-align: center;
            display: block;
            margin-left: auto;
            margin-right: auto;
            width: 100%;
 
    }
    </style>
    """,
    unsafe_allow_html=True,
)
    