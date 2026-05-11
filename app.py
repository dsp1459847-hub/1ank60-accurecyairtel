import streamlit as st
import pandas as pd

st.title("📅 Date Wise Prediction")

# File upload
uploaded_file = st.file_uploader("0DSP0.xlsx", type="xlsx")

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    df['DATE'] = pd.to_datetime(df['DATE'], errors='coerce')
    df = df.dropna(subset=['DATE']).sort_values('DATE')
    
    st.success(f"Loaded {len(df)} days")
    
    # Date selector
    selected_date = st.date_input("Select Date for Prediction", df['DATE'].max())
    
    # Find closest past dates for pattern
    target_date = pd.to_datetime(selected_date)
    past_data = df[df['DATE'] < target_date].tail(30)  # Last 30 days before selected date
    
    st.header(f"Prediction for {selected_date.strftime('%d-%m-%Y')}")
    
    # Shifts
    shifts = ['DS', 'SG', 'FD', 'GD', 'GL', 'DB']
    
    predictions = {}
    
    for shift in shifts:
        if shift in df.columns:
            # Pattern from past 30 days
            recent_shift = past_data[shift].dropna().astype(str)
            first_digits = []
            for val in recent_shift:
                if len(str(val)) >= 1 and str(val) != 'XX':
                    first_digits.append(str(val)[0])
            
            if len(first_digits) > 5:
                # Most common pattern
                count = {}
                for d in first_digits:
                    count[d] = count.get(d, 0) + 1
                
                top_digit = max(count, key=count.get)
                predictions[shift] = top_digit
                st.write(f"**{shift}: {top_digit}** (from {count[top_digit]} repeats)")
    
    # Show prediction table
    if predictions:
        pred_df = pd.DataFrame(list(predictions.items()), columns=['Shift', 'Predicted Digit'])
        st.table(pred_df)
    
    # Show actual result (if date exists)
    actual_row = df[df['DATE'] == target_date]
    if not actual_row.empty:
        st.header("Actual Result (for verification)")
        st.dataframe(actual_row[['DATE', 'DS', 'SG', 'FD', 'GD', 'GL', 'DB']])
    else:
        st.info("Future date - Prediction ready!")
    
    # History preview
    st.header("Pattern Source (30 days before)")
    st.dataframe(past_data[['DATE', 'DS', 'SG']].tail(10))

# Sidebar
st.sidebar.markdown("""
**How it Works:**
1. Select any date
2. App finds patterns from PREVIOUS 30 days
3. Predicts single digit for each shift
4. Compare with actual (if available)

**Perfect for:**
- Backtesting past predictions
- Tomorrow's forecast
- Pattern verification
""")
