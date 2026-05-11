import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")
st.title("🎯 Satta Predictor - Full Control")

# File upload
file = st.file_uploader("Upload Excel", type="xlsx")

if file:
    df = pd.read_excel(file)
    df['DATE'] = pd.to_datetime(df['DATE'], errors='coerce')
    df = df.dropna(subset=['DATE']).sort_values('DATE')
    
    st.success(f"✅ {len(df)} days loaded")
    
    # Controls
    st.header("⚙️ Select Options")
    col1, col2 = st.columns(2)
    
    with col1:
        days_back = st.selectbox("Days Back", [7, 15, 30, 60, 90])
        shift = st.selectbox("Shift", ['DS', 'SG', 'FD', 'GD', 'GL', 'DB'])
    
    with col2:
        start_date = st.date_input("Start Date", df['DATE'].min())
        end_date = st.date_input("End Date", df['DATE'].max())
    
    # Filter data
    mask = (df['DATE'] >= pd.to_datetime(start_date)) & (df['DATE'] <= pd.to_datetime(end_date))
    filtered_df = df[mask].tail(days_back)
    
    st.subheader(f"**Prediction for {shift}** (Last {days_back} days)")
    
    # Get digits
    data = filtered_df[shift].dropna().astype(str)
    digits = []
    for val in data:
        if len(val) > 0 and val != 'XX':
            digits.append(val[0])
    
    if len(digits) >= 3:
        # Count manually
        count_dict = {}
        for d in digits:
            if d.isdigit():
                count_dict[d] = count_dict.get(d, 0) + 1
        
        # Top 3
        sorted_digits = sorted(count_dict, key=count_dict.get, reverse=True)
        st.success(f"**Top Prediction: {sorted_digits[0]}**")
        st.info(f"Top 3: **{', '.join(sorted_digits[:3])}**")
        st.write(f"From {len(digits)} results | Frequency: {count_dict[sorted_digits[0]]}")
    
    # Backtest
    st.subheader("**Backtest Results**")
    if len(filtered_df) > 10:
        hits = 0
        total = 0
        
        for i in range(10, len(filtered_df)):
            train_data = filtered_df[shift].dropna().head(i).astype(str)
            train_digits = [s[0] for s in train_data if len(s)>0 and s!='XX']
            
            test_val = str(filtered_df[shift].iloc[i])
            if len(test_val)>0 and test_val!='XX':
                test_digit = test_val[0]
                if len(train_digits) > 3:
                    train_count = {}
                    for d in train_digits[-10:]:
                        train_count[d] = train_count.get(d, 0) + 1
                    pred = max(train_count, key=train_count.get)
                    if test_digit == pred:
                        hits += 1
                    total += 1
        
        if total > 0:
            acc = (hits/total)*100
            st.metric("Accuracy", f"{acc:.1f}% ({hits}/{total})")
    
    # Quick predictions all shifts
    st.subheader("**All Shifts Quick View**")
    pred_row = st.columns(6)
    all_shifts = ['DS', 'SG', 'FD', 'GD', 'GL', 'DB']
    
    for i, s in enumerate(all_shifts):
        if s in filtered_df.columns:
            data = filtered_df[s].dropna().head(10).astype(str)
            digs = [x[0] for x in data if len(x)>0 and x!='XX']
            if digs:
                top = max(set(digs), key=digs.count)
                with pred_row[i]:
                    st.markdown(f"**{s}<br><span style='font-size:2em;color:green'>{top}</span>**", unsafe_allow_html=True)
    
    # Data preview
    st.subheader("**Recent Data**")
    cols = ['DATE'] + [s for s in all_shifts if s in df.columns][:4]
    st.dataframe(filtered_df[cols].head(10))
    
    # Download
    csv = filtered_df[['DATE', 'DS', 'SG', 'FD']].to_csv(index=False)
    st.download_button("📥 Download CSV", csv, "predictions.csv")

# Sidebar
st.sidebar.header("Controls")
st.sidebar.markdown("""
- **Days**: Analysis period
- **Shift**: Focus prediction  
- **Dates**: Custom range
- **Backtest**: Live accuracy
""")
