import streamlit as st
import pandas as pd
from datetime import datetime

# Page Configuration
st.set_page_config(page_title="MAYA AI - Prediction Dashboard", layout="wide")

st.title("📊 Numerical Forecasting Dashboard")
st.subheader("Data-Driven Single Ank Prediction")

# File Upload Section
uploaded_file = st.file_uploader("अपनी एक्सेल (CSV) फाइल अपलोड करें", type=["csv"])

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        st.success("फाइल सफलतापूर्वक लोड हो गई!")
        
        # डेटा प्रिव्यू
        with st.expander("Raw Data देखें"):
            st.write(df.tail(10))

        # शिफ्ट सिलेक्शन
        shift = st.selectbox("किस शिफ्ट के लिए अंक चाहिए?", ["DS", "FB", "GB", "GL"])

        if st.button("Generate Prediction"):
            # लॉजिक प्रोसेसिंग
            last_row = df.iloc[-1]
            scores = {i: 0 for i in range(10)}

            # 1. Gap Analysis (Last 10 days)
            last_10_str = df.tail(10).to_string()
            for i in range(10):
                if str(i) not in last_10_str:
                    scores[i] += 4  # Gap अंक को सबसे ज्यादा प्राथमिकता

            # 2. Date Sum Logic
            today_date = datetime.now().day
            d_sum = sum(int(d) for d in str(today_date)) % 10
            scores[d_sum] += 2

            # 3. Mirror/Unit Logic (From Previous DS)
            ds_val = str(last_row['DS']).zfill(2)
            ds_units = int(ds_val[1])
            scores[ds_units] += 3  # Last digit follow
            scores[(ds_units + 5) % 10] += 2 # Family/Mirror

            # 4. Cross-Shift Heat
            recent_results = str(last_row['FB']) + str(last_row['GB']) + str(last_row['GL'])
            for i in range(10):
                if str(i) in recent_results:
                    scores[i] += 1

            # परिणाम दिखाना
            sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric(label="🔥 STRONG SINGLE ANK", value=sorted_scores[0][0])
            with col2:
                st.metric(label="Support 1", value=sorted_scores[1][0])
            with col3:
                st.metric(label="Support 2", value=sorted_scores[2][0])

            # स्कोर चार्ट
            st.write("### Prediction Confidence Score")
            chart_data = pd.DataFrame(scores.items(), columns=['Ank', 'Score']).set_index('Ank')
            st.bar_chart(chart_data)

    except Exception as e:
        st.error(f"Error: फाइल फॉर्मेट चेक करें। सुनिश्चित करें कि कॉलम के नाम DS, FB, GB, GL हैं। | {e}")

else:
    st.info("कृपया डेटा प्रोसेस करने के लिए अपनी CSV फाइल अपलोड करें।")
    
