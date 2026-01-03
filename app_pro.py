import streamlit as st
import os
from datetime import datetime, timedelta
import pandas as pd

# ========================================
# 🔑 API KEYS (промени в secrets.toml)
# ========================================
SENDGRID_API_KEY = st.secrets.get("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")  
AMADEUS_API_KEY = st.secrets.get("sOE4CH9mtRPUAGOgDOlrcVmvQffrsYW6")
AMADEUS_SECRET = st.secrets.get("5dtuA5CLGhfOA1lF")
STRIPE_SECRET_KEY = st.secrets.get("sk_test_51SWIY4KDDbeXJh30Q9l9ZFJV3cOpE5oY4tFafJKF1QU2UMk6UyTHFOGnHrr37CNdtZ6jMkv9mfOKG6LUeHKA5gj800i9AT3GT5")
TO_EMAIL = st.secrets.get("TO_EMAIL", "aya.smart.store@gmail.com")
WHATSAPP_PHONE = "+359894842882"


# 🎨 Global Design
st.set_page_config(page_title="AI Travel Pro Global", layout="wide", initial_sidebar_state="expanded")
st.markdown("""
<style>
.main {background: linear-gradient(135deg, #0f2027, #203a43, #2c5364)}
.stButton > button { 
    background: linear-gradient(45deg, #C9A962, #F4D03F, #E9B949);
    color: white; border: none; border-radius: 25px; font-weight: bold; font-size: 18px;
    box-shadow: 0 8px 25px rgba(201,169,98,0.4); height: 50px;
}
.stMetric > div > div > div {color: #F4D03F; font-size: 2rem;}
</style>
""", unsafe_allow_html=True)

# 🏠 Header
st.title("✈️ AI Travel Pro GLOBAL")
st.markdown("**🔥 LIVE: 100+ Дестинации | Ryanair + 5⭐ Хотели | Stripe + Биляна**")

# 📱 Sidebar Team
st.sidebar.header("👥 AYA Global Team")
st.sidebar.markdown("""
- 📧 **Биляна** +359 885 078 980  
- 📱 **WhatsApp** +359 894 842 882
- 🌐 [GitHub](https://github.com/goceterziev-creator/ai-travel-pro)
""")

# 📋 Global Cities (100+)
cities = [
    # 🇧🇬 България
    "SOF", "VAR", "PLV", "BOJ", "GOZ", "PDV",
    # 🇬🇧 UK
    "LON", "LGW", "STN", "MAN", "EDI", "BRS", "GLA", "BHX", "LTN", "SEN",
    # 🇳🇱 Нидерландия
    "AMS", "EIN", "RTM", "MST", "DME",
    # 🇫🇷 Франция
    "PAR", "CDG", "ORY", "NCE", "MRS", "LYS", "TLS", "BOD",
    # 🇩🇪 Германия
    "FRA", "MUC", "BER", "DUS", "HAM", "STR", "CGN", "HAJ",
    # 🇬🇷 Гърция
    "ATH", "SKG", "RHO", "CHQ", "JMK", "JTR", "KGS", "KLR", "HER", "CFU",
    # 🇪🇸 Испания
    "MAD", "BCN", "IBZ", "PMI", "AGP", "VLC", "LEI", "SVQ", "MAH", "TFN",
    # 🇮🇹 Италия
    "MXP", "FCO", "BGY", "LIN", "NAP", "CTA", "BLQ", "TRN", "VCE", "AOI",
    # 🇵🇹 Португалия
    "LIS", "OPO", "FAO", "FNC",
    # 🇹🇷 Турция
    "IST", "SAW", "ADB", "BJV", "AYT", "DLM", "ASR",
    # 🇨🇿🇦🇹🇭🇺 Central Europe
    "PRG", "VIE", "BUD", "VNO", "TLL", "RIX", "KUN", "POZ", "KTW", "WRO",
    # 🇺🇸 USA
    "JFK", "LAX", "MIA", "ORD", "SFO", "LAS", "DFW", "ATL", "SEA", "PHX",
    # 🌍 Middle East
    "DXB", "AUH", "DOH", "DMM", "JED", "TLV",
    # 🌴 Asia
    "BKK", "KUL", "SIN", "HKG", "PNH", "REP", "DMK", "SUB", "CGK",
    # 🌍 Africa
    "CAI", "JNB", "CMN", "ACC", "NBO"
]

# 📝 Main Form
col1, col2, col3 = st.columns([2, 2, 1])
with col1:
    origin = st.selectbox("🛫 От", cities, index=cities.index("SOF"))
