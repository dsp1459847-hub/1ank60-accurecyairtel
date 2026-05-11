import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")
st.title("🎰 Satta King Full Strategy")

# File upload
file = st.file_uploader("0DSP0.xlsx")

if file:
    df = pd.read_excel(file)
    df['DATE'] = pd.to_datetime(df['DATE'], errors='coerce')
    df = df.dropna(subset=['DATE']).sort_values('DATE')
    
    # Controls
    days = st.slider("Analysis Days", 7, 60, 30)
    shift = st.selectbox("Main Shift", ['DS', 'SG', 'FD', 'GD'])
    
    recent = df.tail(days)
    
    st.header(f"🎯 {shift} Strategy")
    
    # Prediction Logic
    data = recent[shift].dropna().astype(str)
    digits = []
    for val in data:
        s = str(val)
        if len(s) >= 2 and s != 'XX':
            digits.append(s)
    
    if len(digits) >= 5:
        # Classify numbers
        single_digits = [d[0] for d in digits]
        last_digits = [d[1] for d in digits]
        
        # Most common
        top_single = max(set(single_digits), key=single_digits.count)
        top_last = max(set(last_digits), key=last_digits.count)
        
        # Form 2-digit numbers
        predictions = []
        for s in [top_single]:
            for l in [top_last, str((int(top_last)+1)%10), str((int(top_last)-1)%10)]:
                predictions.append(s+l)
        
        st.success(f"**Class A (Safe): {top_single}{top_last}**")
        st.info(f"**Class B: {', '.join(predictions[:3])}**")
        st.write(f"**Jodi: {top_single}{top_last}, {top_single}0-{top_single}9**")
    
    # Full Game Strategy
    st.header("🎮 Complete Betting Strategy")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### **Class 1 - Safe Play (₹100)**
        | Bet | Amount | Payout |
        |-----|--------|--------|
        | {top_single} | ₹40 | ₹400 |
        | {top_single}{top_last} | ₹30 | ₹3000 |
        | {top_single}* | ₹30 | ₹300 |

        **Total Risk: ₹100**
        **Min Return: ₹400**
        """.format(top_single=top_single, top_last=top_last))
    
    with col2:
        st.markdown("""
        ### **Class 2 - High Risk (₹200)**
        | Bet | Amount | Payout |
        |-----|--------|--------|
        | Top 3 Jodi | ₹100 | ₹10000 |
        | Patti | ₹50 | ₹5000 |
        | Single | ₹50 | ₹500 |

        **Max Win: ₹10000+**
        """)
    
    # Live Results
    st.header("📊 Recent {shift} Results".format(shift=shift))
    st.dataframe(recent[['DATE', shift]].head(10))
    
    # Betting Calculator
    st.header("💰 Profit Calculator")
    bet_amount = st.number_input("Bet Amount (₹)", 100, 10000, 500)
    win_single = st.number_input("Single Payout (₹)", 90, 100, 90)
    win_jodi = st.number_input("Jodi Payout (₹)", 90, 100, 90)
    
    if st.button("Calculate"):
        single_bet = bet_amount * 0.4
        jodi_bet = bet_amount * 0.3
        patti_bet = bet_amount * 0.3
        
        st.success(f"""
        **Single Win: ₹{single_bet * win_single:.0f}**
        **Jodi Win: ₹{jodi_bet * win_jodi * 10:.0f}**  
        **Patti Win: ₹{patti_bet * 50:.0f}**
        **Best Case: ₹{(single_bet * win_single + jodi_bet * win_jodi * 10):.0f}**
        """)
    
    # Download strategy sheet
    strategy_data = {
        'Play': ['Safe Single', 'Jodi', 'Patti', 'Haruf'],
        'Amount': [40, 30, 30, 100],
        'Prediction': [top_single, f"{top_single}{top_last}", f"{top_single}*", top_single],
        'Payout': [400, 3000, 300, 900]
    }
    csv_strategy = pd.DataFrame(strategy_data).to_csv(index=False)
    st.download_button("📥 Download Strategy CSV", csv_strategy, "strategy.csv")

# Sidebar Game Rules
st.sidebar.header("🎲 How to Play")
st.markdown("""
1. **Class A**: Safe - Single + Jodi
2. **Class B**: Risky - Patti + Haruf  
3. **Daily Routine**:
   - Morning: Update Excel
   - Predict → Bet ₹100-500
   - Track CSV
""")

st.balloons()
