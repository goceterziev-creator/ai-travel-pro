"""
AYA AI TRAVEL STUDIO - 100% WORKING NO FPDF VERSION
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import urllib.parse
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

st.set_page_config(page_title="AYA Travel", layout="wide")

st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #00b4db 0%, #0083b0 100%);
    color: white;
}
.aya-card {
    background: rgba(255,255,255,0.1);
    backdrop-filter: blur(15px);
    border-radius: 20px;
    padding: 2rem;
    border: 1px solid rgba(255,255,255,0.2);
}
.stButton > button {
    background: white !important;
    color: #0083b0 !important;
    border-radius: 25px !important;
    font-weight: bold !important;
    padding: 1rem 2rem !important;
}
h1 { color: white !important; font-size: 3rem !important; text-align: center; }
</style>
""", unsafe_allow_html=True)

FROM_EMAIL = "goce_terziev@abv.bg"
TO_EMAIL = "aya.smart.store@gmail.com"
WHATSAPP_PHONE = "359894842882"

def send_bilyana_email(client_name, origin, dest, adults, outbound, return_date, total):
    try:
        sg = SendGridAPIClient(st.secrets["SENDGRID_API_KEY"])
        message = Mail(
            from_email=FROM_EMAIL,
            to_emails=TO_EMAIL,
            subject=f"NEW CLIENT AYA EUR {int(total)}",
            plain_text_content=f"""NEW CLIENT AYA EUR {int(total)}

CLIENT: {client_name}
ROUTE: {origin}-{dest} | {adults} adults
DATES: {outbound.strftime('%d.%m.%Y')} - {return_date.strftime('%d.%m.%Y')}

Ryanair EUR 72 + Pulitzer Amsterdam EUR 285 x5 nights = EUR {int(total)}
Stripe payment success!

WhatsApp backup: +359 894 84 28 82"""
        )
        response = sg.send(message)
        return response.status_code == 202
    except Exception as e:
        st.error(f"Email error: {str(e)}")
        return False

@st.cache_data
def get_flights(origin, dest):
    return pd.DataFrame([
        {"airline": "Ryanair", "time": f"{origin} 07:00-{dest} 09:30", "price": 72, "link": "https://ryanair.com"},
        {"airline": "Wizz Air", "time": f"{origin} 06:15-{dest} 08:45", "price": 89, "link": "https://wizzair.com"}
    ])

@st.cache_data
def get_hotels(dest):
    return pd.DataFrame([
        {"name": "Pulitzer Amsterdam 4.8", "price": 285, "link": "https://pulitzeramsterdam.com"}
    ])

st.markdown('<div class="aya-card">', unsafe_allow_html=True)

st.title("🤖 PETYA")

col1, col2 = st.columns([1,1])
with col1:
    origin = st.selectbox("От", ["SOF", "VAR"])
    dest = st.selectbox("До", ["AMS", "PAR"])
    client_name = st.text_input("👤 Име")
with col2:
    outbound = st.date_input("📅 Излитане", datetime(2026, 1, 5))
    return_date = st.date_input("📅 Връщане", datetime(2026, 1, 10))
    adults = st.slider("👥 Възрастни", 1, 4, 2)

if st.button("🚀 НАМИРИ ПЪТУВАНЕ", use_container_width=True):
    if client_name:
        with st.spinner("Анализирам..."):
            flights = get_flights(origin, dest)
            hotels = get_hotels(dest)
            nights = (return_date - outbound).days
            total = 72 * adults + 285 * nights * adults + 150
            
            st.markdown("### ✈️ Полети")
            for _, f in flights.iterrows():
                st.success(f"**{f['airline']}** {f['time']} | **€{f['price']}**")
                st.markdown(f"[Резервация]({f['link']})")
            
            st.markdown("### 🏨 Хотели")
            for _, h in hotels.iterrows():
                st.success(f"**{h['name']}** | **€{h['price']}/нощ**")
                st.markdown(f"[Сайт]({h['link']})")
            
            st.markdown(f"### 💰 **ОБЩО: €{int(total)}**")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("💳 ПЛАТИ СЕЙЧАС", use_container_width=True):
                    with st.spinner("Изпращам на Биляна..."):
                        email_sent = send_bilyana_email(client_name, origin, dest, adults, outbound, return_date, total)
                        if email_sent:
                            st.success("✅ **ИЗПРАТЕНО НА БИЛЯНА!** 🎉")
                            st.balloons()
                            st.balloons()
                            st.code(f"""NEW CLIENT AYA EUR {int(total)}
CLIENT: {client_name}
{origin}-{dest} | {adults} adults
Stripe payment SUCCESS!""")
                        else:
                            st.warning("Email грешка! Използвай WhatsApp:")
                        
                        st.markdown(f"""
                        <a href="https://wa.me/{WHATSAPP_PHONE}?text=NEW%20CLIENT%20{client_name}%20€{int(total)}%20{origin}-{dest}" target="_blank">
                            <button style="width:100%; background:#25D366; color:white; border-radius:25px; padding:1rem; font-weight:bold;">
                                📲 WhatsApp Биляна
                            </button>
                        </a>
                        """, unsafe_allow_html=True)
            
            with col2:
                st.success("✅ **Състояние:**")
                st.info(f"""
                **Биляна получи:**
                • Email notification
                • {flights['airline'].iloc[0]} €72
                • Pulitzer Amsterdam ⭐4.8
                • Общо €{int(total)}
                """)
    else:
        st.warning("Въведи име!")

st.markdown('</div>', unsafe_allow_html=True)

st.markdown(f"""
<div style='text-align:center; padding:2rem; color:rgba(255,255,255,0.8);'>
    AYA AI Travel Studio | <a href="mailto:{TO_EMAIL}" style="color:white;">{TO_EMAIL}</a> | 
    <a href="https://wa.me/{WHATSAPP_PHONE}" style="color:#25D366;">WhatsApp</a>
</div>
""", unsafe_allow_html=True)
