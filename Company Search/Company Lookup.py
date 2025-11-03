import pandas as pd
import requests
import streamlit as st
from typing import List, Tuple

SERPER_API_KEY = "18de03250651e4da793a78266cec557f6451196a"

INDUSTRY_KEYWORDS: List[Tuple[str, List[str]]] = [
    (
        "SaaS & Cloud Software",
        [
            "saas",
            "software as a service",
            "subscription software",
            "cloud-based",
            "cloud software",
            "cloud platform",
            "b2b saas",
            "data-as-a-service",
            "platform-as-a-service",
            "paas",
            "iaas",
            "cloud infrastructure",
            "cloud-native",
            "multi-tenant",
            "hosted solution",
        ],
    ),
    (
        "IT Services & Consulting",
        [
            "it services",
            "managed services",
            "managed service provider",
            "msp",
            "systems integrator",
            "system integrator",
            "technology consulting",
            "consulting firm",
            "consultancy",
            "digital transformation",
            "implementation partner",
            "outsourcing",
            "staff augmentation",
            "service delivery",
        ],
    ),
    (
        "Technology",
        [
            "technology",
            "tech company",
            "information technology",
            "software",
            "platform",
            "developer tools",
            "devops",
            "data platform",
            "ai",
            "artificial intelligence",
            "machine learning",
            "ml ",
            "nlp",
            "computer vision",
            "cybersecurity",
            "security software",
            "infosec",
            "semiconductor",
            "chip",
            "hardware",
            "electronics",
            "iot",
        ],
    ),
    (
        "Consumer & Internet Brands",
        [
            "consumer brand",
            "direct-to-consumer",
            "d2c",
            "consumer internet",
            "online community",
            "digital brand",
            "social platform",
            "influencer-led",
            "streaming app",
            "lifestyle brand",
            "mobile app",
        ],
    ),
    (
        "Consumer Goods",
        [
            "consumer goods",
            "cpg",
            "personal care",
            "household products",
            "apparel",
            "footwear",
            "cosmetic",
            "beauty brand",
            "beverage",
            "food brand",
        ],
    ),
    (
        "Retail",
        [
            "retail",
            "ecommerce",
            "e-commerce",
            "online store",
            "marketplace",
            "grocery store",
            "supermarket",
            "department store",
            "omnichannel",
        ],
    ),
    (
        "Manufacturing & Supply Chain",
        [
            "manufacturing",
            "manufacturer",
            "factory",
            "fabrication",
            "production facility",
            "supply chain",
            "contract manufacturer",
            "industrial automation",
            "assembly plant",
            "supply solutions",
        ],
    ),
    (
        "Automotive",
        [
            "automotive",
            "auto manufacturer",
            "car maker",
            "vehicle",
            "ev ",
            "electric vehicle",
            "mobility",
            "autonomous driving",
            "autopilot",
        ],
    ),
    (
        "Energy",
        [
            "energy",
            "oil",
            "gas",
            "o&g",
            "petroleum",
            "renewable",
            "solar",
            "wind",
            "utility-scale",
            "battery storage",
            "power grid",
            "electric utility",
        ],
    ),
    (
        "Utilities",
        [
            "utility",
            "utilities",
            "water utility",
            "electric utility",
            "gas utility",
        ],
    ),
    (
        "Financial Services",
        [
            "bank",
            "banking",
            "financial services",
            "fintech",
            "payments",
            "payment",
            "lending",
            "loan",
            "insurance",
            "insurtech",
            "brokerage",
            "investment",
            "asset management",
            "wealth management",
            "capital markets",
            "exchange",
        ],
    ),
    (
        "Healthcare",
        [
            "healthcare",
            "medical",
            "hospital",
            "clinic",
            "biotech",
            "biotechnology",
            "pharma",
            "pharmaceutical",
            "life sciences",
            "medtech",
            "diagnostic",
        ],
    ),
    (
        "Telecommunications",
        [
            "telecommunications",
            "telecom",
            "wireless",
            "carrier",
            "broadband",
            "5g ",
            "network operator",
        ],
    ),
    (
        "Media & Entertainment",
        [
            "media",
            "entertainment",
            "streaming",
            "video platform",
            "music label",
            "gaming",
            "game studio",
            "publisher",
            "content platform",
        ],
    ),
    (
        "Real Estate",
        [
            "real estate",
            "reit",
            "property management",
            "broker",
            "proptech",
        ],
    ),
    (
        "Transportation",
        [
            "airline",
            "aviation",
            "rail",
            "shipping",
            "logistics",
            "freight",
            "ride-hailing",
            "rideshare",
            "delivery network",
        ],
    ),
    (
        "Education",
        [
            "education",
            "edtech",
            "school",
            "university",
            "learning platform",
        ],
    ),
    (
        "Agriculture",
        [
            "agriculture",
            "agtech",
            "farming",
            "crop",
            "agri",
        ],
    ),
    (
        "Hospitality & Travel",
        [
            "hotel",
            "hospitality",
            "travel",
            "tourism",
            "booking platform",
            "resort",
        ],
    ),
    (
        "Government & Non-Profit",
        [
            "government",
            "public sector",
            "ngo",
            "non-profit",
            "nonprofit",
        ],
    ),
]

