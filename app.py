# फाइल अपलोड के बाद इस कोड का उपयोग करें
if uploaded_file:
    try:
        # डेटा लोड करने का ज्यादा सुरक्षित तरीका
        df = pd.read_csv(uploaded_file, skip_blank_lines=True).dropna(how='all')
        
        # कॉलम के नाम से स्पेस हटाने के लिए
        df.columns = df.columns.str.strip()
        
        # केवल जरूरी कॉलम्स चेक करें
        required_cols = ['DS', 'FB', 'GB', 'GL']
        if not all(col in df.columns for col in required_cols):
            st.error(f"फाइल में {required_cols} कॉलम होने चाहिए!")
        else:
            # डेटा को नंबर में बदलें और गलत डेटा हटाएँ
            for col in required_cols:
                df[col] = pd.to_numeric(df[col], errors='coerce')
            df = df.fillna(0) # खाली जगह को 0 से भरें
            
            st.success("Data Optimized!")
            # ... बाकी का एनालिसिस कोड यहाँ ...

