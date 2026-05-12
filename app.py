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
        # 1. Data load and cleaning
        df = pd.read_csv(uploaded_file, skip_blank_lines=True).dropna(how='all')
        
        # Column names ko saaf karna (spaces hatana aur Capitalize karna)
        df.columns = [str(c).strip().upper() for c in df.columns]
        
        # Check for possible column matches
        required_cols = ['DS', 'FB', 'GB', 'GL']
        
        # Agar file mein columns mil gaye
        found_cols = [col for col in required_cols if col in df.columns]
        
        if len(found_cols) < 4:
            st.error(f"Error: File mein ye columns nahi mile: {list(set(required_cols) - set(found_cols))}")
            st.info("Kripya Excel ki pehli line check karein wahan DS, FB, GB, GL likha hona chahiye.")
        else:
            for col in required_cols:
                df[col] = pd.to_numeric(df[col], errors='coerce')
            df = df.fillna(0)
            
            st.success("File Verified! Data Match Ho Gaya.")
            
            target_shift = st.selectbox("Shift Chunein:", required_cols)

            if st.button("Analysis Shuru Karein"):
                scores = {i: 0 for i in range(10)}
                last_row = df.iloc[-1]
                
                # --- STRATEGY 1: GAP ANALYSIS ---
                recent_data = df.tail(10)[required_cols].astype(str).values.flatten()
                all_digits = "".join(recent_data)
                for i in range(10):
                    if str(i) not in all_digits:
                        scores[i] += 5
                
                # --- STRATEGY 2: DATE SUM ---
                d_sum = sum(int(d) for d in str(datetime.now().day)) % 10
                scores[d_sum] += 2
                
                # --- STRATEGY 3: MIRROR LOGIC ---
                source_val = str(int(last_row['DS'])).zfill(2)
                unit_digit = int(source_val[-1])
                scores[unit_digit] += 3
                scores[(unit_digit + 5) % 10] += 2
                
                # Results Display
                results = pd.DataFrame(scores.items(), columns=['Ank', 'Score']).sort_values(by='Score', ascending=False)
                
                c1, c2 = st.columns(2)
                with c1:
                    st.metric("🔥 STRONG ANK", int(results.iloc[0]['Ank']))
                    st.write("**Top 5 Probability:**")
                    st.dataframe(results.head(5), hide_index=True)
                with c2:
                    st.write("**Confidence Chart**")
                    st.bar_chart(results.set_index('Ank'))

    except Exception as e:
        st.error(f"Logic Error: {e}")
else:
    st.info("Kripya Prediction CSV file upload karein.")
    
