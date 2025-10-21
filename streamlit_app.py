import streamlit as st
import pandas as pd
import numpy as np
import requests
import json
import configparser
import os
from datetime import datetime, timedelta

st.set_page_config(
    page_title="Oak Furniture Land GMC Feed Optimizer",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': None
    }
)

# Minimal CSS - only hide branding, keep sidebar
st.markdown("""
<style>
    /* Hide Streamlit header */
    .stApp > header {
        display: none;
    }
    
    /* Hide Streamlit footer */
    .stApp > footer {
        display: none;
    }
    
    /* Hide Streamlit watermark */
    .stApp::before {
        display: none;
    }
    
    /* Login form styling */
    .login-container {
        max-width: 400px;
        margin: 0 auto;
        padding: 2rem;
        border-radius: 10px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    .login-title {
        text-align: center;
        margin-bottom: 2rem;
        font-size: 1.5rem;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Authentication system
def check_credentials(username, password):
    """Check if credentials are valid"""
    valid_users = {
        "oakfurniture": "OFL2024!",
        "admin": "Admin123!",
        "seo": "SEO2024!"
    }
    return valid_users.get(username) == password

# Initialize session state for authentication
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

# Show login form if not authenticated
if not st.session_state['authenticated']:
    st.markdown('<div class="login-container">', unsafe_allow_html=True)
    
    st.markdown('<div class="login-title">🔐 Oak Furniture Land</div>', unsafe_allow_html=True)
    st.markdown('<div class="login-title">GMC Feed Optimizer</div>', unsafe_allow_html=True)
    
    with st.form("login_form"):
        st.markdown("**Please enter your credentials to access the system:**")
        
        username = st.text_input("Username", placeholder="Enter username")
        password = st.text_input("Password", type="password", placeholder="Enter password")
        
        submitted = st.form_submit_button("Login", type="primary")
        
        if submitted:
            if check_credentials(username, password):
                st.session_state['authenticated'] = True
                st.session_state['username'] = username
                st.success("✅ Login successful!")
                st.rerun()
            else:
                st.error("❌ Invalid username or password")
    
    st.markdown("---")
    st.markdown("**Contact your administrator for access credentials.**")
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# Show logout button
if st.session_state['authenticated']:
    col1, col2, col3 = st.columns([1, 1, 1])
    with col3:
        if st.button("🚪 Logout"):
            st.session_state['authenticated'] = False
            st.session_state.pop('username', None)
            st.rerun()

st.title("🛒 Oak Furniture Land GMC Feed Optimizer")
st.subheader("Strategic product feed optimization using search volume + PPC intelligence")
st.caption("Version 1.1")

# Initialize session state with persistence
if 'sitebulb_data' not in st.session_state:
    st.session_state['sitebulb_data'] = None
if 'seomonitor_data' not in st.session_state:
    st.session_state['seomonitor_data'] = None
if 'product_data' not in st.session_state:
    st.session_state['product_data'] = None
if 'gmc_feed' not in st.session_state:
    st.session_state['gmc_feed'] = None
if 'gmc_file' not in st.session_state:
    st.session_state['gmc_file'] = None
if 'sitebulb_file' not in st.session_state:
    st.session_state['sitebulb_file'] = None

# Data Status Header - Shows what's loaded and analysis readiness
st.markdown("### 📊 Data Status & Analysis Readiness")

# Create columns for status display
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.session_state['gmc_feed'] is not None:
        st.success(f"✅ **GMC Feed**\n{len(st.session_state['gmc_feed'])} products\n{st.session_state.get('gmc_file', 'Unknown file')}")
    else:
        st.error("❌ **GMC Feed**\nNot loaded")

with col2:
    if st.session_state['seomonitor_data'] is not None:
        st.success(f"✅ **SEOMonitor**\n{len(st.session_state['seomonitor_data'])} keywords\nIntelligence data ready")
    else:
        st.error("❌ **SEOMonitor**\nNot loaded")

with col3:
    if st.session_state['sitebulb_data'] is not None:
        st.success(f"✅ **Sitebulb**\n{len(st.session_state['sitebulb_data'])} pages\nCrawl data ready")
    else:
        st.warning("⚠️ **Sitebulb**\nOptional")

with col4:
    # Analysis readiness check
    gmc_ready = st.session_state['gmc_feed'] is not None
    seo_ready = st.session_state['seomonitor_data'] is not None
    
    if gmc_ready and seo_ready:
        st.success("🚀 **Ready for Analysis**\nAll core data loaded\nProceed to optimization!")
    elif gmc_ready:
        st.warning("⚠️ **Partial Ready**\nGMC loaded, need SEO data")
    elif seo_ready:
        st.warning("⚠️ **Partial Ready**\nSEO loaded, need GMC data")
    else:
        st.error("❌ **Not Ready**\nNeed GMC + SEO data")

st.markdown("---")

# Sidebar for navigation
st.sidebar.title("Navigation")

# Data Status Indicator
st.sidebar.markdown("### 📊 Data Status")
if st.session_state['gmc_feed'] is not None:
    st.sidebar.success(f"✅ GMC: {len(st.session_state['gmc_feed'])} products")
else:
    st.sidebar.warning("⚠️ No GMC data")

if st.session_state['seomonitor_data'] is not None:
    st.sidebar.success(f"✅ SEO: {len(st.session_state['seomonitor_data'])} keywords")
else:
    st.sidebar.warning("⚠️ No SEO data")

if st.session_state['sitebulb_data'] is not None:
    st.sidebar.success(f"✅ Sitebulb: {len(st.session_state['sitebulb_data'])} pages")
else:
    st.sidebar.warning("⚠️ No Sitebulb data")

st.sidebar.markdown("---")

page = st.sidebar.selectbox("Choose a section", [
    "GMC Feed Upload", 
    "Sitebulb Upload",
    "SEOMonitor API", 
    "Strategic Optimization",
    "Export Optimized Feed"
])

if page == "GMC Feed Upload":
    st.header("🛒 Upload GMC Feed Data")
    
    # Show current data status
    if st.session_state['gmc_feed'] is not None:
        st.success(f"✅ GMC Feed Already Loaded: {st.session_state.get('gmc_file', 'Unknown file')} ({len(st.session_state['gmc_feed'])} products)")
        st.dataframe(st.session_state['gmc_feed'].head(10))
        st.info("💡 **Data Persistence**: Your GMC feed data is saved and will persist across all tabs.")
    
    # File upload
    uploaded_file = st.file_uploader(
        "Upload your GMC feed file (CSV, Excel)",
        type=['csv', 'xlsx', 'xls'],
        help="Upload your Google Merchant Center product feed"
    )
    
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            
            st.success(f"✅ GMC feed uploaded! {len(df)} products loaded.")
            st.session_state['gmc_feed'] = df
            st.session_state['gmc_file'] = uploaded_file.name
            st.dataframe(df.head(10))
                
        except Exception as e:
            st.error(f"❌ Error reading file: {str(e)}")

elif page == "Sitebulb Upload":
    st.header("📁 Upload Sitebulb Crawl Data")
    
    # Show current data status
    if st.session_state['sitebulb_data'] is not None:
        st.success(f"✅ Sitebulb Data Already Loaded: {st.session_state.get('sitebulb_file', 'Unknown file')} ({len(st.session_state['sitebulb_data'])} records)")
        st.dataframe(st.session_state['sitebulb_data'].head(10))
        st.info("💡 **Data Persistence**: Your Sitebulb crawl data is saved and will persist across all tabs.")
    
    # File upload
    uploaded_file = st.file_uploader(
        "Upload your Sitebulb crawl report (CSV, Excel)",
        type=['csv', 'xlsx', 'xls'],
        help="Upload your Sitebulb crawl export file"
    )
    
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            
            st.success(f"✅ Sitebulb data uploaded! {len(df)} records loaded.")
            st.session_state['sitebulb_data'] = df
            st.session_state['sitebulb_file'] = uploaded_file.name
            st.dataframe(df.head(10))
                
        except Exception as e:
            st.error(f"❌ Error reading file: {str(e)}")

elif page == "SEOMonitor API":
    st.header("📈 SEOMonitor API Integration")
    
    # Try to load config
    try:
        config = configparser.ConfigParser()
        config.read('config_oak_furnitor.ini')
        api_key = config['SEOMonitor']['api_key']
        campaign_id = config['SEOMonitor']['campaign_id']
        brand_name = config['Brand']['name']
        
        st.success(f"✅ API configured for {brand_name}")
        st.info(f"Campaign ID: {campaign_id}")
        
        if st.button("🔍 Fetch ALL Keywords (Paginated)"):
            with st.spinner("🔄 Fetching ALL keyword data with pagination..."):
                # Enhanced API call with pagination
                headers = {
                    'Authorization': api_key,
                    'X-Token': api_key,
                    'Accept': 'application/json'
                }
                
                end_date = datetime.now()
                start_date = end_date - timedelta(days=90)
                
                all_keywords = []
                offset = 0
                limit = 200
                
                while True:
                    params = {
                        'campaign_id': campaign_id,
                        'start_date': start_date.strftime('%Y-%m-%d'),
                        'end_date': end_date.strftime('%Y-%m-%d'),
                        'include_all_groups': 'true',
                        'limit': limit,
                        'offset': offset
                    }
                    
                    url = f"https://apigw.seomonitor.com/v3/rank-tracker/v3.0/keywords"
                    response = requests.get(url, headers=headers, params=params)
                    
                    if response.status_code == 200:
                        data = response.json()
                        if isinstance(data, list) and len(data) > 0:
                            all_keywords.extend(data)
                            offset += len(data)
                            st.write(f"📊 Fetched {len(data)} keywords (Total: {len(all_keywords)})")
                            
                            # Safety cap to avoid infinite loops
                            if len(data) < limit or len(all_keywords) >= 10000:
                                break
                        else:
                            break
                    else:
                        st.error(f"❌ API Error: {response.status_code}")
                        break
                
                if all_keywords:
                    df_seo = pd.DataFrame(all_keywords)
                    st.session_state['seomonitor_data'] = df_seo
                    st.success(f"✅ Fetched {len(df_seo)} keywords total!")
                    st.metric("Total Keywords", len(df_seo))
                    
                    # Show sample data
                    st.subheader("📊 Sample Keyword Data")
                    st.dataframe(df_seo.head(10))
                else:
                    st.error("❌ No keywords found")
        
    except Exception as e:
        st.error(f"❌ Config file not found: {str(e)}")

elif page == "Strategic Optimization":
    st.header("🧠 AI-Powered Strategic Optimization")
    
    if st.session_state['gmc_feed'] is None:
        st.warning("⚠️ Please upload GMC feed data first.")
    else:
        df_gmc = st.session_state['gmc_feed']
        df_seo = st.session_state.get('seomonitor_data')
        
        st.subheader("🔍 Data Sources Available")
        col1, col2 = st.columns(2)
        with col1:
            if df_seo is not None:
                st.success(f"✅ SEOMonitor: {len(df_seo)} keywords")
            else:
                st.warning("⚠️ No SEOMonitor data")
        with col2:
            st.success(f"✅ GMC Feed: {len(df_gmc)} products")
        
        if st.button("🚀 Generate AI-Powered Optimizations", type="primary"):
            if df_seo is not None:
                st.success("✅ Optimization would be generated here!")
                st.info("This is a simplified version. Full optimization logic will be restored.")
            else:
                st.error("❌ SEOMonitor data required for AI optimization.")

elif page == "Export Optimized Feed":
    st.header("📤 Export Optimized GMC Feed")
    
    if st.session_state['gmc_feed'] is None:
        st.warning("⚠️ Please upload GMC feed data first.")
    else:
        df_gmc = st.session_state['gmc_feed']
        
        st.subheader("📊 Export Options")
        
        # Export original feed
        csv_original = df_gmc.to_csv(index=False)
        st.download_button(
            label="Download Original CSV",
            data=csv_original,
            file_name=f"original_{st.session_state.get('gmc_file', 'gmc_feed')}.csv",
            mime="text/csv"
        )
        
        st.info("💡 Full optimization export will be restored in the next update.")

# Footer
st.markdown("---")
st.markdown("🛒 Oak Furniture Land GMC Feed Optimizer | Strategic SEO + PPC Integration")