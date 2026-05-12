import streamlit as st
import pandas as pd
from datetime import datetime

# Page Setup
st.set_page_config(page_title="MAYA Adaptive Super-AI", layout="wide")

st.title("🎯 MAYA Adaptive Super-AI v3.5")
st.write("Ab aap tarikh chunkar us din ki prediction nikal sakte hain.")

uploaded_file = st.file_uploader("Upload your Prediction CSV", type=["csv"])

if uploaded_file:
    try:
        # 1. Data Load
        df = pd.read_csv(uploaded_file, skip_blank_lines=True).dropna(how='all')
        df.columns = [str(c).strip().upper() for c in df.columns]
        
        # Columns identify karna
        col_map = {'DS': 'DS', 'FB': 'FD', 'GB': 'GD', 'GL': 'GL'}
        game_cols = ['DS', 'FD', 'GD', 'GL']
        
        for col in game_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)

        # Date column ko format karna taaki calendar kaam kare
        if 'DATE' in df.columns:
            df['DATE_CLEAN'] = pd.to_datetime(df['DATE'], errors='coerce')
            df = df.dropna(subset=['DATE_CLEAN'])
            
            # --- DATE SELECTION UI ---
            min_date = df['DATE_CLEAN'].min().date()
            max_date = df['DATE_CLEAN'].max().date()
            
            selected_date = st.date_input("Koshish karein ki pichli dates chunein jinka data file mein hai:", 
                                         value=max_date, 
                                         min_value=min_date, 
                                         max_value=max_date)

            # Selected Date tak ka data filter karna
            mask = df['DATE_CLEAN'].dt.date <= selected_date
            filtered_df = df.loc[mask]
            
            if not filtered_df.empty:
                st.info(f"📅 Selected Date: {selected_date} | Records Found: {len(filtered_df)}")
                
                target_shift = st.selectbox("Shift Chunein:", game_cols)

                if st.button("Run Prediction"):
                    scores = {i: 0 for i in range(10)}
                    current_row = filtered_df.iloc[-1] # Chuni hui tarikh ka data
                    
                    # --- DYNAMIC LOGIC BASED ON SHIFT ---
                    # Logic: Target shift ke liye usse pehle wali shift ka unit ank base banega
                    if target_shift == 'FD': source_val = current_row['DS']
                    elif target_shift == 'GD': source_val = current_row['FD']
                    elif target_shift == 'GL': source_val = current_row['GD']
                    else: source_val = current_row['GL'] # DS ke liye GL

                    source_unit = int(str(source_val)[-1]) if source_val > 0 else 0
                    scores[source_unit] += 4  # Direct follow point
                    scores[(source_unit + 5) % 10] += 3  # Rashi/Mirror point
                    
                    # --- GAP ANALYSIS (Selected Date se pichle 7 records) ---
                    recent_data = filtered_df.tail(7)[game_cols].astype(str).values.flatten()
                    all_digits = "".join(recent_data)
                    for i in range(10):
                        if str(i) not in all_digits:
                            scores[i] += 5 # Gap factor
                    
                    # Date Total Logic
                    d_sum = (selected_date.day) % 10
                    scores[d_sum] += 2

                    results = pd.DataFrame(scores.items(), columns=['Ank', 'Score']).sort_values(by='Score', ascending=False)
                    
                    c1, c2 = st.columns(2)
                    with c1:
                        st.metric(f"🔥 {target_shift} STRONG", int(results.iloc[0]['Ank']))
                        st.write("**Probability Rankings:**")
                        st.dataframe(results.head(5), hide_index=True)
                    with c2:
                        st.bar_chart(results.set_index('Ank'))
            else:
                st.warning("Is tarikh ka data file mein nahi mila.")
        else:
            st.error("File mein 'DATE' column nahi mila. Date selection ke liye column hona zaroori hai.")

    except Exception as e:
        st.error(f"Logic Error: {e}")
else:
    st.info("Kripya file upload karein taaki AI tarikh pehchan sake.")
    
