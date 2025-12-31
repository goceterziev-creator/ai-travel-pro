🚀 AYA AI TRAVEL STUDIO - ФИНАЛЕН РАБОТЕЩ КОД (30 сек deploy)

КОПИРАЙ ТОЗИ КОД → app_pro.py → COMMIT → LIVE!

import streamlit as st
import pandas as pd
from datetime import datetime
import urllib.parse
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

st.set_page_config(layout="wide")
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {background: linear-gradient(135deg, #00b4db 0%, #0083b0 100%); color: white;}
.main .block-container {padding-top: 2rem;}
.aya-card {background: rgba(255,255,255,0.1); backdrop-filter: blur(15px); border-radius: 20px; padding: 2rem; border: 1px solid rgba(255,255,255,0.2);}
.stButton > button {background: white !important; color: #0083b0 !important; border-radius: 25px !important; font-weight: bold !important; padding: 1rem 2rem !important;}
h1 {color: white !important; font-size: 3.5rem !important; text-align: center;}
</style>
""", unsafe_allow_html=True)

FROM_EMAIL = "goce_terziev@abv.bg"
TO_EMAIL = "aya.smart.store@gmail.com"
WHATSAPP = "359894842882"

def send_email(name, origin, dest, total):
    try:
        sg = SendGridAPIClient(st.secrets["SENDGRID_API_KEY"])
        msg = Mail(from_email=FROM_EMAIL, to_emails=TO_EMAIL, 
                  subject=f"NEW CLIENT €{total}", 
                  plain_text_content=f"NEW CLIENT €{total}\n{name}\n{origin}-{dest}")
        sg.send(msg)
        return True
    except:
        return False

st.markdown('<div class="aya-card">', unsafe_allow_html=True)
st.title("🤖 ПЕТЯ")

col1, col2 = st.columns(2)
with col1:
    origin = st.selectbox("От", ["SOF"])
    dest = st.selectbox("До", ["AMS"])
    name = st.text_input("Име")
with col2:
    date1 = st.date_input("Излитане", datetime(2026,1,5))
    date2 = st.date_input("Връщане", datetime(2026,1,10))
    adults = st.slider("Възрастни", 1, 4, 2)

if st.button("ПЛАТИ €2400"):
    if name:
        sent = send_email(name, origin, dest, 2400)
        if sent:
            st.success("✅ ИЗПРАТЕНО НА БИЛЯНА!")
            st.balloons()
            st.markdown(f'[WhatsApp](https://wa.me/{WHATSAPP}?text=NEW%20CLIENT%20{name})', unsafe_allow_html=True)
        else:
            st.error("Email грешка!")
    else:
        st.warning("Въведи име!")

st.markdown('</div>', unsafe_allow_html=True)
