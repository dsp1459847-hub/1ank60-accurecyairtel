import streamlit as st
import pandas as pd

# Page Setup
st.set_page_config(page_title="MAYA AI - Prediction Fix", layout="wide")

st.title("🎯 MAYA Adaptive Super-AI v4.7 (Final Fixed)")

uploaded_file = st.file_uploader("अपनी CSV फाइल अपलोड करें", type=["csv"])

if uploaded_file:
    try:
        # 1. डेटा लोड और कॉलम फिक्स (DS, FD, GD, GL)
        df = pd.read_csv(uploaded_file, skip_blank_lines=True).dropna(how='all')
        df.columns = [str(c).strip().upper() for c in df.columns]
        
        game_cols = ['DS', 'FD', 'GD', 'GL']
        for col in game_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)

        if 'DATE' in df.columns:
            # तारीखों की लिस्ट (Latest first)
            date_list = df['DATE'].unique().tolist()[::-1]
            
            st.markdown("### 📅 तारीख और शिफ्ट चुनें")
            c_date, c_shift = st.columns(2)
            
            with c_date:
                sel_date = st.selectbox("तारीख चुनें:", options=date_list)
            
            with c_shift:
                target_s = st.selectbox("किस शिफ्ट का अंक चाहिए?", game_cols)

            # डेटा फिल्टर करना (चुनी हुई तारीख का इंडेक्स)
            idx = df[df['DATE'] == sel_date].index[0]
            f_df = df.iloc[:idx + 1]
            current_data = df.iloc[idx] 

            # --- HISTORY DISPLAY (ऊपर) ---
            st.info(f"🕒 {sel_date} के वास्तविक नतीजे (Records)")
            h1, h2, h3, h4 = st.columns(4)
            h1.metric("DS Result", current_data['DS'])
            h2.metric("FD Result", current_data['FD'])
            h3.metric("GD Result", current_data['GD'])
            h4.metric("GL Result", current_data['GL'])
            
            st.divider()

            # --- 🛠️ CORRECTED PREDICTION LOGIC 🛠️ ---
            scores = {i: 0 for i in range(10)}
            
            # सही शिफ्ट मैपिंग (Shift-to-Shift Connection)
            if target_s == 'FD':
                # फरीदाबाद के लिए पिछला 'देसावर' देखो
                base_val = current_data['DS']
            elif target_s == 'GD':
                # गाजियाबाद के लिए आज का 'फरीदाबाद' देखो
                base_val = current_data['FD']
            elif target_s == 'GL':
                # गली के लिए आज का 'गाजियाबाद' देखो
                base_val = current_data['GD']
            elif target_s == 'DS':
                # देसावर के लिए पिछली 'गली' देखो
                base_val = current_data['GL']
            else:
                base_val = 0

            # अंक निकालना (Last Digit)
            u_ank = int(str(base_val)[-1]) if base_val > 0 else 0
            scores[u_ank] += 4          # सीधा अंक को 4 पॉइंट
            scores[(u_ank + 5) % 10] += 3 # राशि को 3 पॉइंट
            
            # गैप एनालिसिस (पिछले 7 रिकॉर्ड्स)
            all_recent = f_df.tail(7)[game_cols].astype(str).values.flatten()
            digits_pool = "".join(all_recent)
            for i in range(10):
                if str(i) not in digits_pool:
                    scores[i] += 5 # गायब अंक को सबसे ज्यादा पावर

            # रिजल्ट सॉर्टिंग
            res = pd.DataFrame(scores.items(), columns=['Ank', 'Score']).sort_values(by='Score', ascending=False)
            
            # डिस्प्ले
            st.subheader(f"🔮 {target_s} प्रेडिक्शन रिपोर्ट")
            r1, r2 = st.columns([1, 2])
            with r1:
                st.success(f"Strongest Single: {int(res.iloc[0]['Ank'])}")
                st.write("**टॉप प्रोबेबिलिटी अंक:**")
                st.dataframe(res.head(5), hide_index=True)
            with r2:
                st.bar_chart(res.set_index('Ank'))
        else:
            st.error("फाइल में 'DATE' कॉलम नहीं मिला!")

    except Exception as e:
        st.error(f"Error: {e}")
else:
    st.info("भाई, अपनी फाइल ऊपर अपलोड करो!")
    
