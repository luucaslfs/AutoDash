import streamlit as st
import pandas as pd
from io import StringIO
import base64
import dashboard_generator
import auth

st.set_page_config(page_title="AutoDash", layout="wide")

def main():
    st.title("AutoDash")

    if auth():
        st.success("Authenticated successfully!")

        uploaded_file = st.file_uploader("Choose a CSV or Excel file", type=["csv", "xlsx"])
        
        if uploaded_file is not None:
            if uploaded_file.name.endswith('.csv'):
                data = pd.read_csv(uploaded_file)
            else:
                data = pd.read_excel(uploaded_file)
            
            st.write("Data Preview:")
            st.dataframe(data.head())

            if st.button("Generate Dashboard"):
                dashboard_code = dashboard_generator(data)
                
                st.code(dashboard_code, language="python")
                
                # Download button for the generated code
                b64 = base64.b64encode(dashboard_code.encode()).decode()
                href = f'<a href="data:file/txt;base64,{b64}" download="generated_dashboard.py">Download Python File</a>'
                st.markdown(href, unsafe_allow_html=True)

if __name__ == "__main__":
    main()