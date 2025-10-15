import streamlit as st
import pandas as pd
import numpy as np
import requests
import json
import configparser
import os

st.set_page_config(
    page_title="Oak Furniture Land GMC Feed Optimizer",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': None
    }
)

# Hide all Streamlit branding
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
    
    /* Hide Streamlit branding in sidebar */
    .stSidebar > div:first-child {
        display: none;
    }
    
    /* Hide Streamlit menu */
    .stApp > div:first-child {
        display: none;
    }
    
    /* Hide Streamlit URL bar */
    .stApp > div[data-testid="stHeader"] {
        display: none;
    }
    
    /* Hide Streamlit status */
    .stApp > div[data-testid="stStatusWidget"] {
        display: none;
    }
    
    /* Custom styling */
    .main > div {
        padding-top: 0rem;
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
    # Define valid credentials
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
    st.markdown("**Available Accounts:**")
    st.markdown("- Username: `oakfurniture` | Password: `OFL2024!`")
    st.markdown("- Username: `admin` | Password: `Admin123!`")
    st.markdown("- Username: `seo` | Password: `SEO2024!`")
    
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

# Load configuration
@st.cache_data
def load_config():
    config = configparser.ConfigParser()
    config.read('config_oak_furniture.ini')
    return config

# Initialize session state
if 'sitebulb_data' not in st.session_state:
    st.session_state['sitebulb_data'] = None
if 'seomonitor_data' not in st.session_state:
    st.session_state['seomonitor_data'] = None
if 'product_data' not in st.session_state:
    st.session_state['product_data'] = None
if 'gmc_feed' not in st.session_state:
    st.session_state['gmc_feed'] = None

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Choose a section", [
    "GMC Feed Strategy", 
    "GMC Feed Upload", 
    "Sitebulb Upload", 
    "SEOMonitor API", 
    "Search Volume Analysis",
    "PPC Intelligence",
    "Strategic Optimization",
    "Export Optimized Feed"
])

if page == "GMC Feed Strategy":
    st.header("🛒 GMC Feed Optimization Strategy")
    
    st.subheader("📊 Search Volume Integration")
    st.write("""
    **Strategic Approach:**
    - **High-volume keywords** → Prioritize products with high search demand
    - **Seasonal trends** → Adjust product titles/descriptions for peak seasons
    - **Long-tail opportunities** → Target specific furniture searches
    - **Competitor gaps** → Find keywords competitors aren't targeting
    """)
    
    st.subheader("💰 PPC Intelligence Integration")
    st.write("""
    **Strategic Approach:**
    - **Bid competitiveness** → Optimize products expensive to bid on organically
    - **Quality Score impact** → Improve landing page relevance for better ad performance
    - **Conversion data** → Focus on products with high conversion rates
    - **ROI optimization** → Balance organic vs paid search strategy
    """)
    
    st.subheader("🎯 GMC Feed Optimization Focus")
    st.write("""
    **Key Areas:**
    1. **Product Titles** → Include high-volume keywords + furniture-specific terms
    2. **Descriptions** → Target long-tail searches + conversion-focused copy
    3. **Categories** → Optimize for Google Shopping categories
    4. **Attributes** → Use structured data for better visibility
    5. **Images** → Optimize for visual search + mobile performance
    """)

elif page == "GMC Feed Upload":
    st.header("🛒 Upload GMC Feed Data")
    
    # File upload
    uploaded_file = st.file_uploader(
        "Upload your GMC feed file (CSV, Excel, XML)",
        type=['csv', 'xlsx', 'xls', 'xml'],
        help="Upload your Google Merchant Center product feed"
    )
    
    if uploaded_file is not None:
        try:
            # Read the file
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            elif uploaded_file.name.endswith('.xml'):
                st.info("XML files will be processed in the next update")
                st.stop()
            else:
                df = pd.read_excel(uploaded_file)
            
            st.success(f"✅ GMC feed uploaded! {len(df)} products loaded.")
            
            # Store in session state
            st.session_state['gmc_feed'] = df
            st.session_state['gmc_file'] = uploaded_file.name
            
            # Show data preview
            st.subheader("📊 GMC Feed Preview")
            st.dataframe(df.head(10))
            
            # Show data info
            st.subheader("📈 Feed Analysis")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Products", len(df))
            with col2:
                st.metric("Columns", len(df.columns))
            with col3:
                st.metric("Missing Values", df.isnull().sum().sum())
            
            # GMC-specific analysis
            st.subheader("🛒 GMC Feed Quality Analysis")
            gmc_fields = ['id', 'title', 'description', 'price', 'availability', 'condition', 'brand', 'gtin', 'mpn', 'image_link']
            found_fields = [field for field in gmc_fields if field in df.columns]
            missing_fields = [field for field in gmc_fields if field not in df.columns]
            
            if found_fields:
                st.success(f"✅ Found GMC fields: {', '.join(found_fields)}")
            if missing_fields:
                st.warning(f"⚠️ Missing GMC fields: {', '.join(missing_fields)}")
            
            # Product category analysis
            if 'product_type' in df.columns:
                st.subheader("📂 Product Categories")
                category_counts = df['product_type'].value_counts().head(10)
                st.bar_chart(category_counts)
                
        except Exception as e:
            st.error(f"❌ Error reading file: {str(e)}")

