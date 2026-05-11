import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")
st.title("🎯 Satta Predictor Pro")

# File upload
file = st.file_uploader("Upload 0DSP0.xlsx")

if file:
    df = pd.read_excel(file)
    df['DATE'] = pd.to_datetime(df['DATE'], errors='coerce')
    df = df.dropna(subset=['DATE']).sort_values('DATE')
    
    st.success(f"Loaded {len(df)} days")
    
    # Sidebar controls
    st.sidebar.header("⚙️ Controls")
    days_back = st.sidebar.slider("Days for Analysis", 7, 90, 30)
    shift = st.sidebar.selectbox("Select Shift", ['DS', 'SG', 'FD', 'GD', 'GL', 'DB'])
    
    # Filter data
    recent_df = df.tail(days_back)
    
    # Prediction for selected shift
    st.header(f"🔮 {shift} Predictions")
    
    data = recent_df[shift].dropna().head(20).astype(str)
    digits = [s[0] for s in data if len(s)>0 and s!='XX']
    
    if len(digits) > 3:
        # Count digits
        counts = {}
        for d in digits:
            if d.isdigit():
                counts[d] = counts.get(d, 0) + 1
        
        # Top 5
        top_digits = sorted(counts, key=counts.get, reverse=True)[:5]
        st.markdown(f"**Top Prediction: {top_digits[0]}**")
        st.write(f"Top 5: **{', '.join(top_digits)}**")
        st.write(f"Based on last {len(digits)} results")
    
    # Backtest
    st.header("📊 Backtest")
    if len(recent_df) > 10:
        test_results = []
        for i in range(10, len(recent_df)):
            train_digits = [s[0] for s in recent_df[shift].dropna().head(i).astype(str) if len(str(s))>0 and str(s)!='XX']
            test_digit = str(recent_df[shift].iloc[i])[0] if len(str(recent_df[shift].iloc[i]))>0 else 'X'
            
            if len(train_digits) > 3 and test_digit.isdigit():
                train_counts = {}
                for d in train_digits[-10:]:
                    train_counts[d] = train_counts.get(d, 0) + 1
                pred_top = sorted(train_counts, key=train_counts.get, reverse=True)[0]
                hit = test_digit == pred_top
                test_results.append({'Date': recent_df['DATE'].iloc[i], 'Actual': test_digit, 'Predicted': pred_top, 'Hit': hit})
        
        if test_results:
            bt_df = pd.DataFrame(test_results)
            accuracy = bt_df['Hit'].mean() * 100
            st.metric("Accuracy", f"{accuracy:.1f}%")
            st.dataframe(bt_df.tail(10))
    
    # All shifts quick view
    st.header("Quick All Shifts")
    cols = st.columns(3)
    all_shifts = ['DS', 'SG', 'FD', 'GD']
    for i, s in enumerate(all_shifts):
        with cols[i]:
            data = recent_df[s].dropna().head(10).astype(str)
            digits = [x[0] for x in data if len(x)>0 and x!='XX']
            if digits:
                top = max(set(digits), key=digits.count)
                st.markdown(f"**{s}: {top}**")
    
    # Download
    csv = recent_df[['DATE', 'DS', 'SG', 'FD', 'GD']].to_csv(index=False)
    st.download_button("Download Data", csv, "data.csv")

st.sidebar.markdown("""
**Features:**
- Date range selector
- Shift selector  
- Live backtest
- Top predictions
- CSV export

**Usage:**
1. Upload Excel
2. Select days/shift
3. See predictions + accuracy
""")
