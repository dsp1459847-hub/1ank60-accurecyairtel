import streamlit as st
import pandas as pd
from datetime import datetime

# Page Setup
st.set_page_config(page_title="MAYA Adaptive Super-AI", layout="wide")

st.title("🎯 MAYA Adaptive Super-AI v2.0")

# File Upload
uploaded_file = st.file_uploader("Upload your Prediction CSV", type=["csv"])

if uploaded_file:
    try:
        # 1. डेटा लोड करना
        df = pd.read_csv(uploaded_file, skip_blank_lines=True).dropna(how='all')
        
        # कॉलम के नाम से फालतू स्पेस हटाना
        df.columns = [str(c).strip().upper() for c in df.columns]
        
        # --- आपकी फाइल के हिसाब से कॉलम मैपिंग ---
        # आपकी फाइल में: FD (Faridabad), GD (Ghaziabad) है
        col_map = {
            'DS': 'DS',
            'FB': 'FD',  # आपकी फाइल का FD
            'GB': 'GD',  # आपकी फाइल का GD
            'GL': 'GL'
        }

        # चेक करना कि क्या ये कॉलम फाइल में हैं
        missing = [v for k, v in col_map.items() if v not in df.columns]
        
        if missing:
            st.error(f"Error: फाइल में ये कॉलम नहीं मिले: {missing}")
            st.write("आपकी फाइल के असली कॉलम ये हैं:", list(df.columns))
        else:
            # डेटा को क्लीन करना
            for standard_name, file_name in col_map.items():
                df[file_name] = pd.to_numeric(df[file_name], errors='coerce')
            
            df = df.fillna(0)
            st.success("✅ फाइल मैच हो गई! (FD और GD मिल गए)")
            
            target_shift = st.selectbox("किस शिफ्ट का अंक चाहिए?", ['DS', 'FD', 'GD', 'GL'])

            if st.button("Analysis Shuru Karein"):
                scores = {i: 0 for i in range(10)}
                last_row = df.iloc[-1]
                
                # --- STRATEGY 1: GAP ANALYSIS (Last 10 Days) ---
                # केवल गेम वाले कॉलम पर फोकस
                game_cols = ['DS', 'FD', 'GD', 'GL']
                recent_data = df.tail(10)[game_cols].astype(str).values.flatten()
                all_digits = "".join(recent_data)
                for i in range(10):
                    if str(i) not in all_digits:
                        scores[i] += 5 # जो अंक गायब है उसे सबसे ज्यादा पॉइंट
                
                # --- STRATEGY 2: DATE SUM ---
                d_sum = sum(int(d) for d in str(datetime.now().day)) % 10
                scores[d_sum] += 2
                
                # --- STRATEGY 3: MIRROR/UNIT LOGIC ---
                # पिछली शिफ्ट (DS) का आधार
                ds_val = str(int(last_row['DS'])).zfill(2)
                unit_digit = int(ds_val[-1])
                scores[unit_digit] += 3
                scores[(unit_digit + 5) % 10] += 2
                
                # रिजल्ट्स दिखाना
                results = pd.DataFrame(scores.items(), columns=['Ank', 'Score']).sort_values(by='Score', ascending=False)
                
                c1, c2 = st.columns(2)
                with c1:
                    st.metric("🔥 STRONG SINGLE ANK", int(results.iloc[0]['Ank']))
                    st.write("**Top 5 अंकों की लिस्ट:**")
                    st.dataframe(results.head(5), hide_index=True)
                with c2:
                    st.write("**Confidence Score Chart**")
                    st.bar_chart(results.set_index('Ank'))

    except Exception as e:
        st.error(f"Logic Error: {e}")
else:
    st.info("भाई, अपनी CSV फाइल ऊपर अपलोड करो।")
    