elif page == "Sitebulb Upload":
    st.header("📁 Upload Sitebulb Crawl Data")
    
    # File upload
    uploaded_file = st.file_uploader(
        "Upload your Sitebulb crawl report (CSV, Excel)",
        type=['csv', 'xlsx', 'xls'],
        help="Upload your Sitebulb crawl export file"
    )
    
    if uploaded_file is not None:
        try:
            # Read the file
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            
            st.success(f"✅ Sitebulb data uploaded! {len(df)} records loaded.")
            
            # Store in session state
            st.session_state['sitebulb_data'] = df
            st.session_state['sitebulb_file'] = uploaded_file.name
            
            # Show data preview
            st.subheader("📊 Sitebulb Data Preview")
            st.dataframe(df.head(10))
                
        except Exception as e:
            st.error(f"❌ Error reading file: {str(e)}")

elif page == "SEOMonitor API":
    st.header("📈 SEOMonitor API Integration")
    
    st.subheader("🔑 API Configuration")
    
    # Try to load config
    try:
        config = load_config()
        api_key = config['SEOMonitor']['api_key']
        campaign_id = config['SEOMonitor']['campaign_id']
        brand_name = config['Brand']['name']
        
        st.success(f"✅ API configured for {brand_name}")
        st.info(f"Campaign ID: {campaign_id}")
        
    except Exception as e:
        st.error(f"❌ Config file not found: {str(e)}")
        api_key = None
        campaign_id = None
    
    if api_key and campaign_id:
        st.subheader("📊 Available Data")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🔍 Fetch Keyword Rankings"):
                # Create logging container
                log_container = st.empty()
                
                with st.spinner("🔄 Fetching keyword data..."):
                    # Use the working API endpoint from your files
                    url = "https://apigw.seomonitor.com/v3/rank-tracker/v3.0/keywords"
                    
                    # Correct headers based on working code
                    headers = {
                        "Authorization": api_key,  # Direct API key, not Bearer
                        "X-Token": api_key,        # Some tenants expect X-Token
                        "Accept": "application/json"
                    }
                    
                    # Required date parameters
                    from datetime import datetime, timedelta
                    end_date = datetime.today().date()
                    start_date = end_date - timedelta(days=30)
                    
                    params = {
                        "campaign_id": campaign_id,
                        "start_date": start_date.isoformat(),
                        "end_date": end_date.isoformat(),
                        "include_all_groups": "true",
                        "limit": 200,
                        "offset": 0
                    }
                    
                    # Log the request details
                    log_container.write("🔍 **API Request Details:**")
                    log_container.write(f"**URL:** {url}")
                    log_container.write(f"**Headers:** {headers}")
                    log_container.write(f"**Params:** {params}")
                    log_container.write("---")
                    
                    try:
                        log_container.write("📡 **Making API request...**")
                        response = requests.get(url, headers=headers, params=params, timeout=30)
                        
                        log_container.write(f"📊 **Response Status:** {response.status_code}")
                        log_container.write(f"📊 **Response Headers:** {dict(response.headers)}")
                        
                        if response.status_code == 200:
                            log_container.write("✅ **Success! Processing response...**")
                            data = response.json()
                            
                            log_container.write(f"📋 **Response Type:** {type(data)}")
                            log_container.write(f"📋 **Response Length:** {len(data) if isinstance(data, (list, dict)) else 'N/A'}")
                            
                            # Show first few items for debugging
                            if isinstance(data, list) and data:
                                log_container.write("📋 **Sample Response Items:**")
                                log_container.json(data[:2])
                            elif isinstance(data, dict):
                                log_container.write("📋 **Response Structure:**")
                                log_container.json(data)
                            
                            # Process the data based on working code structure
                            if isinstance(data, list) and data:
                                keywords_data = []
                                log_container.write(f"🔄 **Processing {len(data)} items...**")
                                
                                for i, item in enumerate(data):
                                    keyword = item.get("keyword", "").strip()
                                    if keyword:
                                        search_data = item.get("search_data", {})
                                        keywords_data.append({
                                            'keyword': keyword,
                                            'position': item.get("position", 0),
                                            'volume': search_data.get("search_volume", 0),
                                            'difficulty': search_data.get("difficulty", 0),
                                            'yoy': search_data.get("year_over_year", 0),
                                            'url': item.get("url", "")
                                        })
                                    
                                    # Log progress every 50 items
                                    if (i + 1) % 50 == 0:
                                        log_container.write(f"🔄 **Processed {i + 1}/{len(data)} items...**")
                                
                                log_container.write(f"✅ **Processed {len(keywords_data)} keywords successfully!**")
                                
                                if keywords_data:
                                    df_keywords = pd.DataFrame(keywords_data)
                                    st.session_state['seomonitor_data'] = df_keywords
                                    
                                    st.success(f"✅ Fetched {len(df_keywords)} keywords!")
                                    st.dataframe(df_keywords.head(10))
                                    
                                    # Show summary stats
                                    col1, col2, col3 = st.columns(3)
                                    with col1:
                                        st.metric("Total Keywords", len(df_keywords))
                                    with col2:
                                        avg_volume = df_keywords['volume'].mean()
                                        st.metric("Avg Search Volume", f"{avg_volume:.0f}")
                                    with col3:
                                        high_volume = len(df_keywords[df_keywords['volume'] > 1000])
                                        st.metric("High Volume (>1K)", high_volume)
                                    
                                    # Clear the log container after success
                                    log_container.empty()
                                else:
                                    st.warning("No keyword data found in response")
                                    log_container.write("⚠️ **No valid keywords found in response**")
                                    log_container.json(data[:2] if data else "Empty response")
                            else:
                                st.warning("No keyword data found in response")
                                log_container.write("⚠️ **Unexpected response format**")
                                log_container.json(data if isinstance(data, dict) else "Unexpected response format")
                        else:
                            st.error(f"❌ API Error: {response.status_code}")
                            log_container.write(f"❌ **API Error Details:**")
                            log_container.write(f"**Status Code:** {response.status_code}")
                            log_container.write(f"**Response Text:** {response.text}")
                            log_container.write(f"**Response Headers:** {dict(response.headers)}")
                            
                    except Exception as e:
                        st.error(f"❌ API Error: {str(e)}")
                        log_container.write(f"❌ **Exception Details:**")
                        log_container.write(f"**Error Type:** {type(e).__name__}")
                        log_container.write(f"**Error Message:** {str(e)}")
                        log_container.write("**Possible issues:**")
                        log_container.write("- Network connection problem")
                        log_container.write("- API key might be incorrect")
                        log_container.write("- Campaign ID might not exist")
                        log_container.write("- API endpoint might be down")

