import streamlit as st
import pandas as pd

st.set_page_config(page_title="Satta Predictor", layout="wide")
st.title("🎯 Satta Prediction Tool")
st.markdown("**Upload Excel → Get Predictions Instantly**")

# File Upload
uploaded_file = st.file_uploader("Choose 0DSP0.xlsx", type="xlsx")

if uploaded_file is not None:
    # Load data
    df = pd.read_excel(uploaded_file)
    
    # Clean & Sort
    df['DATE'] = pd.to_datetime(df['DATE'], errors='coerce')
    df = df.sort_values('DATE', ascending=False).head(100)  # Recent 100 days
    
    st.success(f"✅ Loaded {len(df)} records")
    
    # Shifts list
    shifts = ['DS', 'SG', 'FD', 'GD', 'GL', 'DB', 'ZA']
    
    # Predictions
    st.subheader("**🔮 Tomorrow's Predictions**")
    pred_table = []
    
    for shift in shifts:
        if shift in df.columns:
            # Get last 10 values, extract first digit
            recent = df[shift].dropna().head(10).astype(str)
            digits = [x[0] for x in recent if len(x) > 0 and x != 'XX' and x != 'nan']
            
            if len(digits) >= 3:
                from collections import Counter
                top3 = [d for d, _ in Counter(digits).most_common(3)]
                pred_table.append([shift, ', '.join(top3)])
                st.write(f"**{shift}:** {', '.join(top3)}")
            else:
                st.write(f"**{shift}:** Data insufficient")
    
    # Results Table
    st.subheader("**📋 Prediction Summary**")
    pred_df = pd.DataFrame(pred_table, columns=['Shift', 'Top 3 Digits'])
    st.table(pred_df)
    
    # Recent Results
    st.subheader("**📊 Last 10 Days**")
    display_cols = ['DATE'] + [s for s in shifts if s in df.columns][:6]
    st.dataframe(df[display_cols].head(10), use_container_width=True)
    
    # Download
    csv = df[['DATE', 'DS', 'SG', 'FD', 'GD', 'GL', 'DB']].head(30).to_csv(index=False)
    st.download_button("💾 Download CSV", csv, "predictions.csv")

# Sidebar Instructions
st.sidebar.markdown("""
# 🚀 Setup
**Local Run:**
