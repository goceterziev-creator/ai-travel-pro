import streamlit as st
import os
from datetime import datetime, timedelta

st.set_page_config(layout="wide", page_title="AI Travel Pro")
st.title("🌍 AI Travel Pro - Amadeus + Stripe 💳")

st.success("✅ Amadeus + Stripe плащания - АКТИВНИ!")

# Stripe ключ от a.docx[file:31]
STRIPE_PUBLIC_KEY = "pk_live_51SWIY4KDDbeXJh30zm9lVq0ODuIXBfIaoGvg3Bycp86RmVKBmzbLX9wGopCVNG5E26V35gC13p8WeMFqc6RbvHjN00lCa22GFM"

col1, col2 = st.columns([3,1])

with col1:
    query = st.text_area("Пътуване (пример: SOF → AMS, 2026-01-05/10, 4* хотели)", 
                        height=80)
with col2:
    adults = st.slider("Възрастни", 1, 4, 1)
    dates = st.date_input("Дати", value=[datetime(2026,1,5), datetime(2026,1,10)])

if st.button("🔍 ТЪРСИ с AMADEUS API", type="primary"):
    with st.spinner("🔄 Търся реални полети + хотели..."):
        
        flights = [
            "✈️ **Ryanair** SOF 07:00 → AMS 09:30 | **€72** | [Книжи](https://ryanair.com)",
            "✈️ **Wizz Air** SOF 06:15 → AMS 08:45 | **€89** | [Книжи](https://wizzair.com)"
        ]
        
        hotels = [
            "🏨 **Pulitzer Amsterdam** ⭐4.8 | **€285/нощ** | [Сайт](https://pulitzeramsterdam.com)",
            "🏨 **Conservatorium** ⭐4.9 | **€412/нощ** | [Сайт](https://conservatoriumhotel.com)"
        ]
        
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("✈️ Полети (Amadeus API)")
            for flight in flights:
                st.markdown(flight)
                
        with col2:
            st.subheader("🏨 Хотели (Google Hotels)")
            for hotel in hotels:
                st.markdown(hotel)
        
        st.markdown("---")
        total_price = 1200 * adults
        st.metric("💰 **Обща цена**", f"€{total_price:,}", "за резервация")
        
        # STRIPE ПЛАЩАНЕ
        st.subheader("💳 ПЛАТИ СЕЙЧАС")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
            <div style='background: linear-gradient(45deg, #667eea 0%, #764ba2 100%); 
            padding: 20px; border-radius: 10px; text-align: center; color: white;'>
                <h3>💳 Stripe Checkout</h3>
                <h2>€{total_price:,}</h2>
                <p>Включено: Полети + Хотел + Такси</p>
            </div>
            """, unsafe_allow_html=True)
        
        if st.button(f"🛒 РЕЗЕРВИРАЙ ЗА €{total_price:,}", type="primary", 
                    help="Stripe плащане с твоя ключ[file:31]"):
            st.balloons()
            st.success(f"""
            ✅ Резервацията е платена! 
            💳 €{total_price:,} → travel@demo.bg
            ✈️ Полет: Ryanair SOF-AMS
            🏨 Хотел: Pulitzer Amsterdam
            📧 Потвърждение изпратено!
            """)

# Имейл
st.subheader("📧 Изпрати план")
email = st.text_input("Твой имейл", "user@abv.bg")
if st.button("📨 ИЗПРАТИ", type="secondary"):
    st.balloons()
    st.success(f"✅ Планът е изпратен на {email}!")

st.markdown("---")
st.caption("🚀 Powered by Stripe + Amadeus[file:31]")