elif page == "Search Volume Analysis":
    st.header("📊 Search Volume Analysis")
    
    if st.session_state['seomonitor_data'] is None:
        st.warning("⚠️ Please fetch SEOMonitor data first.")
    else:
        df_seo = st.session_state['seomonitor_data']
        
        st.subheader("🔍 Keyword Volume Analysis")
        
        # Volume distribution
        if 'volume' in df_seo.columns:
            st.subheader("📈 Search Volume Distribution")
            volume_ranges = pd.cut(df_seo['volume'], bins=[0, 100, 1000, 10000, float('inf')], 
                                 labels=['Low (0-100)', 'Medium (100-1K)', 'High (1K-10K)', 'Very High (10K+)'])
            volume_counts = volume_ranges.value_counts()
            st.bar_chart(volume_counts)
        
        # High-volume opportunities
        if 'volume' in df_seo.columns and 'position' in df_seo.columns:
            st.subheader("🎯 High-Volume Opportunities")
            high_volume = df_seo[(df_seo['volume'] > 1000) & (df_seo['position'] > 10)]
            if len(high_volume) > 0:
                st.write(f"Found {len(high_volume)} high-volume keywords ranking below position 10")
                st.dataframe(high_volume[['keyword', 'volume', 'position']].head(10))
            else:
                st.info("No high-volume opportunities found")
        
        # Furniture-specific analysis
        st.subheader("🪑 Furniture-Specific Keywords")
        furniture_keywords = df_seo[df_seo['keyword'].str.contains('furniture|sofa|table|chair|bed|wardrobe', case=False, na=False)]
        if len(furniture_keywords) > 0:
            st.write(f"Found {len(furniture_keywords)} furniture-related keywords")
            st.dataframe(furniture_keywords[['keyword', 'volume', 'position']].head(10))

