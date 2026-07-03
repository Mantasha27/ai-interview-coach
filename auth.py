import streamlit as st
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def login_system(cursor, conn):
    if "user" not in st.session_state:
        st.session_state.user = None

    if st.session_state.user is None:
        # --- UI STYLING: RED & CHARCOAL ON WHITE ---
        st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap');
        
        /* 1. Background: Solid White */
        .stApp {
            background-color: #ffffff !important;
            font-family: 'Inter', sans-serif;
        }

        /* 2. Main Login Card: Dark Charcoal */
        [data-testid="stVerticalBlockBorderWrapper"] {
            background-color: #1a1a1a !important; 
            padding: 50px 40px !important;
            border-radius: 0px !important; 
            max-width: 420px;
            margin: auto;
            border: none !important;
            box-shadow: 0 15px 35px rgba(0,0,0,0.1) !important;
        }

        /* 3. Header Styling: Dark Red/Black */
        .brand-title {
            text-align: center;
            color: #b91c1c; /* Professional Red */
            font-size: 26px;
            font-weight: 300;
            letter-spacing: 5px;
            margin-bottom: 30px;
            text-transform: uppercase;
        }

        /* 4. Inputs: Light Grey with Sharp Edges */
        .stTextInput input {
            background-color: #e5e7eb !important;
            color: #111827 !important;
            border-radius: 0px !important;
            border: none !important;
            height: 48px !important;
        }

        /* 5. Login Button: Bold Red */
        div.stButton > button[kind="primary"] {
            background-color: #dc2626 !important; /* Bright Red */
            color: white !important;
            border-radius: 0px !important;
            border: none !important;
            height: 52px !important;
            text-transform: uppercase;
            letter-spacing: 3px;
            font-weight: 600;
            margin-top: 20px;
        }

        /* 6. Register Button: Dark matching the box */
        div.stButton > button[kind="secondary"] {
            background-color: #1a1a1a !important;
            color: #ffffff !important;
            border-radius: 0px !important;
            border: 1px solid #dc2626 !important; /* Red Border */
            height: 52px !important;
            text-transform: uppercase;
            letter-spacing: 3px;
            margin-top: 15px;
        }

        /* Hover States */
        div.stButton > button[kind="primary"]:hover {
            background-color: #b91c1c !important;
        }

        header, footer { visibility: hidden; }
        </style>
        """, unsafe_allow_html=True)

        # --- UI LAYOUT ---
        st.markdown('<div class="brand-title">Interview Coach</div>', unsafe_allow_html=True)

        with st.container(border=True):
            username = st.text_input("Username", placeholder="Username", label_visibility="collapsed")
            password = st.text_input("Password", type="password", placeholder="Password", label_visibility="collapsed")
            
            # Sign In
            login_btn = st.button("Sign In", type="primary", use_container_width=True)

        # Register
        register_btn = st.button("Create Account", type="secondary", use_container_width=True)

        # --- LOGIC ---
        if login_btn:
            if username and password:
                hashed = hash_password(password)
                cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, hashed))
                user = cursor.fetchone()
                if user:
                    st.session_state.user = username
                    st.rerun()
                else:
                    st.error("Invalid Login")
            else:
                st.toast("Credentials required", icon="🔒")

        if register_btn:
            if username and password:
                hashed = hash_password(password)
                try:
                    cursor.execute("INSERT INTO users (username, password) VALUES (?,?)", (username, hashed))
                    conn.commit()
                    st.success("Account created! Please sign in.")
                except:
                    st.error("Username already exists")

        st.stop()
    else:
        # Side Bar
        with st.sidebar:
            st.write(f"Logged in as: {st.session_state.user}")
            if st.button("Logout", use_container_width=True):
                st.session_state.user = None
                st.rerun()