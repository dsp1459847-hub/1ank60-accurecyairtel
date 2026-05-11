import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")
st.title("🎯 Satta Prediction Tool")

uploaded_file = st.file_uploader("Upload 0DSP0.xlsx", type="xlsx")

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    df['DATE'] = pd.to_datetime(df['DATE'], errors='coerce')
    df = df.sort_values('DATE', ascending=False).head(100)
    
    st.success(f"Loaded {len(df)} records")
    
    shifts = ['DS', 'SG', 'FD', 'GD', 'GL', 'DB']
    st.subheader("Tomorrow's Predictions")
    
    for shift in shifts:
        if shift in df.columns:
            recent = df[shift].dropna().head(10).astype(str)
            digits = []
            for x in recent:
                if len(x) > 0 and x not in ['XX', 'nan']:
                    digits.append(x[0])
            
            if len(digits) >= 2:
                from collections import Counter
                top3 = [d for d, c in Counter(digits).most_common(3)]
                st.markdown(f"**{shift}:** {', '.join(top3)}")
    
    # Last 10 days
    st.subheader("Last 10 Days")
    cols = ['DATE', 'DS', 'SG', 'FD', 'GD', 'GL', 'DB']
    show_df = df[cols].head(10).fillna('XX')
    st.dataframe(show_df)
    
    # Download
    csv = df[['DATE','DS','SG','FD','GD','GL','DB']].head(30).to_csv(index=False)
    st.download_button("Download CSV", csv, "predictions.csv")

st.sidebar.markdown("## Setup
**Local:** pip install streamlit pandas openpyxl
**Run:** streamlit run app.py")