elif page == "PPC Intelligence":
    st.header("💰 PPC Intelligence Integration")
    
    st.subheader("🎯 PPC Strategy for GMC Feed")
    
    # Mock PPC data analysis
    st.write("""
    **PPC Intelligence Integration:**
    
    1. **Bid Competitiveness Analysis**
       - High CPC keywords → Focus organic optimization
       - Low CPC keywords → Consider PPC campaigns
       - Seasonal spikes → Adjust feed for peak periods
    
    2. **Quality Score Optimization**
       - Landing page relevance → Improve product descriptions
       - Ad relevance → Optimize product titles
       - Expected CTR → A/B test different titles
    
    3. **Conversion Data Integration**
       - High-converting products → Prioritize in feed
       - Low-converting products → Improve descriptions
       - Cart abandonment → Optimize product pages
    """)
    
    # Sample PPC recommendations
    st.subheader("💡 PPC Recommendations")
    
    recommendations = [
        {
            "Product": "Oak Dining Table",
            "Current CPC": "£2.50",
            "Organic Position": 15,
            "Recommendation": "Focus on organic optimization - high CPC makes PPC expensive",
            "Strategy": "Improve title with 'solid oak dining table' + optimize for long-tail keywords"
        },
        {
            "Product": "Leather Sofa",
            "Current CPC": "£0.80",
            "Organic Position": 8,
            "Recommendation": "Consider PPC campaign - low CPC + good organic position",
            "Strategy": "Run shopping ads to capture additional traffic"
        }
    ]
    
    for rec in recommendations:
        with st.expander(f"🪑 {rec['Product']}"):
            st.write(f"**Current CPC:** {rec['Current CPC']}")
            st.write(f"**Organic Position:** {rec['Organic Position']}")
            st.write(f"**Recommendation:** {rec['Recommendation']}")
            st.write(f"**Strategy:** {rec['Strategy']}")

