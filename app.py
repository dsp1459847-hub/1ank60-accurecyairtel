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
        # 1. डेटा लोड और क्लीनिंग
        df = pd.read_csv(uploaded_file, skip_blank_lines=True).dropna(how='all')
        df.columns = df.columns.str.strip() # कॉलम के नाम से स्पेस हटाना
        
        required_cols = ['DS', 'FB', 'GB', 'GL']
        
        if not all(col in df.columns for col in required_cols):
            st.error(f"फाइल में ये कॉलम होने चाहिए: {required_cols}")
        else:
            for col in required_cols:
                df[col] = pd.to_numeric(df[col], errors='coerce')
            df = df.fillna(0)
            
            st.success("Data Loaded Successfully!")
            
            target_shift = st.selectbox("Select Target Shift", required_cols)

            if st.button("Run Adaptive Analysis"):
                scores = {i: 0 for i in range(10)}
                last_row = df.iloc[-1]
                
                # --- STRATEGY 1: GAP ANALYSIS ---
                recent_data = df.tail(10).astype(str).values.flatten()
                all_digits = "".join(recent_data)
                for i in range(10):
                    if str(i) not in all_digits:
                        scores[i] += 5
                
                # --- STRATEGY 2: DATE SUM ---
                d_sum = sum(int(d) for d in str(datetime.now().day)) % 10
                scores[d_sum] += 2
                
                # --- STRATEGY 3: MIRROR LOGIC ---
                # पिछली शिफ्ट का डेटा लेना (जैसे GB के लिए FB)
                source_val = str(int(last_row['DS'])).zfill(2)
                unit_digit = int(source_val[-1])
                scores[unit_digit] += 3
                scores[(unit_digit + 5) % 10] += 2
                
                # Results Display
                results = pd.DataFrame(scores.items(), columns=['Ank', 'Score']).sort_values(by='Score', ascending=False)
                
                c1, c2 = st.columns(2)
                with c1:
                    st.metric("🔥 STRONG ANK", results.iloc[0]['Ank'])
                    st.dataframe(results.head(5), hide_index=True)
                with c2:
                    st.bar_chart(results.set_index('Ank'))

    except Exception as e:
        st.error(f"Main Logic Error: {e}")
else:
    st.info("Please upload a CSV file.")
    
