#Website
import requests

# company_lookup_app.py

import requests
import streamlit as st
import pandas as pd


SERPER_API_KEY = "18de03250651e4da793a78266cec557f6451196a"

def get_company_info_from_serper(company_name):
    url = "https://google.serper.dev/search"
    headers = {
        "X-API-KEY": SERPER_API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "q": f"{company_name} company website and industry"
    }

    response = requests.post(url, headers=headers, json=payload)
    data = response.json()

    if "organic" in data and data["organic"]:
        top_result = data["organic"][0]
        return {
            "Company": company_name,
            "Title": top_result.get("title", "N/A"),
            "Website": top_result.get("link", "N/A"),
            "Summary": top_result.get("snippet", "N/A")
        }
    else:
        return {
            "Company": company_name,
            "Title": "N/A",
            "Website": "N/A",
            "Summary": "No results found."
        }

# Streamlit UI
st.title("🔍 Company Info Finder (via Serper API)")

company_input = st.text_area(
    "Enter company names (one per line):",
    placeholder="Apple\nMicrosoft\nTesla"
)

if st.button("Search") and company_input.strip():
    company_list = [name.strip() for name in company_input.split("\n") if name.strip()]
    
    results = []
    with st.spinner("Fetching info for all companies..."):
        for name in company_list:
            result = get_company_info_from_serper(name)
            results.append(result)

    if results:
        df = pd.DataFrame(results)
        st.markdown("### 📄 Company Info Table")
        st.dataframe(df, use_container_width=True)

        # Show download button only if results exist
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Export as CSV",
            data=csv,
            file_name="company_info.csv",
            mime="text/csv"
        )