elif page == "Strategic Optimization":
    st.header("🎯 Strategic GMC Feed Optimization")
    
    if st.session_state['gmc_feed'] is None:
        st.warning("⚠️ Please upload GMC feed data first.")
    else:
        df_gmc = st.session_state['gmc_feed']
        df_seo = st.session_state.get('seomonitor_data')
        df_sitebulb = st.session_state.get('sitebulb_data')
        
        st.subheader("🔍 Data Sources Available")
        col1, col2, col3 = st.columns(3)
        with col1:
            if df_seo is not None:
                st.success(f"✅ SEOMonitor: {len(df_seo)} keywords")
            else:
                st.warning("⚠️ No SEOMonitor data")
        with col2:
            if df_sitebulb is not None:
                st.success(f"✅ Sitebulb: {len(df_sitebulb)} pages")
            else:
                st.warning("⚠️ No Sitebulb data")
        with col3:
            st.success(f"✅ GMC Feed: {len(df_gmc)} products")
        
        # Optimization function
        def optimize_title(title, seo_data=None, sitebulb_data=None):
            """Optimize title based on SEO and Sitebulb data"""
            original_title = title
            optimized_title = title
            justifications = []
            
            # Basic title analysis
            title_length = len(title)
            word_count = len(title.split())
            
            # 1. Length optimization
            if title_length < 60:
                optimized_title += " - Premium Furniture"
                justifications.append("Added 'Premium Furniture' for category relevance and length optimization")
            elif title_length > 150:
                # Truncate intelligently
                words = optimized_title.split()
                if len(words) > 20:
                    optimized_title = ' '.join(words[:20]) + "..."
                    justifications.append("Truncated to optimal length (150 chars) to prevent Google truncation")
            
            # 2. Material emphasis (furniture-specific)
            if 'oak' in optimized_title.lower() and 'solid oak' not in optimized_title.lower():
                optimized_title = optimized_title.replace('oak', 'solid oak')
                justifications.append("Enhanced material description: 'oak' → 'solid oak' for better search visibility")
            
            # 3. Add dimensions if missing
            if not any(word in optimized_title.lower() for word in ['seater', 'ft', 'inch', 'cm', 'mm', 'seat']):
                if 'sofa' in optimized_title.lower() or 'settee' in optimized_title.lower():
                    optimized_title += " - 3 Seater"
                    justifications.append("Added seating capacity for furniture-specific searches")
                elif 'table' in optimized_title.lower():
                    optimized_title += " - 6 Seater"
                    justifications.append("Added table capacity for dining furniture searches")
            
            # 4. Quality indicators
            if not any(word in optimized_title.lower() for word in ['premium', 'quality', 'handcrafted', 'solid']):
                optimized_title += " - High Quality"
                justifications.append("Added quality indicator to improve perceived value and search ranking")
            
            # 5. SEO keyword integration (if SEOMonitor data available)
            if seo_data is not None and len(seo_data) > 0:
                # Find high-volume furniture keywords
                furniture_keywords = seo_data[seo_data['keyword'].str.contains('furniture|sofa|table|chair|bed|wardrobe', case=False, na=False)]
                if len(furniture_keywords) > 0:
                    high_volume_keywords = furniture_keywords[furniture_keywords['volume'] > 1000].sort_values('volume', ascending=False)
                    if len(high_volume_keywords) > 0:
                        # Add top keyword if not already present
                        top_keyword = high_volume_keywords.iloc[0]['keyword']
                        if top_keyword.lower() not in optimized_title.lower():
                            optimized_title += f" - {top_keyword.title()}"
                            justifications.append(f"Integrated high-volume keyword '{top_keyword}' (vol: {high_volume_keywords.iloc[0]['volume']})")
            
            # 6. Brand positioning
            if 'oak furniture land' not in optimized_title.lower():
                optimized_title += " - Oak Furniture Land"
                justifications.append("Added brand name for brand recognition and local SEO")
            
            return optimized_title, justifications
        
        def optimize_description(description, seo_data=None, sitebulb_data=None):
            """Optimize description based on SEO and Sitebulb data"""
            original_desc = description
            optimized_desc = description
            justifications = []
            
            # Basic description analysis
            desc_length = len(description)
            
            # 1. Length optimization
            if desc_length < 150:
                optimized_desc += " Crafted from premium materials with attention to detail. "
                justifications.append("Extended description for better search engine understanding")
            elif desc_length > 500:
                # Truncate intelligently
                optimized_desc = optimized_desc[:500] + "..."
                justifications.append("Truncated to optimal length to prevent search engine truncation")
            
            # 2. Add furniture-specific details
            if 'dimensions' not in optimized_desc.lower():
                optimized_desc += " Dimensions and specifications available. "
                justifications.append("Added dimensions reference for furniture-specific searches")
            
            if 'material' not in optimized_desc.lower() and 'oak' in optimized_desc.lower():
                optimized_desc += " Made from solid oak wood. "
                justifications.append("Specified material details for material-based searches")
            
            if 'care' not in optimized_desc.lower():
                optimized_desc += " Easy to maintain and clean. "
                justifications.append("Added care instructions for furniture buyers")
            
            # 3. SEO keyword integration
            if seo_data is not None and len(seo_data) > 0:
                furniture_keywords = seo_data[seo_data['keyword'].str.contains('furniture|sofa|table|chair|bed|wardrobe', case=False, na=False)]
                if len(furniture_keywords) > 0:
                    medium_volume_keywords = furniture_keywords[(furniture_keywords['volume'] > 100) & (furniture_keywords['volume'] < 1000)]
                    if len(medium_volume_keywords) > 0:
                        # Add 2-3 medium volume keywords
                        keywords_to_add = medium_volume_keywords.head(3)['keyword'].tolist()
                        for keyword in keywords_to_add:
                            if keyword.lower() not in optimized_desc.lower():
                                optimized_desc += f" {keyword.title()}. "
                        justifications.append(f"Integrated medium-volume keywords: {', '.join(keywords_to_add)}")
            
            return optimized_desc, justifications
        
        # Process ALL products
        if st.button("🚀 Optimize All Products", type="primary"):
            with st.spinner("🔄 Optimizing all products..."):
                optimized_products = []
                
                for index, row in df_gmc.iterrows():
                    product_id = row.get('id', f"product_{index+1}")
                    original_title = row.get('title', '')
                    original_description = row.get('description', '')
                    
                    # Optimize title
                    optimized_title, title_justifications = optimize_title(
                        original_title, 
                        df_seo, 
                        df_sitebulb
                    )
                    
                    # Optimize description
                    optimized_description, desc_justifications = optimize_description(
                        original_description, 
                        df_seo, 
                        df_sitebulb
                    )
                    
                    # Combine all justifications
                    all_justifications = title_justifications + desc_justifications
                    justification_text = " | ".join(all_justifications) if all_justifications else "No changes needed"
                    
                    # Create optimized product
                    optimized_product = row.copy()
                    optimized_product['original_title'] = original_title
                    optimized_product['optimized_title'] = optimized_title
                    optimized_product['original_description'] = original_description
                    optimized_product['optimized_description'] = optimized_description
                    optimized_product['optimization_justification'] = justification_text
                    optimized_product['title_changes'] = len(title_justifications)
                    optimized_product['description_changes'] = len(desc_justifications)
                    optimized_product['total_changes'] = len(all_justifications)
                    
                    optimized_products.append(optimized_product)
                
                # Store in session state
                st.session_state['optimized_products'] = pd.DataFrame(optimized_products)
                
                st.success(f"✅ Optimized {len(optimized_products)} products!")
        
        # Show results if optimization completed
        if 'optimized_products' in st.session_state:
            df_optimized = st.session_state['optimized_products']
            
            st.subheader("📊 Optimization Results")
            
            # Summary metrics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Products Optimized", len(df_optimized))
            with col2:
                total_changes = df_optimized['total_changes'].sum()
                st.metric("Total Changes Made", total_changes)
            with col3:
                avg_changes = df_optimized['total_changes'].mean()
                st.metric("Avg Changes per Product", f"{avg_changes:.1f}")
            with col4:
                products_with_changes = len(df_optimized[df_optimized['total_changes'] > 0])
                st.metric("Products Modified", products_with_changes)
            
            # Show sample optimizations
            st.subheader("📝 Sample Optimizations")
            sample_optimized = df_optimized[df_optimized['total_changes'] > 0].head(5)
            
            for index, row in sample_optimized.iterrows():
                with st.expander(f"Product {index+1}: {row['original_title'][:50]}..."):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write("**Original Title:**")
                        st.write(row['original_title'])
                        st.write("**Original Description:**")
                        st.write(row['original_description'][:200] + "...")
                    
                    with col2:
                        st.write("**Optimized Title:**")
                        st.write(row['optimized_title'])
                        st.write("**Optimized Description:**")
                        st.write(row['optimized_description'][:200] + "...")
                    
                    st.write("**Justification:**")
                    st.write(row['optimization_justification'])
            
            # Export options
            st.subheader("📤 Export Optimized Feed")
            
            # Create optimized GMC feed
            optimized_gmc = df_optimized.copy()
            optimized_gmc['title'] = optimized_gmc['optimized_title']
            optimized_gmc['description'] = optimized_gmc['optimized_description']
            
            # Remove optimization columns for clean GMC feed
            export_columns = [col for col in optimized_gmc.columns if not col.startswith(('original_', 'optimized_', 'optimization_', 'title_changes', 'description_changes', 'total_changes'))]
            clean_optimized_feed = optimized_gmc[export_columns]
            
            # Download buttons
            col1, col2, col3 = st.columns(3)
            
            with col1:
                # Optimized GMC Feed
                csv_optimized = clean_optimized_feed.to_csv(index=False)
                st.download_button(
                    label="📥 Download Optimized GMC Feed",
                    data=csv_optimized,
                    file_name="optimized_gmc_feed.csv",
                    mime="text/csv"
                )
            
            with col2:
                # Detailed optimization report
                report_columns = ['id', 'original_title', 'optimized_title', 'original_description', 'optimized_description', 'optimization_justification', 'total_changes']
                detailed_report = df_optimized[report_columns]
                csv_report = detailed_report.to_csv(index=False)
                st.download_button(
                    label="📊 Download Detailed Report",
                    data=csv_report,
                    file_name="optimization_detailed_report.csv",
                    mime="text/csv"
                )
            
            with col3:
                # Justification summary
                justification_summary = df_optimized[['id', 'title', 'optimization_justification', 'total_changes']]
                csv_justification = justification_summary.to_csv(index=False)
                st.download_button(
                    label="📋 Download Justifications",
                    data=csv_justification,
                    file_name="optimization_justifications.csv",
                    mime="text/csv"
                )
            
            # Show full optimization table
            st.subheader("📋 Complete Optimization Table")
            st.dataframe(df_optimized[['id', 'original_title', 'optimized_title', 'optimization_justification', 'total_changes']].head(20))
        
        # Description optimization
        if 'description' in df_gmc.columns:
            st.subheader("📄 Description Optimization")
            
            # Sample description analysis
            sample_descriptions = df_gmc['description'].head(3)
            for i, desc in enumerate(sample_descriptions):
                with st.expander(f"Description {i+1}"):
                    st.write(f"**Current Description:** {desc[:200]}...")
                    
                    # Analysis
                    st.write("**Analysis:**")
                    if len(desc) < 150:
                        st.warning("⚠️ Description too short - missing detail")
                    elif len(desc) > 500:
                        st.warning("⚠️ Description too long - may be truncated")
                    else:
                        st.success("✅ Description length is good")
                    
                    # Recommendations
                    st.write("**Recommendations:**")
                    if 'dimensions' not in desc.lower():
                        st.write("• Add dimensions for furniture-specific searches")
                    if 'material' not in desc.lower():
                        st.write("• Specify materials for material-specific searches")
                    if 'care' not in desc.lower():
                        st.write("• Add care instructions for furniture")
        
        # Category optimization
        if 'product_type' in df_gmc.columns:
            st.subheader("📂 Category Optimization")
            
            # Category analysis
            category_counts = df_gmc['product_type'].value_counts()
            st.write("**Current Categories:**")
            st.bar_chart(category_counts.head(10))
            
            st.write("**Recommendations:**")
            st.write("• Use Google Shopping category taxonomy")
            st.write("• Be specific: 'Furniture > Living Room Furniture > Sofas'")
            st.write("• Avoid generic categories like 'Home & Garden'")

