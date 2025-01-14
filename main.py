import streamlit as st
from scrape import (
    scrape_website,
    extract_body_content,
    clean_body_content,
    split_dom_content,
    scrape_multiple_websites
)
from parse import parse_with_groq

# Streamlit UI
st.set_page_config(page_title="AI Web Scraper", layout="wide")
st.markdown("<h1>AI Web Scraper <sup><span style='color:red; font-size:0.6em;'>(beta)</span></sup></h1>", unsafe_allow_html=True)

def is_valid_url(url):
    return url.startswith("http://") or url.startswith("https://")

# Input URL
url = st.text_input("Enter Website URL", placeholder="https://example.com")

# Step 1: Scrape the Website
if st.button("Scrape Website"):
    if is_valid_url(url):
        with st.spinner("Scraping the website..."):
            dom_content = scrape_website(url)
            if dom_content:
                body_content = extract_body_content(dom_content)
                cleaned_content = clean_body_content(body_content)

                # Store the DOM content in Streamlit session state
                st.session_state.dom_content = cleaned_content

                # Display the DOM content in an expandable text box
                with st.expander("View DOM Content"):
                    st.text_area("DOM Content", cleaned_content, height=300)
            else:
                st.error("Failed to scrape the website.")
    else:
        st.error("Please enter a valid URL.")

# Step 2: Ask Questions About the DOM Content
if "dom_content" in st.session_state:
    st.subheader("Parse the DOM Content")
    parse_description = st.text_area("Describe what you want to parse", placeholder="e.g., Extract all email addresses")
    
    if st.button("Parse Content"):
        if parse_description:
            with st.spinner("Parsing the content..."):
                dom_chunks = split_dom_content(st.session_state.dom_content)
                combined_results = parse_with_groq(dom_chunks, parse_description)
                
                # Display the combined parsed result
                st.subheader("Parsed Results")
                st.code(combined_results)
        else:
            st.error("Please provide a description of what you want to parse.")
