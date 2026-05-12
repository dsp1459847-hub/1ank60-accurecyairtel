import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

# Page Setup
st.set_page_config(page_title="MAYA Adaptive Super-AI", page_icon="🎯", layout="wide")

# Custom CSS for Professional Look
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_allow_html=True)

st.title("🎯 MAYA Adaptive Super-AI v2.0")
st.write("Numerical Forecasting with Pattern Convergence Logic")

# Sidebar for Configuration
st.sidebar.header("AI Configuration")
lookback_days = st.sidebar.slider("Lookback Period (Days)", 5, 30, 10)
confidence_threshold = st.sidebar.slider("Confidence Boost", 1, 5, 3)

# File Upload
uploaded_file = st.file_uploader("Upload your Prediction Excel (CSV)", type=["csv"])

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)
        # Ensure numeric data
        for col in ['DS', 'FB', 'GB', 'GL']:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        df = df.dropna()
        st.success(f"Loaded {len(df)} records. Analyzing patterns...")

        target_shift = st.selectbox("Select Target Shift", ["DS", "FB", "GB", "GL"])

        if st.button("Run Adaptive Analysis"):
            # Logic Engine
            scores = {i: 0 for i in range(10)}
            last_row = df.iloc[-1]
            
            # 1. GAP ANALYSIS (The "Missing Ank" Rule)
            recent_data = df.tail(lookback_days).values.flatten().astype(str)
            all_digits = "".join(recent_data)
            for i in range(10):
                if str(i) not in all_digits:
                    scores[i] += 5  # Highest weight for long-term gaps
                elif all_digits.count(str(i)) < 2:
                    scores[i] += 2 # Low frequency boost

            # 2. ADAPTIVE CROSS-SHIFT (Current Day Flow)
            current_day_str = str(last_row.values)
            for i in range(10):
                if str(i) in current_day_str:
                    scores[i] += confidence_threshold # User-defined boost

            # 3. DATE-TIME CONVERGENCE
            d_sum = sum(int(d) for d in str(datetime.now().day)) % 10
            scores[d_sum] += 2
            
            # 4. MIRROR REFLECTION
            # If target is GB, look at DS; if target is GL, look at GB
            source_map = {"GB": "DS", "GL": "GB", "FB": "DS", "DS": "GL"}
            source_val = str(int(last_row[source_map[target_shift]])).zfill(2)
            unit_digit = int(source_val[-1])
            mirror_digit = (unit_digit + 5) % 10
            
            scores[unit_digit] += 3
            scores[mirror_digit] += 2

            # Processing Results
            results = pd.DataFrame(scores.items(), columns=['Ank', 'Score']).sort_values(by='Score', ascending=False)
            top_ank = results.iloc[0]['Ank']
            
            # UI Display
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.metric("🔥 STRONG SINGLE", f"{top_ank}", f"Score: {results.iloc[0]['Score']}")
                st.write("---")
                st.write("**Top Recommendations:**")
                st.dataframe(results.head(4), hide_index=True)

            with col2:
                st.write("### Pattern Distribution")
                st.bar_chart(results.set_index('Ank'))

            st.info(f"AI Logic: आधारित है {source_map[target_shift]} -> {target_shift} क्रॉस-फ्लो और {lookback_days} दिनों के गैप एनालिसिस पर।")

    except Exception as e:
        st.error(f"Error analyzing data: {e}")
else:
    st.warning("Please upload a CSV file to begin.")
    
