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
        
        # Column names ko clean karna
        df.columns = [str(c).strip().upper() for c in df.columns]
        
        # --- SMART COLUMN MAPPING ---
        # Agar file mein exact 'FB' nahi hai, toh milte julte naam dhoondna
        def find_col(target, options):
            for opt in options:
                if target in opt or opt in target:
                    return opt
            return None

        col_map = {
            'DS': find_col('DS', df.columns) or find_col('DESAWAR', df.columns),
            'FB': find_col('FB', df.columns) or find_col('FARIDABAD', df.columns),
            'GB': find_col('GB', df.columns) or find_col('GHAZIABAD', df.columns),
            'GL': find_col('GL', df.columns) or find_col('GALI', df.columns)
        }

        # Check if all required mappings found
        missing = [k for k, v in col_map.items() if v is None]
        
        if missing:
            st.error(f"Error: File mein ye data nahi mila: {missing}")
            st.info("Kripya check karein ki aapki CSV ki pehli line mein shifts ke naam sahi hain.")
            st.write("Aapki file ke columns:", list(df.columns))
        else:
            # Rename columns to standard names for logic
            df = df.rename(columns={v: k for k, v in col_map.items()})
            
            for col in ['DS', 'FB', 'GB', 'GL']:
                df[col] = pd.to_numeric(df[col], errors='coerce')
            df = df.fillna(0)
            
            st.success("File Verified! Data Match Ho Gaya.")
            
            target_shift = st.selectbox("Shift Chunein:", ['DS', 'FB', 'GB', 'GL'])

            if st.button("Analysis Shuru Karein"):
                scores = {i: 0 for i in range(10)}
                last_row = df.iloc[-1]
                
                # --- STRATEGY: GAP ANALYSIS ---
                recent_data = df.tail(10)[['DS', 'FB', 'GB', 'GL']].astype(str).values.flatten()
                all_digits = "".join(recent_data)
                for i in range(10):
                    if str(i) not in all_digits:
                        scores[i] += 5
                
                # --- STRATEGY: DATE SUM ---
                d_sum = sum(int(d) for d in str(datetime.now().day)) % 10
                scores[d_sum] += 2
                
                # --- STRATEGY: MIRROR LOGIC ---
                # Default source DS for all
                source_val = str(int(last_row['DS'])).zfill(2)
                unit_digit = int(source_val[-1])
                scores[unit_digit] += 3
                scores[(unit_digit + 5) % 10] += 2
                
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
    