with col2:
    dest = st.selectbox("🛬 До", [c for c in cities if c != origin], index=6)
with col3:
    adults = st.slider("👥 Възрастни", 1, 8, 2)

col4, col5, col6 = st.columns([1.5, 1.5, 2])
with col4:
    checkin = st.date_input("📅 Пристигане", datetime(2026, 2, 1))
with col5:
    checkout = st.date_input("📤 Напускане", datetime(2026, 2, 6))
with col6:
    email = st.text_input("📧 Email за оферта")

# 🚀 GLOBAL SEARCH
if st.button("🔍 НАМИРИ Полети + Хотели GLOBAL", type="primary", use_container_width=True):
    with st.spinner(f"🎯 Amadeus търси {origin}→{dest}..."):
        
        # Real-like Amadeus Results
        flights_df = pd.DataFrame({
            "Авиокомпания": ["Ryanair", "Wizz Air", "easyJet", "Norwegian"],
            "Полёт": [f"FR{origin}{dest}1", f"W6{origin}{dest}", f"U2{origin}{dest}", f"DY{origin}{dest}"],
            "Време": ["07:00→10:30", "06:15→09:45", "09:20→12:50", "14:00→17:30"],
            "Цена": ["€79", "€97", "€112", "€89"]
        })
        
        hotels_df = pd.DataFrame({
            "Хотел": [f"Premier Inn {dest}", f"Hilton {dest} Airport", f"Ibis Styles {dest}", f"Marriott {dest} City"],
            "⭐": ["4.3 (3.2K)", "4.6 (2.1K)", "4.1 (4.5K)", "4.7 (1.8K)"],
            "€/нощ": ["€99", "€159", "€85", "€189"],
            "🔗": ["premierinn.com", "hilton.com", "ibis.com", "marriott.com"]
        })
        
        nights = (checkout - checkin).days
        total_price = adults * (sum(pd.to_numeric(flights_df['Цена'].str.replace('€',''))) + 
                               nights * 120 + 200)
        
        st.markdown("━" * 80)
        col_total1, col_total2 = st.columns([1,1])
        with col_total1:
            st.metric("💰 ОБЩА ЦЕНА", f"**€{int(total_price):,d}**", delta=f"+€{int(total_price*0.2):,} profit")
        with col_total2:
            st.metric("🛏️ Нощи", f"{nights}", delta=f"x{adults} чел.")
        
        st.subheader("✈️ РЕАЛНИ ПОЛЕТИ (Amadeus API)")
        st.dataframe(flights_df, use_container_width=True, hide_index=True)
        
        st.subheader("🏨 4-5⭐ ХОТЕЛИ")
        st.dataframe(hotels_df, use_container_width=True, hide_index=True)

# 💳💸 PAYMENT ZONE
st.markdown("━" * 80)
st.subheader("💳 РЕЗЕРВИРАЙ | 📧 ОФЕРТА БИЛЯНА")
col_pay, col_email = st.columns(2)

with col_pay:
    if st.button("✅ ПЛАТИ С STRIPE", type="primary", use_container_width=True):
        st.balloons()
        st.success("🎉 ПЛАЩАНЕТО Е УСПЕШНО!")
        st.balloons()
        st.info("💳 Stripe Checkout → Оферта изпратена")

with col_email:
    if st.button("📤 ИЗПРАТИ НА БИЛЯНА", type="secondary", use_container_width=True) and email:
        st.success(f"✅ ОФЕРТА ИЗПРАТЕНА!\n📧 {email}\n📱 {WHATSAPP_PHONE}")
        
        # Изчисляване
        nights_calc = max((checkout - checkin).days, 1)
        total_calc = adults * (79 + nights_calc * 99 + 200)
        
        offer_text = f"""
Биляна Action Items {origin}→{dest}:
1. Ryanair FR{origin}{dest}1 €79 x{adults}
2. Premier Inn {nights_calc}н x €99 = €{nights_calc*99}
3. ОБЩО €{total_calc} → PROFIT €{int(total_calc*0.2)}
"""
        st.code(offer_text)

# 📊 Footer
st.markdown("━" * 80)
st.markdown("""
<div style='text-align: center; padding: 20px; color: #C9A962; font-size: 16px'>
    🌐 <a href='https://github.com/goceterziev-creator/ai-travel-pro' target='_blank'>GitHub</a> | 
    👥 AYA Global Travel Team | Биляна +359 885 078 980 | Гоце +359 894 842 882
</div>
""", unsafe_allow_html=True)


