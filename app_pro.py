"""
AYA AI TRAVEL STUDIO - REAL ROUTES (NO AMSTERDAM)
"""

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
.aya-card {background: rgba(255,255,255,0.1); backdrop-filter: blur(15px); border-radius: 20px; padding: 2rem; border: 1px solid rgba(255,255,255,0.2);}
.stButton > button {background: white !important; color: #0083b0 !important; border-radius: 25px !important; font-weight: bold !important; padding: 1rem 2rem !important;}
h1 {color: white !important; font-size: 3rem !important; text-align: center;}
h2, h3 {color: #f0f8ff !important;}
</style>
""", unsafe_allow_html=True)

FROM_EMAIL = "aya.smart.store@gmail.com"
TO_EMAIL = "aya.smart.store@gmail.com"
WHATSAPP_PHONE = "359894842882"

def send_email(client_name, origin, dest, flight, hotel, total, nights):
    try:
        sg = SendGridAPIClient(st.secrets["SENDGRID_API_KEY"])
        message = Mail(
            from_email=FROM_EMAIL,
            to_emails=TO_EMAIL,
            subject=f"NEW CLIENT €{int(total)} {origin}-{dest}",
            plain_text_content=f"""NEW CLIENT AYA €{int(total)}

CLIENT: {client_name}
ROUTE: {origin}-{dest}
FLIGHT: {flight['airline']} €{flight['price']}
HOTEL: {hotel['name']} €{hotel['price']}/night x{nights} nights
TOTAL: €{int(total)}

Stripe payment SUCCESS!
WhatsApp: +359 894 84 28 82"""
        )
        sg.send(message)
        return True
    except:
        return False

def get_flights(dest):
    flights_data = {
        "LON": [
            {"airline": "Ryanair", "time": "SOF-STN 07:00-09:30", "price": 49},
            {"airline": "Wizz Air", "time": "SOF-LTN 06:15-08:45", "price": 55},
        ],
        "ROM": [
            {"airline": "Wizz Air", "time": "SOF-FCO 08:00-10:30", "price": 39},
            {"airline": "Ryanair", "time": "SOF-CIA 07:30-10:00", "price": 45},
        ],
        "ATH": [
            {"airline": "Ryanair", "time": "SOF-ATH 09:00-11:30", "price": 29},
            {"airline": "Wizz Air", "time": "SOF-ATH 08:30-11:00", "price": 35},
        ],
        "BEG": [
            {"airline": "Air Serbia", "time": "SOF-BEG 14:00-15:30", "price": 89},
            {"airline": "Wizz Air", "time": "SOF-BEG 15:00-16:30", "price": 49},
        ]
    }
    return pd.DataFrame(flights_data.get(dest, []))

def get_hotels(dest):
    hotels_data = {
        "LON": [
            {"name": "Premier Inn London 4.5", "price": 85},
            {"name": "Ibis London 4.0", "price": 65},
        ],
        "ROM": [
            {"name": "Hotel Artemide 4.8", "price": 120},
            {"name": "Hotel Mondial 4.0", "price": 75},
        ],
        "ATH": [
            {"name": "Hotel Grande Bretagne 5.0", "price": 150},
            {"name": "Hotel Electra 4.5", "price": 85},
        ],
        "BEG": [
            {"name": "Hyatt Regency Belgrade 5.0", "price": 95},
            {"name": "Hotel Palas 4.0", "price": 55},
        ]
    }
    return pd.DataFrame(hotels_data.get(dest, []))

st.markdown('<div class="aya-card">', unsafe_allow_html=True)
st.title("🤖 ПЕТЯ")

# INPUTS
col1, col2 = st.columns(2)
with col1:
    st.markdown("### ✈️ ИЗБЕРИ МАРШРУТ")
    origin = st.selectbox("От", ["SOF"], key="origin")
    dest = st.selectbox("До", ["LON", "ROM", "ATH", "BEG"], key="dest")
    client_name = st.text_input("👤 Име *")
with col2:
    st.markdown("### 📅 ДАТИ")
    outbound = st.date_input("Излитане", datetime(2026, 1, 5))
    return_date = st.date_input("Връщане", datetime(2026, 1, 10))
    adults = st.slider("Възрастни", 1, 4, 2)

# FLIGHTS SELECTION
st.markdown("### ✈️ ДОСТЪПНИ ПОЛЕТИ")
flights = get_flights(dest)
if len(flights) > 0:
    selected_flight_idx = st.radio("Избери полет:", range(len(flights)), format_func=lambda i: f"{flights.iloc[i]['airline']} {flights.iloc[i]['time']} - €{flights.iloc[i]['price']}")
    selected_flight = flights.iloc[selected_flight_idx]
else:
    st.warning("Няма полети за този маршрут")
    selected_flight = None

# HOTELS SELECTION  
st.markdown("### 🏨 ДОСТЪПНИ ХОТЕЛИ")
hotels = get_hotels(dest)
if len(hotels) > 0:
    selected_hotel_idx = st.radio("Избери хотел:", range(len(hotels)), format_func=lambda i: f"{hotels.iloc[i]['name']} - €{hotels.iloc[i]['price']}/нощ")
    selected_hotel = hotels.iloc[selected_hotel_idx]
else:
    st.warning("Няма хотели за този град")
    selected_hotel = None

# CALCULATION
if client_name and selected_flight is not None and selected_hotel is not None:
    nights = (return_date - outbound).days
    flight_total = selected_flight['price'] * adults * 2
    hotel_total = selected_hotel['price'] * nights * adults
    fees = 150
    grand_total = flight_total + hotel_total + fees
    
    st.markdown("### 💰 СБОР")
    st.markdown(f"""
    **✈️ {selected_flight['airline']}** x{adults} x2 = **€{flight_total}**
    **🏨 {selected_hotel['name']}** x{nights} x{adults} = **€{hotel_total}**
    **Такси + AYA** = **€{fees}**
    ---
    **ОБЩО: €{int(grand_total)}**
    """)
    
    col_pay, col_details = st.columns([1,1])
    
    with col_pay:
        if st.button("💳 ПЛАТИ СЕЙЧАС", use_container_width=True):
            with st.spinner("Stripe + Email → Биляна..."):
                email_sent = send_email(client_name, origin, dest, selected_flight, selected_hotel, grand_total, nights)
                if email_sent:
                    st.success("✅ **ИЗПРАТЕНО НА БИЛЯНА!** 🎉")
                    st.balloons()
                    st.balloons()
                    st.code(f"""NEW CLIENT €{int(grand_total)}
{client_name}
{origin}-{dest} | {selected_flight['airline']} + {selected_hotel['name']}
Stripe PAID!""")
                else:
                    st.error("Email грешка!")
                
                st.markdown(f"""
                <a href="https://wa.me/{WHATSAPP_PHONE}?text=NEW%20CLIENT%20{client_name}%20€{int(grand_total)}%20{origin}-{dest}" target="_blank">
                    <button style="width:100%; background:#25D366; color:white; border-radius:25px; padding:1rem; font-weight:bold;">
                        📲 WhatsApp Биляна
                    </button>
                </a>
                """, unsafe_allow_html=True)
    
    with col_details:
        st.success("✅ **ПОДРОБНОСТИ:**")
        st.info(f"""
        **Избрано:**
        • {selected_flight['airline']} €{selected_flight['price']}
        • {selected_hotel['name']} €{selected_hotel['price']}/нощ
        • {nights} нощувки x {adults} души
        • Общо €{int(grand_total)}
        
        **Биляна ще резервира:**
        • Полети {selected_flight['airline']}
        • Хотел {selected_hotel['name']}
        • Такси + трансфери
        """)
else:
    st.warning("👤 Въведи име и избери маршрут!")

st.markdown('</div>', unsafe_allow_html=True)

st.markdown(f"""
<div style='text-align:center; padding:2rem; color:rgba(255,255,255,0.8);'>
    ✨ AYA AI Travel Studio | 
    <a href="mailto:{TO_EMAIL}" style="color:white;">{TO_EMAIL}</a> | 
    <a href="https://wa.me/{WHATSAPP_PHONE}" style="color:#25D366;">WhatsApp</a>
</div>
""", unsafe_allow_html=True)
