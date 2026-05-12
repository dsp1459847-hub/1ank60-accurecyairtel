import streamlit as st
import pandas as pd
from datetime import datetime

# Page Configuration
st.set_page_config(page_title="MAYA AI - Live Prediction", layout="wide")

st.title("🎯 MAYA Adaptive Super-AI v4.0")
st.write("Ab result turant badlega aur aap purani history bhi verify kar sakte hain.")

uploaded_file = st.file_uploader("अपनी CSV फाइल अपलोड करें", type=["csv"])

if uploaded_file:
    try:
        # 1. Data Loading
        df = pd.read_csv(uploaded_file, skip_blank_lines=True).dropna(how='all')
        df.columns = [str(c).strip().upper() for c in df.columns]
        
        # Column Mapping
        col_map = {'DS': 'DS', 'FB': 'FD', 'GB': 'GD', 'GL': 'GL'}
        game_cols = ['DS', 'FD', 'GD', 'GL']
        
        for col in game_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)

        if 'DATE' in df.columns:
            df['DATE_CLEAN'] = pd.to_datetime(df['DATE'], errors='coerce')
            df = df.dropna(subset=['DATE_CLEAN'])
            
            # --- Sidebar Controls ---
            st.sidebar.header("Control Panel")
            max_dt = df['DATE_CLEAN'].max().date()
            min_dt = df['DATE_CLEAN'].min().date()
            
            sel_date = st.sidebar.date_input("Tarikh Chunein:", value=max_dt, min_value=min_dt, max_value=max_dt)
            target_s = st.sidebar.selectbox("Shift Chunein:", game_cols)

            # Filtering Data
            mask = df['DATE_CLEAN'].dt.date <= sel_date
            f_df = df.loc[mask]
            
            if not f_df.empty:
                current_data = f_df.iloc[-1] # Selected Date ka asli result
                
                # --- SECTION 1: HISTORY VERIFICATION ---
                st.subheader(f"📅 Selected Date History: {sel_date}")
                cols = st.columns(4)
                cols[0].metric("DS Result", current_data['DS'])
                cols[1].metric("FD Result", current_data['FD'])
                cols[2].metric("GD Result", current_data['GD'])
                cols[3].metric("GL Result", current_data['GL'])
                
                st.divider()

                # --- SECTION 2: AUTO-PREDICTION LOGIC ---
                # Jaise hi select hoga, ye calculation apne aap chalegi
                scores = {i: 0 for i in range(10)}
                
                # Dynamic Base Calculation
                if target_s == 'FD': base = current_data['DS']
                elif target_s == 'GD': base = current_data['FD']
                elif target_s == 'GL': base = current_data['GD']
                else: base = current_data['GL']

                u_ank = int(str(base)[-1]) if base > 0 else 0
                scores[u_ank] += 4
                scores[(u_ank + 5) % 10] += 3
                
                # Gap Analysis (Pichle 7 din)
                recent_vals = f_df.tail(7)[game_cols].astype(str).values.flatten()
                all_d = "".join(recent_vals)
                for i in range(10):
                    if str(i) not in all_d: scores[i] += 5
                
                # Results Display
                res = pd.DataFrame(scores.items(), columns=['Ank', 'Score']).sort_values(by='Score', ascending=False)
                
                st.subheader(f"🔮 Prediction for Next {target_s}")
                c1, c2 = st.columns([1, 2])
                with c1:
                    st.success(f"Strongest Ank: {res.iloc[0]['Ank']}")
                    st.write("**Probability Table:**")
                    st.dataframe(res.head(5), hide_index=True)
                with c2:
                    st.bar_chart(res.set_index('Ank'))
            else:
                st.warning("Is tarikh ka data nahi mila.")
        else:
            st.error("File mein 'DATE' column missing hai!")

    except Exception as e:
        st.error(f"Error: {e}")
else:
    st.info("Kripya CSV file upload karein.")
    