STARTUP_KEYWORDS: List[str] = [
    "startup",
    "scale-up",
    "scaleup",
    "seed round",
    "series a",
    "series b",
    "series c",
    "pre-seed",
    "vc-backed",
    "venture-backed",
    "venture capital",
    "accelerator",
    "incubator",
    "y combinator",
    "yc",
    "angel investment",
    "early-stage",
    "fast-growing",
    "high-growth",
    "growth stage",
    "funding"
]

TRADITIONAL_KEYWORDS: List[str] = [
    "established",
    "since 19",
    "since 18",
    "legacy",
    "subsidiary",
    "conglomerate",
    "incumbent",
    "multinational",
    "family business"
]

PUBLIC_KEYWORDS: List[str] = [
    "public company",
    "publicly traded",
    "listed company",
    "fortune 500"
]


def _standardize_industry_from_text(text: str) -> str:
    """Return a standardized industry based on keywords in the text."""
    if not text:
        return "Unknown"

    lower_text = text.lower()
    for industry, keywords in INDUSTRY_KEYWORDS:
        if any(keyword in lower_text for keyword in keywords):
            return industry

    return "Unknown"


def _classify_business_type(text: str) -> str:
    """Heuristically classify a company as Startup or Traditional based on keywords."""
    if not text:
        return "Unknown"

    lower_text = text.lower()

    if any(keyword in lower_text for keyword in STARTUP_KEYWORDS):
        return "Startup"

    if any(keyword in lower_text for keyword in TRADITIONAL_KEYWORDS):
        return "Traditional"
    
    if any(keyword in lower_text for keyword in PUBLIC_KEYWORDS):
        return "Public Company"

    return "Public Company"



def get_company_info_from_serper(company_name: str) -> dict:
    url = "https://google.serper.dev/search"
    headers = {
        "X-API-KEY": SERPER_API_KEY,
        "Content-Type": "application/json",
    }
    payload = {"q": f"{company_name} company website and industry"}

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=15)
        response.raise_for_status()
        data = response.json()
    except (requests.RequestException, ValueError):
        return {
            "Company": company_name,
            "Title": "N/A",
            "Website": "N/A",
            "Summary": "Lookup failed.",
            "Industry": "Unknown",
            "Business Type": "Unknown",
        }

    if data.get("organic"):
        top_result = data["organic"][0]
        title = top_result.get("title", "N/A")
        link = top_result.get("link", "N/A")
        snippet = top_result.get("snippet", "N/A")
        combined_text = " ".join(
            part for part in (title, snippet) if part and part != "N/A"
        )
        industry = _standardize_industry_from_text(combined_text)
        business_type = _classify_business_type(combined_text)
        return {
            "Company": company_name,
            "Title": title,
            "Website": link,
            "Summary": snippet,
            "Industry": industry,
            "Business Type": business_type,
        }

    return {
        "Company": company_name,
        "Title": "N/A",
        "Website": "N/A",
        "Summary": "No results found.",
        "Industry": "Unknown",
        "Business Type": "Unknown",
    }


st.title("Company Info Finder (via Serper API)")

company_input = st.text_area(
    "Enter company names (one per line):",
    placeholder="Apple\nMicrosoft\nTesla",
)

if st.button("Search") and company_input.strip():
    company_list = [name.strip() for name in company_input.splitlines() if name.strip()]

    results = []
    with st.spinner("Fetching info for all companies..."):
        for name in company_list:
            results.append(get_company_info_from_serper(name))

    if results:
        df = pd.DataFrame(results)
        if "Industry" not in df.columns:
            df["Industry"] = "Unknown"
        if "Business Type" not in df.columns:
            df["Business Type"] = "Unknown"
        df = df[["Company", "Industry", "Business Type", "Title", "Website", "Summary"]]

        st.markdown("### Company Info Table")
        st.dataframe(df, use_container_width=True)

        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Export as CSV",
            data=csv,
            file_name="company_info.csv",
            mime="text/csv",
        )
else:
    st.info("Add one or more company names to start a lookup.")
