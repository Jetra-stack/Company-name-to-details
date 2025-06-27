#Website
import requests

# company_lookup_app.py

import requests
import streamlit as st

SERPER_API_KEY = st.secrets["SERPER_API_KEY"]

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
        title = top_result.get("title")
        link = top_result.get("link")
        snippet = top_result.get("snippet")

        return {
            "title": title,
            "website": link,
            "summary": snippet
        }
    else:
        return {"error": "No results found."}

#Streamlit UI
st.title("🔍 Company Info Finder (via Serper)")
company_name = st.text_input("Enter a company name:")

if st.button("Search") and company_name.strip():
    with st.spinner("Fetching company info..."):
        info = get_company_info_from_serper(company_name)
    
    st.markdown("### 📄 Result:")
    if "error" in info:
        st.error(info["error"])
    else:
        st.markdown(f"**Title:** {info['title']}")
        st.markdown(f"**Website:** [{info['website']}]({info['website']})")
        st.markdown(f"**Summary:** {info['summary']}")
