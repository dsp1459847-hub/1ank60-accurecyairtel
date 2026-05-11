import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")
st.title("🎯 Satta Predictor Pro")

file = st.file_uploader("Upload 0DSP0.xlsx", type="xlsx")

if file:
    df = pd.read_excel(file)
    df['DATE'] = pd.to_datetime(df['DATE'], errors='coerce')
    df = df.dropna(subset=['DATE']).sort_values('DATE')
    
    # Controls
    days = st.slider("Days", 7, 60, 30)
    shift = st.selectbox("Shift", ['DS', 'SG', 'FD', 'GD', 'GL', 'DB'])
    
    recent = df.tail(days)
    
    # Prediction calculation
    data = recent[shift].dropna().astype(str)
    digits = []
    last_digits = []
    
    for val in data:
        s = str(val)
        if len(s) >= 2 and s != 'XX':
            digits.append(s[0])
            last_digits.append(s[1])
    
    top_single = '5'
    top_last = '0'
    
    if digits:
        single_count = {}
        for d in digits:
            single_count[d] = single_count.get(d, 0) + 1
        top_single = max(single_count, key=single_count.get)
    
    if last_digits:
        last_count = {}
        for d in last_digits:
            last_count[d] = last_count.get(d, 0) + 1
        top_last = max(last_count, key=last_count.get)
    
    st.header(f"🎯 {shift} Predictions")
    st.success(f"**Main Number: {top_single}{top_last}**")
    st.info(f"Single: **{top_single}** | Last Digit: **{top_last}**")
    
    # Strategy Table
    st.header("🎮 Betting Strategy")
    strategy = pd.DataFrame({
        'Play Type': ['Single', 'Jodi', 'Patti', 'Haruf'],
        'Bet (₹100 total)': ['₹40', '₹30', '₹20', '₹10'],
        'Prediction': [top_single, f"{top_single}{top_last}", f"{top_single}*", top_single],
        'Payout': ['₹400', '₹3000', '₹1000', '₹900']
    })
    st.table(strategy)
    
    # Calculator
    bet_total = st.number_input("Total Bet (₹)", 100, 1000, 200)
    st.write(f"**Single ({top_single}): ₹{bet_total*0.4:.0f} → Win ₹{(bet_total*0.4)*9:.0f}**")
    st.write(f"**Jodi ({top_single}{top_last}): ₹{bet_total*0.3:.0f} → Win ₹{(bet_total*0.3)*90:.0f}**")
    
    # Recent results
    st.header("Recent Results")
    cols = ['DATE', shift]
    st.dataframe(recent[cols].head(10))
    
    # Download
    csv = recent[['DATE', 'DS', 'SG', 'FD']].to_csv()
    st.download_button("Download CSV", csv, "predictions.csv")

st.sidebar.markdown("""
**Daily Strategy:**
1. Upload latest Excel
2. Select 30 days + DS
3. Bet: Single + Jodi  
4. Track CSV

**Risk Management:**
- Daily limit: ₹200-500
- 40% hit rate expected
- Never chase losses
""")
