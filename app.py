import streamlit as st
import pandas as pd

# Page Setup
st.set_page_config(page_title="MAYA AI - Date Wise Prediction", layout="wide")

st.title("🎯 MAYA Adaptive Super-AI v4.6")

uploaded_file = st.file_uploader("अपनी CSV फाइल अपलोड करें", type=["csv"])

if uploaded_file:
    try:
        # 1. डेटा लोड करना
        df = pd.read_csv(uploaded_file, skip_blank_lines=True).dropna(how='all')
        df.columns = [str(c).strip().upper() for c in df.columns]
        
        # आपकी फाइल के कॉलम्स: DS, FD, GD, GL
        game_cols = ['DS', 'FD', 'GD', 'GL']
        
        # नंबरों को क्लीन करना
        for col in game_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)

        # --- DATE SELECTION OPTION ---
        if 'DATE' in df.columns:
            # तारीखों की लिस्ट बनाना (उल्टे क्रम में ताकि ताज़ा तारीख सबसे ऊपर हो)
            date_list = df['DATE'].unique().tolist()[::-1]
            
            st.markdown("### 📅 तारीख और शिफ्ट चुनें")
            c_date, c_shift = st.columns(2)
            
            with c_date:
                # यहाँ आएगा तारीख चुनने का ऑप्शन
                sel_date = st.selectbox("तारीख चुनें:", options=date_list)
            
            with c_shift:
                target_s = st.selectbox("शिफ्ट चुनें:", game_cols)

            # चुनी हुई तारीख का इंडेक्स निकालकर डेटा फिल्टर करना
            idx = df[df['DATE'] == sel_date].index[0]
            f_df = df.iloc[:idx + 1]
            current_data = df.iloc[idx] 

            # --- HISTORY DISPLAY ---
            st.info(f"🕒 {sel_date} के असली रिजल्ट्स")
            h1, h2, h3, h4 = st.columns(4)
            h1.metric("DS", current_data['DS'])
            h2.metric("FD", current_data['FD'])
            h3.metric("GD", current_data['GD'])
            h4.metric("GL", current_data['GL'])
            
            st.divider()

            # --- PREDICTION LOGIC ---
            scores = {i: 0 for i in range(10)}
            
            # बेस अंक चुनना
            if target_s == 'FD': base = current_data['DS']
            elif target_s == 'GD': base = current_data['FD']
            elif target_s == 'GL': base = current_data['GD']
            else: base = current_data['GL']

            u_ank = int(str(base)[-1]) if base > 0 else 0
            scores[u_ank] += 4
            scores[(u_ank + 5) % 10] += 3
            
            # गैप एनालिसिस
            recent_vals = f_df.tail(7)[game_cols].astype(str).values.flatten()
            all_digits = "".join(recent_vals)
            for i in range(10):
                if str(i) not in all_digits: scores[i] += 5
            
            # रिजल्ट दिखाना
            res = pd.DataFrame(scores.items(), columns=['Ank', 'Score']).sort_values(by='Score', ascending=False)
            
            st.subheader(f"🔮 {target_s} प्रेडिक्शन")
            res_col1, res_col2 = st.columns([1, 2])
            with res_col1:
                st.success(f"सबसे मजबूत अंक: {res.iloc[0]['Ank']}")
                st.write("**स्कोर टेबल:**")
                st.dataframe(res.head(5), hide_index=True)
            with res_col2:
                st.bar_chart(res.set_index('Ank'))
        else:
            st.error("फाइल में 'DATE' कॉलम नहीं मिला। अपनी एक्सेल की पहली लाइन चेक करें।")

    except Exception as e:
        st.error(f"Logic Error: {e}")
else:
    st.info("भाई, पहले ऊपर फाइल अपलोड करो, तभी तारीख चुनने का ऑप्शन आएगा!")
    
