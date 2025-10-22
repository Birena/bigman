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
st.caption("Version 2.0 - AI INTELLIGENCE FALLBACK")

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
                            
                            # 3. LOGICAL OPTIMIZATION DECISIONS BASED ON SEO PATTERNS
                            
                            # TITLE OPTIMIZATION - Based on what works
                            if top_performers:
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
                            
                            # Extract material
                            materials = ['oak', 'wood', 'fabric', 'leather', 'metal', 'glass', 'marble', 'mink', 'velvet', 'cotton', 'linen']
                            for mat in materials:
                                if mat in product_text.lower():
                                    material = mat
                                    break
                            
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
                                # Create intelligent title optimization
                                if product_type == 'sofa' and material:
                                    optimized_title = f"{material.title()} {product_type.title()} | {product_title}"
                                    title_reasoning = f"AI optimization: Prioritize '{material.title()} {product_type.title()}' - high-value keywords for furniture searches"
                                    priority_score += 20
                                    
                                elif product_type == 'table' and material:
                                    optimized_title = f"{material.title()} {product_type.title()} | {product_title}"
                                    title_reasoning = f"AI optimization: Prioritize '{material.title()} {product_type.title()}' - common search terms for furniture"
                                    priority_score += 20
                                    
                                elif product_type == 'chair' and material:
                                    optimized_title = f"{material.title()} {product_type.title()} | {product_title}"
                                    title_reasoning = f"AI optimization: Prioritize '{material.title()} {product_type.title()}' - popular furniture search terms"
                                    priority_score += 20
                                
                                # Add brand if not prominent
                                if brand and brand.lower() not in product_title.lower():
                                    optimized_title = f"{optimized_title} | {brand}"
                                    title_reasoning += f" - Added brand '{brand}' for authority"
                                    priority_score += 10
                                
                                # Description optimization
                                if product_type and material:
                                    optimized_desc = f"{product_desc} Premium {material.title()} {product_type.title()} from {brand if brand else 'Oak Furnitureland'} - Quality furniture for modern homes."
                                    description_reasoning = f"AI optimization: Enhanced description with '{material.title()} {product_type.title()}' keywords and brand authority"
                                    priority_score += 15
                                
                                # Set impact level
                                if priority_score >= 30:
                                    expected_impact = "MEDIUM"
                                else:
                                    expected_impact = "LOW"
                                    
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
                        
                        # 5. Add Sitebulb insights if available
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
                            'title_reasoning': title_reasoning,
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