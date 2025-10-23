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

# Professional CSS with unique font styling
st.markdown("""
<style>
/* Import Google Fonts for unique typography */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap');

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

/* Global font styling */
.stApp {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    font-weight: 400;
    line-height: 1.6;
}

/* Headers with unique styling */
h1 {
    font-family: 'Inter', sans-serif;
    font-weight: 700;
    font-size: 2.5rem;
    color: #1a1a1a;
    letter-spacing: -0.02em;
    margin-bottom: 0.5rem;
}

h2 {
    font-family: 'Inter', sans-serif;
    font-weight: 600;
    font-size: 1.8rem;
    color: #2d3748;
    letter-spacing: -0.01em;
    margin-top: 2rem;
    margin-bottom: 1rem;
}

h3 {
    font-family: 'Inter', sans-serif;
    font-weight: 600;
    font-size: 1.4rem;
    color: #4a5568;
    margin-top: 1.5rem;
    margin-bottom: 0.8rem;
}

/* Subheaders */
.stSubheader {
    font-family: 'Inter', sans-serif;
    font-weight: 500;
    font-size: 1.2rem;
    color: #718096;
    margin-bottom: 1rem;
}

/* Caption styling */
.stCaption {
    font-family: 'JetBrains Mono', 'Courier New', monospace;
    font-weight: 500;
    font-size: 0.9rem;
    color: #805ad5;
    background: linear-gradient(135deg, #f7fafc 0%, #edf2f7 100%);
    padding: 0.5rem 1rem;
    border-radius: 8px;
    border-left: 4px solid #805ad5;
    margin-bottom: 1rem;
}

/* Button styling */
.stButton > button {
    font-family: 'Inter', sans-serif;
    font-weight: 500;
    border-radius: 8px;
    transition: all 0.2s ease;
}

.stButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}

/* Metric styling */
.stMetric {
    font-family: 'Inter', sans-serif;
}

.stMetric > div > div {
    font-weight: 600;
    color: #2d3748;
}

/* Dataframe styling */
.stDataFrame {
    font-family: 'Inter', sans-serif;
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

/* Sidebar styling */
.stSidebar {
    font-family: 'Inter', sans-serif;
}

.stSidebar .stSelectbox > div > div {
    font-family: 'Inter', sans-serif;
    font-weight: 500;
}

/* Login form styling */
.login-container {
    max-width: 400px;
    margin: 0 auto;
    padding: 2rem;
    border-radius: 12px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    font-family: 'Inter', sans-serif;
    box-shadow: 0 10px 30px rgba(0,0,0,0.2);
}

.login-title {
    text-align: center;
    margin-bottom: 2rem;
    font-size: 1.8rem;
    font-weight: 700;
    letter-spacing: -0.02em;
}

/* Success/Error message styling */
.stSuccess {
    font-family: 'Inter', sans-serif;
    font-weight: 500;
    border-radius: 8px;
}

.stError {
    font-family: 'Inter', sans-serif;
    font-weight: 500;
    border-radius: 8px;
}

.stWarning {
    font-family: 'Inter', sans-serif;
    font-weight: 500;
    border-radius: 8px;
}

.stInfo {
    font-family: 'Inter', sans-serif;
    font-weight: 500;
    border-radius: 8px;
}

/* Code blocks */
.stCode {
    font-family: 'JetBrains Mono', 'Courier New', monospace;
    font-size: 0.9rem;
    background: #f7fafc;
    border-radius: 6px;
    padding: 0.5rem;
}

/* Progress bar styling */
.stProgress > div > div {
    border-radius: 8px;
    background: linear-gradient(90deg, #805ad5 0%, #667eea 100%);
}

/* Selectbox and input styling */
.stSelectbox > div > div,
.stTextInput > div > div > input {
    font-family: 'Inter', sans-serif;
    font-weight: 400;
    border-radius: 6px;
}

/* File uploader styling */
.stFileUploader > div {
    font-family: 'Inter', sans-serif;
    border-radius: 8px;
    border: 2px dashed #cbd5e0;
    transition: all 0.2s ease;
}

.stFileUploader > div:hover {
    border-color: #805ad5;
    background: #f7fafc;
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
st.caption("Version 2.6 - COMPLETE ERROR HANDLING FIX")

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
        config.read('config_oak_furniture.ini')
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
        
        # Add batch processing option for large datasets
        st.subheader("⚙️ Processing Options")
        batch_size = st.selectbox(
            "Processing batch size (for large datasets)",
            [100, 250, 500, 1000, "All at once"],
            index=2,
            help="Smaller batches prevent timeouts but take longer overall"
        )
        
        # Add preview mode option
        preview_mode = st.checkbox(
            "Preview mode (analyze first 10 products only)",
            value=False,
            help="Test optimization logic on a small sample before processing all products"
        )
        
        if preview_mode:
            st.info("🔍 Preview mode: Will analyze first 10 products only for testing")
        
        if st.button("🚀 Generate Intelligent Optimizations", type="primary"):
            if df_seo is not None:
                with st.spinner("🧠 AI is analyzing SEO data and optimizing all products..."):
                    # Initialize progress bar
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    # Get Sitebulb data if available
                    df_sitebulb = st.session_state.get('sitebulb_data')
                    
                    # Get optimization recommendations
                    recommendations = []
                    total_products = len(df_gmc)
                    
                    # Apply preview mode if enabled
                    if preview_mode:
                        total_products = min(10, total_products)
                        st.info(f"🔍 Preview mode: Analyzing first {total_products} products only")
                    
                    for i, (_, product) in enumerate(df_gmc.iterrows()):
                        # Update progress
                        progress = (i + 1) / total_products
                        progress_bar.progress(progress)
                        status_text.text(f"🎯 Analyzing product {i+1}/{total_products}: {product.get('title', 'Unknown')[:50]}...")
                        
                        # Get product data
                        product_title = str(product.get('title', ''))
                        product_desc = str(product.get('description', ''))
                        product_id = product.get('id', f'product_{i}')
                        product_text = f"{product_title} {product_desc}".lower()
                        
                        # Initialize optimization
                        optimized_title = product_title
                        optimized_desc = product_desc
                        title_reasoning = "No optimization needed"
                        description_reasoning = "No optimization needed"
                        priority_score = 0
                        expected_impact = "LOW"
                        
                        # TRULY INTELLIGENT SEO OPTIMIZATION BASED ON PERFORMANCE DATA
                        
                        # 1. Find TRULY relevant keywords with actual ranking data
                        relevant_keywords = []
                        product_words = set(product_text.lower().split())
                        
                        # Define furniture-related terms for better matching
                        furniture_terms = {'sofa', 'chair', 'table', 'desk', 'bed', 'furniture', 'oak', 'wood', 'fabric', 'leather', 'dining', 'living', 'bedroom', 'office', 'recliner', 'storage', 'cabinet', 'wardrobe', 'dresser', 'bookshelf', 'coffee', 'side', 'dining', 'kitchen', 'bathroom', 'outdoor', 'garden'}
                        
                        for _, keyword_row in df_seo.iterrows():
                            keyword = str(keyword_row.get('keyword', ''))
                            if keyword:
                                keyword_words = set(keyword.lower().split())
                                
                                # Get actual ranking data first
                                position = keyword_row.get('position', 999)
                                search_volume = keyword_row.get('search_volume', 0)
                                difficulty = keyword_row.get('difficulty', 0)
                                
                                # STRICT RELEVANCE CHECKING
                                # 1. Must have actual search volume (> 0)
                                # 2. Must be semantically relevant to the product
                                if search_volume > 0:
                                    # Check for semantic relevance
                                    is_relevant = False
                                    
                                    # Check if keyword contains furniture-related terms
                                    if keyword_words.intersection(furniture_terms):
                                        is_relevant = True
                                    
                                    # Check if keyword is directly in product text
                                    elif keyword.lower() in product_text.lower():
                                        is_relevant = True
                                    
                                    # Check for word overlap with product (but be more strict)
                                    elif len(keyword_words.intersection(product_words)) >= 2:  # At least 2 words must match
                                        is_relevant = True
                                    
                                    if is_relevant:
                                        relevant_keywords.append({
                                            'keyword': keyword,
                                            'position': position,
                                            'search_volume': search_volume,
                                            'difficulty': difficulty
                                        })
                        
                        # 2. INTELLIGENT ANALYSIS BASED ON ACTUAL PERFORMANCE PATTERNS
                        if relevant_keywords:
                            # Sort by search volume to prioritize opportunities
                            relevant_keywords.sort(key=lambda x: x['search_volume'], reverse=True)
                            
                            # ANALYZE WHAT MAKES PRODUCTS RANK WELL
                            # Find keywords ranking in top 10 (successful patterns)
                            top_performers = [kw for kw in relevant_keywords if kw['position'] <= 10 and kw['search_volume'] > 0]
                            
                            # Find keywords ranking poorly but with high volume (opportunities)
                            poor_performers = [kw for kw in relevant_keywords if kw['position'] > 20 and kw['search_volume'] > 500]
                            
                            # Find high-volume keywords we're not ranking for (gaps)
                            missing_opportunities = [kw for kw in relevant_keywords if kw['search_volume'] > 1000 and kw['position'] > 50]
                            
                            # Find low-difficulty, high-volume opportunities (easier wins)
                            easy_wins = [kw for kw in relevant_keywords if kw['difficulty'] < 30 and kw['search_volume'] > 300 and kw['position'] > 30]
                            
                            # 3. LOGICAL OPTIMIZATION DECISIONS BASED ON SEO PATTERNS
                            
                            # TITLE OPTIMIZATION - Prioritize easy wins first
                            if easy_wins:
                                # Focus on low-difficulty, high-volume opportunities first
                                best_easy_win = easy_wins[0]
                                optimized_title = f"{best_easy_win['keyword'].title()} | {product_title}"
                                title_reasoning = f"EASY WIN: Target '{best_easy_win['keyword']}' ({best_easy_win['search_volume']:,} searches, difficulty {best_easy_win['difficulty']}) - low competition opportunity"
                                priority_score += 70
                                
                            elif top_performers:
                                # Analyze what makes top performers successful
                                best_performer = top_performers[0]
                                
                                # Check if the successful keyword is prominently placed in title
                                if best_performer['keyword'].lower() not in product_title.lower():
                                    # Move successful keyword to front of title
                                    optimized_title = f"{best_performer['keyword'].title()} {product_title}"
                                    title_reasoning = f"Move high-performing keyword '{best_performer['keyword']}' to front (ranks #{best_performer['position']}, {best_performer['search_volume']:,} searches) - proven to work"
                                    priority_score += 40
                                else:
                                    # Keyword is in title but not prominent - restructure
                                    words = product_title.split()
                                    keyword_words = best_performer['keyword'].lower().split()
                                    
                                    # Find where keyword appears and move to front
                                    for i, word in enumerate(words):
                                        if word.lower() in keyword_words:
                                            # Move keyword to front
                                            keyword_part = ' '.join([w for w in words if w.lower() in keyword_words])
                                            remaining_words = [w for w in words if w.lower() not in keyword_words]
                                            optimized_title = f"{keyword_part.title()} {' '.join(remaining_words)}"
                                            title_reasoning = f"Restructure title to prioritize '{best_performer['keyword']}' (ranks #{best_performer['position']}) - move to front for better visibility"
                                            priority_score += 35
                                            break
                                    
                            elif poor_performers:
                                # Focus on improving poor performers with high volume
                                best_opportunity = poor_performers[0]
                                
                                # Check if keyword is in title but not prominent
                                if best_opportunity['keyword'].lower() in product_title.lower():
                                    # Keyword is there but not working - move to front
                                    words = product_title.split()
                                    keyword_words = best_opportunity['keyword'].lower().split()
                                    
                                    # Move keyword to front
                                    keyword_part = ' '.join([w for w in words if w.lower() in keyword_words])
                                    remaining_words = [w for w in words if w.lower() not in keyword_words]
                                    optimized_title = f"{keyword_part.title()} {' '.join(remaining_words)}"
                                    title_reasoning = f"Move '{best_opportunity['keyword']}' to front - currently ranks #{best_opportunity['position']} but has {best_opportunity['search_volume']:,} searches (high potential)"
                                    priority_score += 45
                                else:
                                    # Add missing high-volume keyword
                                    optimized_title = f"{best_opportunity['keyword'].title()} {product_title}"
                                    title_reasoning = f"Add high-volume keyword '{best_opportunity['keyword']}' ({best_opportunity['search_volume']:,} searches) - currently ranking #{best_opportunity['position']} but can improve"
                                    priority_score += 50
                                    
                            elif missing_opportunities:
                                # Target completely missing high-volume keywords
                                best_missing = missing_opportunities[0]
                                optimized_title = f"{best_missing['keyword'].title()} {product_title}"
                                title_reasoning = f"Target missing high-volume keyword '{best_missing['keyword']}' ({best_missing['search_volume']:,} searches) - not currently ranking, big opportunity"
                                priority_score += 60
                            
                            # DESCRIPTION OPTIMIZATION - Based on successful patterns
                            if top_performers:
                                # Use successful keywords in description for reinforcement
                                best_performer = top_performers[0]
                                if best_performer['keyword'].lower() not in product_desc.lower():
                                    optimized_desc = f"{product_desc} {best_performer['keyword'].title()}"
                                    description_reasoning = f"Reinforce successful keyword '{best_performer['keyword']}' in description (ranks #{best_performer['position']}) - helps maintain ranking"
                                    priority_score += 25
                            
                            # 4. Calculate impact based on actual SEO value
                            if priority_score >= 60:
                                expected_impact = "HIGH"
                            elif priority_score >= 35:
                                expected_impact = "MEDIUM"
                            else:
                                expected_impact = "LOW"
                        else:
                            # No relevant keywords found - use AI intelligence for basic optimization
                            # AI-POWERED FALLBACK OPTIMIZATION
                            
                            # Extract key product attributes for intelligent optimization
                            product_words = product_text.lower().split()
                            
                            # Identify product type and key features
                            product_type = None
                            material = None
                            color = None
                            brand = None
                            
                            # Common furniture types
                            furniture_types = {
                                'sofa': ['sofa', 'settee', 'couch', 'recliner'],
                                'chair': ['chair', 'dining chair', 'office chair', 'armchair'],
                                'table': ['table', 'dining table', 'coffee table', 'side table', 'desk'],
                                'bed': ['bed', 'bedroom', 'mattress', 'headboard'],
                                'storage': ['wardrobe', 'cabinet', 'dresser', 'bookshelf', 'storage'],
                                'dining': ['dining', 'dining room', 'dining set'],
                                'living': ['living room', 'lounge', 'living'],
                                'office': ['office', 'desk', 'office chair', 'office furniture']
                            }
                            
                            # Identify product type
                            for ftype, keywords in furniture_types.items():
                                if any(kw in product_text.lower() for kw in keywords):
                                    product_type = ftype
                                    break
                            
                            # Extract material - be more specific and accurate
                            materials = ['oak', 'wood', 'fabric', 'leather', 'metal', 'glass', 'marble', 'mink', 'velvet', 'cotton', 'linen', 'beige', 'plush', 'modular']
                            for mat in materials:
                                if mat in product_text.lower():
                                    material = mat
                                    break
                            
                            # Special case: if it's a fabric sofa, use "Fabric" not "Oak"
                            if 'fabric' in product_text.lower() and 'sofa' in product_text.lower():
                                material = 'fabric'
                            elif 'leather' in product_text.lower() and 'sofa' in product_text.lower():
                                material = 'leather'
                            elif 'oak' in product_text.lower() and ('table' in product_text.lower() or 'chair' in product_text.lower()):
                                material = 'oak'
                            
                            # Extract color
                            colors = ['white', 'black', 'brown', 'grey', 'gray', 'beige', 'cream', 'navy', 'blue', 'red', 'green', 'mink', 'charcoal']
                            for col in colors:
                                if col in product_text.lower():
                                    color = col
                                    break
                            
                            # Extract brand
                            if 'oak furnitureland' in product_text.lower():
                                brand = 'Oak Furnitureland'
                            
                            # AI INTELLIGENT OPTIMIZATION BASED ON PRODUCT ANALYSIS
                            if product_type and material:
                                # Check if material is already prominent in title
                                material_already_prominent = material.lower() in product_title.lower()[:50]  # Check first 50 chars
                                
                                if not material_already_prominent:
                                    # INTELLIGENT PRODUCT INTENT ANALYSIS
                                    # Analyze what customers are actually searching for based on product attributes
                                    
                                    # Extract additional product attributes for better targeting
                                    size_info = ""
                                    style_info = ""
                                    color_info = ""
                                    special_features = []
                                    
                                    # Look for size information
                                    if any(size in product_text.lower() for size in ['2 seat', '3 seat', '4 seat', 'corner', 'modular']):
                                        if '2 seat' in product_text.lower():
                                            size_info = "2 Seater"
                                        elif '3 seat' in product_text.lower():
                                            size_info = "3 Seater"
                                        elif '4 seat' in product_text.lower():
                                            size_info = "4 Seater"
                                        elif 'corner' in product_text.lower():
                                            size_info = "Corner"
                                        elif 'modular' in product_text.lower():
                                            size_info = "Modular"
                                    
                                    # Look for style information
                                    if any(style in product_text.lower() for style in ['modern', 'contemporary', 'traditional', 'classic', 'luxury', 'premium']):
                                        for style in ['modern', 'contemporary', 'traditional', 'classic', 'luxury', 'premium']:
                                            if style in product_text.lower():
                                                style_info = style.title()
                                                break
                                    
                                    # Look for color information
                                    if any(color in product_text.lower() for color in ['beige', 'brown', 'grey', 'gray', 'white', 'black', 'navy', 'blue']):
                                        for color in ['beige', 'brown', 'grey', 'gray', 'white', 'black', 'navy', 'blue']:
                                            if color in product_text.lower():
                                                color_info = color.title()
                                                break
                                    
                                    # Look for special features
                                    if 'recliner' in product_text.lower():
                                        special_features.append('Recliner')
                                    if 'storage' in product_text.lower():
                                        special_features.append('Storage')
                                    if 'power' in product_text.lower():
                                        special_features.append('Power')
                                    
                                    # CREATE INTELLIGENT TITLE BASED ON SEARCH INTENT
                                    # Prioritize what customers actually search for
                                    search_intent_keywords = []
                                    
                                    # Add size if it's a key differentiator
                                    if size_info and size_info in ['2 Seater', '3 Seater', '4 Seater', 'Corner']:
                                        search_intent_keywords.append(size_info)
                                    
                                    # Add material (but only if it's a key selling point)
                                    if material in ['leather', 'fabric', 'oak', 'wood']:
                                        search_intent_keywords.append(f"{material.title()}")
                                    
                                    # Add product type
                                    search_intent_keywords.append(f"{product_type.title()}")
                                    
                                    # Add special features if they're important
                                    if special_features:
                                        search_intent_keywords.extend(special_features[:1])  # Limit to 1 special feature
                                    
                                    # Create optimized title with search intent
                                    if search_intent_keywords:
                                        intent_keywords = " ".join(search_intent_keywords)
                                        optimized_title = f"{intent_keywords} | {product_title}"
                                        title_reasoning = f"AI optimization: Prioritize '{intent_keywords}' - matches customer search intent for {product_type} with {material} material"
                                        priority_score += 25
                                    
                                    # Add brand if not prominent
                                    if brand and brand.lower() not in product_title.lower():
                                        optimized_title = f"{optimized_title} | {brand}"
                                        title_reasoning += f" - Added brand '{brand}' for authority"
                                        priority_score += 10
                                    
                                    # Description optimization based on search intent
                                    if product_type and material:
                                        # Create description that matches search intent
                                        intent_desc = f"{product_desc} "
                                        if size_info:
                                            intent_desc += f"Perfect {size_info.lower()} {product_type} "
                                        if style_info:
                                            intent_desc += f"in {style_info.lower()} style "
                                        if color_info:
                                            intent_desc += f"in {color_info.lower()} color. "
                                        intent_desc += f"Premium {material.title()} {product_type.title()} from {brand if brand else 'Oak Furnitureland'} - Quality furniture for modern homes."
                                        
                                        optimized_desc = intent_desc
                                        description_reasoning = f"AI optimization: Enhanced description with search intent keywords - {size_info if size_info else material.title()} {product_type.title()}"
                                        priority_score += 15
                                    
                                    # Set impact level
                                    if priority_score >= 30:
                                        expected_impact = "MEDIUM"
                                    else:
                                        expected_impact = "LOW"
                                else:
                                    # Material already prominent - no optimization needed
                                    title_reasoning = f"AI analysis: '{material.title()}' already prominent in title - no optimization needed"
                                    
                            else:
                                # Fallback - use search volume data strategically even without direct relevance
                                # Look for high-volume furniture keywords that could be relevant
                                if df_seo is not None:
                                    try:
                                        # Get high-volume furniture keywords
                                        high_volume_furniture = df_seo[
                                            (df_seo['search_volume'] > 500) & 
                                            (df_seo['search_volume'] < 5000) &  # Not too competitive
                                            (df_seo['keyword'].str.contains('|'.join(['sofa', 'chair', 'table', 'furniture', 'oak']), case=False, na=False))
                                        ].sort_values('search_volume', ascending=False)
                                        
                                        if not high_volume_furniture.empty:
                                            # Use the highest volume relevant keyword
                                            best_keyword = high_volume_furniture.iloc[0]['keyword']
                                            search_volume = high_volume_furniture.iloc[0]['search_volume']
                                            
                                            optimized_title = f"{best_keyword.title()} | {product_title}"
                                            title_reasoning = f"AI optimization: Added high-volume keyword '{best_keyword}' ({search_volume:,} searches) - strategic opportunity"
                                            priority_score += 30
                                            expected_impact = "MEDIUM"
                                            
                                            # Enhanced description
                                            optimized_desc = f"{product_desc} {best_keyword.title()} from Oak Furnitureland - Quality furniture with free delivery."
                                            description_reasoning = f"AI optimization: Enhanced with high-volume keyword '{best_keyword}' for better search visibility"
                                            priority_score += 15
                                        else:
                                            # Fallback - basic title structure optimization
                                            words = product_title.split()
                                            if len(words) > 8:  # Title too long
                                                # Move key words to front
                                                key_words = []
                                                remaining_words = []
                                                
                                                for word in words:
                                                    if word.lower() in ['oak', 'furniture', 'sofa', 'chair', 'table', 'bed', 'dining', 'living', 'office']:
                                                        key_words.append(word)
                                                    else:
                                                        remaining_words.append(word)
                                                
                                                if key_words:
                                                    optimized_title = f"{' '.join(key_words)} | {' '.join(remaining_words)}"
                                                    title_reasoning = f"AI optimization: Restructured title to prioritize key furniture terms - improved readability and SEO"
                                                    priority_score += 15
                                                    expected_impact = "LOW"
                                            
                                            # Basic description enhancement
                                            if len(product_desc) < 100:  # Description too short
                                                optimized_desc = f"{product_desc} Quality furniture from Oak Furnitureland - Free delivery and expert customer service."
                                                description_reasoning = f"AI optimization: Enhanced short description with trust signals and brand mention"
                                                priority_score += 10
                                                expected_impact = "LOW"
                                    except KeyError:
                                        # search_volume column doesn't exist, use basic optimization
                                        words = product_title.split()
                                        if len(words) > 8:  # Title too long
                                            # Move key words to front
                                            key_words = []
                                            remaining_words = []
                                            
                                            for word in words:
                                                if word.lower() in ['oak', 'furniture', 'sofa', 'chair', 'table', 'bed', 'dining', 'living', 'office']:
                                                    key_words.append(word)
                                                else:
                                                    remaining_words.append(word)
                                            
                                            if key_words:
                                                optimized_title = f"{' '.join(key_words)} | {' '.join(remaining_words)}"
                                                title_reasoning = f"AI optimization: Restructured title to prioritize key furniture terms - improved readability and SEO"
                                                priority_score += 15
                                                expected_impact = "LOW"
                                        
                                        # Basic description enhancement
                                        if len(product_desc) < 100:  # Description too short
                                            optimized_desc = f"{product_desc} Quality furniture from Oak Furnitureland - Free delivery and expert customer service."
                                            description_reasoning = f"AI optimization: Enhanced short description with trust signals and brand mention"
                                            priority_score += 10
                                            expected_impact = "LOW"
                                else:
                                    # No SEOMonitor data - basic optimization
                                    title_reasoning = "AI optimization: No SEOMonitor data available - basic title structure optimization"
                                    expected_impact = "LOW"
                        
                        # 5. Add competitor analysis using SEOMonitor data
                        competitor_insights = ""
                        if df_seo is not None:
                            try:
                                # Find keywords where competitors might be ranking better
                                competitor_keywords = df_seo[
                                    (df_seo['search_volume'] > 1000) & 
                                    (df_seo['position'] > 20) &
                                    (df_seo['keyword'].str.contains('|'.join(['sofa', 'chair', 'table', 'furniture']), case=False, na=False))
                                ]
                                
                                if not competitor_keywords.empty:
                                    competitor_insights = f" | Competitor opportunity: {competitor_keywords.iloc[0]['keyword']} ({competitor_keywords.iloc[0]['search_volume']:,} searches)"
                                    priority_score += 20
                            except KeyError:
                                # search_volume column doesn't exist, skip competitor analysis
                                pass
                        
                        # 6. Add Sitebulb insights if available
                        if df_sitebulb is not None:
                            # Look for technical issues affecting this product
                            product_url = product.get('link', '')
                            if product_url:
                                # Find matching page in Sitebulb data
                                matching_pages = df_sitebulb[df_sitebulb['URL'].str.contains(product_url.split('/')[-1], na=False)]
                                if not matching_pages.empty:
                                    page_data = matching_pages.iloc[0]
                                    
                                    # Check for technical issues
                                    if page_data.get('Status Code', 200) != 200:
                                        title_reasoning += f" | Fix {page_data.get('Status Code')} error"
                                        priority_score += 10
                                    
                                    if page_data.get('Title Tag Length', 0) > 60:
                                        title_reasoning += " | Title too long"
                                        priority_score += 5
                                    
                                    if page_data.get('Meta Description Length', 0) > 160:
                                        description_reasoning += " | Description too long"
                                        priority_score += 5
                        
                        # Store recommendation
                        recommendations.append({
                            'product_id': product_id,
                            'current_title': product_title,
                            'optimized_title': optimized_title,
                            'current_description': product_desc,
                            'optimized_description': optimized_desc,
                            'priority_score': priority_score,
                            'expected_impact': expected_impact,
                            'title_reasoning': title_reasoning + competitor_insights,
                            'description_reasoning': description_reasoning
                        })
                    
                    # Store recommendations
                    st.session_state['optimization_recommendations'] = recommendations
                    
                    # Clear progress
                    progress_bar.empty()
                    status_text.empty()
                    
                    # Show results
                    st.success(f"✅ Generated intelligent optimizations for {len(recommendations)} products!")
                    
                    # Show summary
                    high_impact = len([r for r in recommendations if r['expected_impact'] == 'HIGH'])
                    medium_impact = len([r for r in recommendations if r['expected_impact'] == 'MEDIUM'])
                    low_impact = len([r for r in recommendations if r['expected_impact'] == 'LOW'])
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("High Impact", high_impact)
                    with col2:
                        st.metric("Medium Impact", medium_impact)
                    with col3:
                        st.metric("Low Impact", low_impact)
                    
                    st.info("💡 Intelligent optimizations complete! Based on actual SEO performance data.")
                    
                    # Show debugging info
                    if recommendations:
                        st.subheader("🔍 Debugging Info")
                        optimized_count = len([r for r in recommendations if r['title_reasoning'] != "No optimization needed" and r['title_reasoning'] != "No relevant keywords with search volume found"])
                        st.write(f"Products with optimizations: {optimized_count}/{len(recommendations)}")
                        
                        # Show search volume data availability
                        if df_seo is not None:
                            st.subheader("📊 SEOMonitor Search Volume Analysis")
                            try:
                                total_keywords = len(df_seo)
                                keywords_with_volume = len(df_seo[df_seo['search_volume'] > 0])
                                avg_search_volume = df_seo['search_volume'].mean()
                                max_search_volume = df_seo['search_volume'].max()
                                
                                col1, col2, col3, col4 = st.columns(4)
                                with col1:
                                    st.metric("Total Keywords", total_keywords)
                                with col2:
                                    st.metric("Keywords with Volume", keywords_with_volume)
                                with col3:
                                    st.metric("Avg Search Volume", f"{avg_search_volume:.0f}")
                                with col4:
                                    st.metric("Max Search Volume", max_search_volume)
                                
                                # Show sample of high-volume keywords
                                high_volume_keywords = df_seo[df_seo['search_volume'] > 1000].head(10)
                                if not high_volume_keywords.empty:
                                    st.write("**High Volume Keywords (>1000 searches):**")
                                    st.dataframe(high_volume_keywords[['keyword', 'search_volume', 'position']])
                                
                                # Show easy win opportunities
                                easy_wins = df_seo[
                                    (df_seo['search_volume'] > 300) & 
                                    (df_seo['search_volume'] < 2000) & 
                                    (df_seo['position'] > 30) &
                                    (df_seo['difficulty'] < 40)
                                ].sort_values('search_volume', ascending=False).head(5)
                                
                                if not easy_wins.empty:
                                    st.write("**Easy Win Opportunities (low difficulty, good volume):**")
                                    st.dataframe(easy_wins[['keyword', 'search_volume', 'position', 'difficulty']])
                            except KeyError:
                                st.warning("⚠️ SEOMonitor data doesn't have 'search_volume' column. Available columns:")
                                st.write(list(df_seo.columns))
                                st.info("💡 The optimization logic will use AI fallback instead of search volume data.")
                        
                        # Show sample of what was found
                        sample_recs = [r for r in recommendations if r['title_reasoning'] not in ["No optimization needed", "No relevant keywords with search volume found"]][:3]
                        if sample_recs:
                            st.write("Sample optimizations:")
                            for rec in sample_recs:
                                st.write(f"- {rec['title_reasoning']}")
                        else:
                            st.warning("⚠️ No optimizations found - this could mean:")
                            st.write("• Keywords have zero search volume")
                            st.write("• Keywords are not semantically relevant to products")
                            st.write("• SEOMonitor data extraction issues")
                        
                        # Show AI intelligence usage
                        ai_optimizations = len([r for r in recommendations if "AI optimization:" in r['title_reasoning']])
                        if ai_optimizations > 0:
                            st.info(f"🤖 AI Intelligence used for {ai_optimizations} products (when SEOMonitor data wasn't sufficient)")
                        
                        # Show A/B testing suggestions
                        ab_test_candidates = [r for r in recommendations if r['expected_impact'] in ['HIGH', 'MEDIUM'] and 'EASY WIN' in r['title_reasoning']]
                        if ab_test_candidates:
                            st.subheader("🧪 A/B Testing Suggestions")
                            st.write(f"Found {len(ab_test_candidates)} high-impact optimizations perfect for A/B testing:")
                            for rec in ab_test_candidates[:3]:  # Show top 3
                                st.write(f"• **{rec['current_title'][:50]}...** → **{rec['optimized_title'][:50]}...**")
                                st.write(f"  *Reasoning: {rec['title_reasoning']}*")
                                st.write("---")
            else:
                st.error("❌ SEOMonitor data required for AI optimization.")

elif page == "Export Optimized Feed":
    st.header("📤 Export Optimized GMC Feed")
    
    if st.session_state['gmc_feed'] is None:
        st.warning("⚠️ Please upload GMC feed data first.")
    else:
        df_gmc = st.session_state['gmc_feed']
        recommendations = st.session_state.get('optimization_recommendations', [])
        
        st.subheader("📊 Export Options")
        
        # Export original feed
        csv_original = df_gmc.to_csv(index=False)
        st.download_button(
            label="Download Original CSV",
            data=csv_original,
            file_name=f"original_{st.session_state.get('gmc_file', 'gmc_feed')}.csv",
            mime="text/csv"
        )
        
        # Export optimized feed
        if recommendations:
            st.markdown("---")
            st.subheader("🚀 Optimized Feed Export")
            
            # Create optimized DataFrame with proper column structure
            optimized_data = []
            for rec in recommendations:
                # Find original product data
                try:
                    if 'id' in df_gmc.columns:
                        original_product = df_gmc[df_gmc['id'] == rec['product_id']].iloc[0]
                    else:
                        # Fallback to index-based lookup
                        product_index = int(rec['product_id'].split('_')[1]) if '_' in rec['product_id'] else 0
                        original_product = df_gmc.iloc[product_index]
                except:
                    # If we can't find the product, skip it
                    continue
                
                # Create optimized product row with proper column structure
                optimized_row = original_product.to_dict()
                
                # Add optimization columns NEXT TO original columns
                # Insert optimized title after original title
                title_index = list(optimized_row.keys()).index('title') + 1
                optimized_row = {k: v for i, (k, v) in enumerate(optimized_row.items())}
                
                # Add the optimization data
                optimized_row['optimized_title'] = rec['optimized_title']
                optimized_row['title_reasoning'] = rec['title_reasoning']
                optimized_row['optimized_description'] = rec['optimized_description']
                optimized_row['description_reasoning'] = rec['description_reasoning']
                optimized_row['optimization_priority'] = rec['priority_score']
                optimized_row['expected_impact'] = rec['expected_impact']
                
                optimized_data.append(optimized_row)
            
            df_optimized = pd.DataFrame(optimized_data)
            
            # Export optimized CSV
            csv_optimized = df_optimized.to_csv(index=False)
            st.download_button(
                label="⬇️ Download Optimized CSV (with reasons)",
                data=csv_optimized,
                file_name=f"optimized_{st.session_state.get('gmc_file', 'gmc_feed')}.csv",
                mime="text/csv"
            )
            
            # Export optimized Excel (with fallback)
            try:
                import io
                output = io.BytesIO()
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    df_optimized.to_excel(writer, sheet_name='Optimized Feed', index=False)
                
                st.download_button(
                    label="⬇️ Download Optimized XLSX (with reasons)",
                    data=output.getvalue(),
                    file_name=f"optimized_{st.session_state.get('gmc_file', 'gmc_feed')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            except ImportError:
                st.warning("⚠️ Excel export requires openpyxl package. CSV download available above.")
                st.info("💡 To enable Excel export, add 'openpyxl' to requirements.txt")
            
            # Show summary
            st.success(f"✅ Ready to export {len(optimized_data)} optimized products!")
            
            # Show sample of optimizations with proper columns
            st.subheader("📋 Sample Optimizations")
            # Show key columns: original title, optimized title, original description, optimized description, reasoning
            sample_columns = ['title', 'optimized_title', 'title_reasoning', 'description', 'optimized_description', 'description_reasoning', 'expected_impact']
            available_columns = [col for col in sample_columns if col in df_optimized.columns]
            sample_df = df_optimized[available_columns].head(5)
            st.dataframe(sample_df)
            
        else:
            st.warning("⚠️ No optimizations found. Please run 'Strategic Optimization' first.")

# Footer
st.markdown("---")
st.markdown("🛒 Oak Furniture Land GMC Feed Optimizer | Strategic SEO + PPC Integration")