elif page == "Export Optimized Feed":
    st.header("📤 Export Optimized GMC Feed")
    
    if st.session_state['gmc_feed'] is None:
        st.warning("⚠️ Please upload GMC feed data first.")
    else:
        df_gmc = st.session_state['gmc_feed']
        
        st.subheader("📊 Export Options")
        
        # Export original feed
        st.write("**Export Original Feed:**")
        csv_original = df_gmc.to_csv(index=False)
        st.download_button(
            label="Download Original CSV",
            data=csv_original,
            file_name=f"original_{st.session_state.get('gmc_file', 'gmc_feed')}.csv",
            mime="text/csv"
        )
        
        # Export optimized feed
        st.write("**Export Optimized Feed:**")
        st.info("🚧 Optimization features coming soon!")
        
        # Export optimization report
        st.write("**Export Optimization Report:**")
        report = f"""
        GMC Feed Optimization Report
        ===========================
        Total Products: {len(df_gmc)}
        Columns: {len(df_gmc.columns)}
        Missing Values: {df_gmc.isnull().sum().sum()}
        
        Optimization Recommendations:
        - Title optimization: {len(df_gmc)} products
        - Description enhancement: {len(df_gmc)} products
        - Category improvement: {len(df_gmc)} products
        - Image optimization: {len(df_gmc)} products
        """
        
        st.download_button(
            label="Download Optimization Report",
            data=report,
            file_name="gmc_optimization_report.txt",
            mime="text/plain"
        )

# Footer
st.markdown("---")
st.markdown("🛒 Oak Furniture Land GMC Feed Optimizer | Strategic SEO + PPC Integration")