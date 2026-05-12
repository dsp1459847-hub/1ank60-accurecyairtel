import streamlit as st
import pandas as pd

# Page Setup
st.set_page_config(page_title="MAYA AI - History & Prediction", layout="wide")

st.title("🎯 MAYA Adaptive Super-AI v4.5")

uploaded_file = st.file_uploader("अपनी CSV फाइल अपलोड करें", type=["csv"])

if uploaded_file:
    try:
        # 1. डेटा लोड करना
        df = pd.read_csv(uploaded_file, skip_blank_lines=True).dropna(how='all')
        df.columns = [str(c).strip().upper() for c in df.columns]
        
        # कॉलम पहचान: FD, GD, DS, GL
        col_map = {'DS': 'DS', 'FB': 'FD', 'GB': 'GD', 'GL': 'GL'}
        game_cols = ['DS', 'FD', 'GD', 'GL']
        
        # नंबरों को साफ करना
        for col in game_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)

        # --- तारीख को फिक्स करना (Critical Step) ---
        if 'DATE' in df.columns:
            # तारीख को साफ़ सुथरा करना
            df['DATE'] = df['DATE'].astype(str).str.strip()
            all_dates = df['DATE'].unique().tolist()
            
            # --- UI CONTROLS ---
            st.sidebar.header("Settings")
            # ड्रॉपडाउन ताकि तारीख गलत होने का चांस ही न रहे
            sel_date = st.sidebar.selectbox("तारीख चुनें (History के लिए):", options=all_dates[::-1])
            target_s = st.sidebar.selectbox("किस शिफ्ट का अंक निकालें?", game_cols)

            # डेटा फिल्टर (चुनी हुई तारीख तक)
            idx = df[df['DATE'] == sel_date].index[0]
            f_df = df.iloc[:idx + 1]
            current_data = df.iloc[idx] # चुनी हुई तारीख का असली रिजल्ट

            # --- SECTION 1: HISTORY DISPLAY ---
            st.markdown(f"### 🕒 तारीख {sel_date} का असली रिजल्ट (History)")
            h1, h2, h3, h4 = st.columns(4)
            h1.metric("DS", current_data['DS'])
            h2.metric("FD", current_data['FD'])
            h3.metric("GD", current_data['GD'])
            h4.metric("GL", current_data['GL'])
            
            st.divider()

            # --- SECTION 2: AUTO-CALCULATION ---
            scores = {i: 0 for i in range(10)}
            
            # पिछली शिफ्ट का बेस (FD के लिए DS, GD के लिए FD...)
            if target_s == 'FD': base = current_data['DS']
            elif target_s == 'GD': base = current_data['FD']
            elif target_s == 'GL': base = current_data['GD']
            else: base = current_data['GL']

            u_ank = int(str(base)[-1]) if base > 0 else 0
            scores[u_ank] += 4
            scores[(u_ank + 5) % 10] += 3
            
            # गैप एनालिसिस (पिछले 7 रिकॉर्ड)
            recent_vals = f_df.tail(7)[game_cols].astype(str).values.flatten()
            all_d = "".join(recent_vals)
            for i in range(10):
                if str(i) not in all_d: scores[i] += 5
            
            # रिजल्ट डिस्प्ले
            res = pd.DataFrame(scores.items(), columns=['Ank', 'Score']).sort_values(by='Score', ascending=False)
            
            st.subheader(f"🔮 {target_s} के लिए प्रेडिक्शन")
            c1, c2 = st.columns([1, 2])
            with c1:
                st.success(f"सबसे मजबूत अंक: {res.iloc[0]['Ank']}")
                st.write("**टॉप 5 अंक स्कोर:**")
                st.dataframe(res.head(5), hide_index=True)
            with c2:
                st.bar_chart(res.set_index('Ank'))
        else:
            st.error("आपकी फाइल में 'DATE' नाम का कॉलम नहीं मिल रहा है!")

    except Exception as e:
        st.error(f"गड़बड़ हुई: {e}")
else:
    st.info("भाई, ऊपर फाइल अपलोड करो, फिर देखो जादू!")
    
