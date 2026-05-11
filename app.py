import streamlit as st
import pandas as pd

st.title("Satta Predictor")

# File upload
file = st.file_uploader("0DSP0.xlsx", type="xlsx")

if file:
    df = pd.read_excel(file)
    df = df.sort_values('DATE', ascending=False).head(50)
    
    st.write("Predictions:")
    
    shifts = ['DS', 'SG', 'FD', 'GD', 'GL', 'DB']
    
    for shift in shifts:
        if shift in df.columns:
            data = df[shift].dropna().head(10)
            digits = []
            for val in data:
                s = str(val)
                if len(s) > 0 and s != 'XX':
                    digits.append(s[0])
            
            if len(digits) > 1:
                counts = {}
                for d in digits:
                    if d in counts:
                        counts[d] += 1
                    else:
                        counts[d] = 1
                
                top = sorted(counts, key=counts.get, reverse=True)[:3]
                st.write(f"{shift}: {', '.join(top)}")
    
    # Show recent data
    st.write("Recent Data:")
    st.dataframe(df[['DATE','DS','SG','FD']].head(10))
    
    # Download
    csv = df[['DATE','DS','SG']].to_csv(index=False)
    st.download_button("CSV", csv, "data.csv")

st.sidebar.write("Upload file to start")
