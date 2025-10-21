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

# Load configuration
@st.cache_data
def load_config():
    config = configparser.ConfigParser()
    config.read('config_oak_furniture.ini')
    return config

# Enhanced SEOMonitor API Integration with Intelligence
def fetch_comprehensive_seomonitor_data():
    """Fetch comprehensive keyword data from SEOMonitor API with intelligence analysis"""
    try:
        # Read config
        config = configparser.ConfigParser()
        config.read('config_oak_furniture.ini')
        api_key = config.get('SEOMonitor', 'api_key')
        campaign_id = config.get('SEOMonitor', 'campaign_id')
        
        # Only use available endpoints - SEOMonitor API v3 only has keywords endpoint for rank tracker
        endpoints = {
            'keywords': f"https://apigw.seomonitor.com/v3/rank-tracker/v3.0/keywords"
        }
        
        headers = {
            'Authorization': api_key,
            'X-Token': api_key,
            'Accept': 'application/json'
        }
        
        # Get comprehensive data (last 90 days for better analysis)
        end_date = datetime.now()
        start_date = end_date - timedelta(days=90)
        
        all_data = {}
        
        # Fetch keyword rankings (traditional + shopping) with pagination
        for endpoint_name, url in endpoints.items():
            try:
                st.write(f"🔍 Fetching {endpoint_name} data (paginated)...")
                page_limit = 200  # typical API page size cap
                offset = 0
                collected_rows = []
                while True:
                    params = {
                        'campaign_id': campaign_id,
                        'start_date': start_date.strftime('%Y-%m-%d'),
                        'end_date': end_date.strftime('%Y-%m-%d'),
                        'include_all_groups': 'true',
                        'limit': page_limit,
                        'offset': offset
                    }
                    response = requests.get(url, headers=headers, params=params)
                    if response.status_code != 200:
                        st.error(f"❌ {endpoint_name} API Error: {response.status_code}")
                        break
                    data = response.json()
                    if not isinstance(data, list) or len(data) == 0:
                        # No more data
                        break
                    collected_rows.extend(data)
                    # Advance pagination
                    fetched_count = len(data)
                    offset += fetched_count
                    # Safety cap to avoid excessive loops
                    if fetched_count < page_limit or offset > 50000:
                        break
                if collected_rows:
                    df_endpoint = pd.DataFrame(collected_rows)
                    all_data[endpoint_name] = df_endpoint
                    st.success(f"✅ {endpoint_name}: {len(df_endpoint)} records (all pages)")
                    
                    # Debug: Show available columns for keywords
                    if endpoint_name == 'keywords' and len(df_endpoint) > 0:
                        st.info(f"🔍 Available columns: {list(df_endpoint.columns)}")
                        if len(df_endpoint) > 0:
                            st.info(f"🔍 Sample data: {df_endpoint.iloc[0].to_dict()}")
                            
                            # Show specific field values
                            sample_row = df_endpoint.iloc[0]
                            st.info(f"🔍 Field values - Volume: {sample_row.get('volume', 'NOT_FOUND')}, Position: {sample_row.get('position', 'NOT_FOUND')}, Difficulty: {sample_row.get('difficulty', 'NOT_FOUND')}")
                            
                            # Show all field names that might contain volume/position data
                            volume_fields = [col for col in df_endpoint.columns if 'volume' in col.lower() or 'search' in col.lower()]
                            position_fields = [col for col in df_endpoint.columns if 'position' in col.lower() or 'rank' in col.lower()]
                            st.info(f"🔍 Volume-related fields: {volume_fields}")
                            st.info(f"🔍 Position-related fields: {position_fields}")
                else:
                    all_data[endpoint_name] = pd.DataFrame()
                    st.warning(f"⚠️ No {endpoint_name} data found")
            except Exception as e:
                st.error(f"❌ Error fetching {endpoint_name}: {str(e)}")
                all_data[endpoint_name] = pd.DataFrame()
        
        # Process and combine all data
        return process_comprehensive_data(all_data, campaign_id)
        
    except Exception as e:
        st.error(f"❌ Error in comprehensive data fetch: {str(e)}")
        return pd.DataFrame()

def process_comprehensive_data(all_data, campaign_id):
    """Process and analyze comprehensive SEOMonitor data"""
    
    # Start with keyword data
    keywords_df = all_data.get('keywords', pd.DataFrame())
    shopping_df = all_data.get('shopping_rankings', pd.DataFrame())
    competitors_df = all_data.get('competitors', pd.DataFrame())
    sov_df = all_data.get('share_of_voice', pd.DataFrame())
    
    if keywords_df.empty and shopping_df.empty:
        st.error("❌ No keyword data available")
        return pd.DataFrame()
    
    # Combine traditional and shopping rankings
    combined_df = pd.concat([keywords_df, shopping_df], ignore_index=True) if not shopping_df.empty else keywords_df
    
    # Enhanced data processing
    processed_df = combined_df.copy()
    
    # Add intelligence fields using nested data extraction
    # First, let's see what fields we actually have
    available_cols = list(processed_df.columns)
    st.info(f"🔍 Processing fields: {available_cols}")
    
    # Map the fields - handle nested data structures
    def extract_search_volume(row):
        """Extract search volume from nested search_data"""
        try:
            search_data = row.get('search_data', {})
            if isinstance(search_data, dict):
                # Try direct search_volume first
                direct_volume = search_data.get('search_volume', 0)
                if direct_volume > 0:
                    return direct_volume
                
                # Try monthly_searches array
                monthly_searches = search_data.get('monthly_searches', [])
                if isinstance(monthly_searches, list) and len(monthly_searches) > 0:
                    # Get the most recent month's volume
                    latest_month = monthly_searches[-1]
                    if isinstance(latest_month, dict):
                        return latest_month.get('search_volume', 0)
            return 0
        except Exception as e:
            return 0
    
    def extract_position(row):
        """Extract position from nested ranking_data"""
        try:
            ranking_data = row.get('ranking_data', {})
            desktop_rank = ranking_data.get('desktop', {}).get('rank', 0)
            mobile_rank = ranking_data.get('mobile', {}).get('rank', 0)
            # Use desktop rank as primary, fallback to mobile
            return desktop_rank if desktop_rank > 0 else mobile_rank
        except:
            return 0
    
    def extract_difficulty(row):
        """Extract difficulty from nested traffic_data or opportunity"""
        try:
            # Try traffic_data.opportunity first
            traffic_data = row.get('traffic_data', {})
            if isinstance(traffic_data, dict):
                opportunity = traffic_data.get('opportunity', {})
                if isinstance(opportunity, dict):
                    difficulty_str = opportunity.get('difficulty', '')
                    if difficulty_str:
                        # Convert difficulty string to numeric
                        if 'top_30' in difficulty_str.lower():
                            return 30
                        elif 'top_10' in difficulty_str.lower():
                            return 10
                        elif 'top_5' in difficulty_str.lower():
                            return 5
            
            # Try direct opportunity field
            opportunity = row.get('opportunity', {})
            if isinstance(opportunity, dict):
                difficulty_str = opportunity.get('difficulty', '')
                if difficulty_str:
                    if 'top_30' in difficulty_str.lower():
                        return 30
                    elif 'top_10' in difficulty_str.lower():
                        return 10
                    elif 'top_5' in difficulty_str.lower():
                        return 5
            
            return 0
        except:
            return 0
    
    # Apply the extraction functions
    processed_df['search_volume'] = processed_df.apply(extract_search_volume, axis=1)
    processed_df['position'] = processed_df.apply(extract_position, axis=1)
    processed_df['difficulty'] = processed_df.apply(extract_difficulty, axis=1)
    processed_df['ranking_type'] = processed_df.get('type', processed_df.get('ranking_type', 'traditional'))
    
    # Debug: Show extracted values
    st.info(f"🔍 Extracted values - Volume: {processed_df['search_volume'].sum()}, Position: {processed_df['position'].mean():.1f}, Difficulty: {processed_df['difficulty'].mean():.1f}")
    
    # Debug: Show sample nested data structure
    if len(processed_df) > 0:
        sample_row = processed_df.iloc[0]
        st.info(f"🔍 Sample search_data: {sample_row.get('search_data', 'NOT_FOUND')}")
        st.info(f"🔍 Sample ranking_data: {sample_row.get('ranking_data', 'NOT_FOUND')}")
        st.info(f"🔍 Sample traffic_data: {sample_row.get('traffic_data', 'NOT_FOUND')}")
    
    # Calculate intelligence metrics
    processed_df['traffic_potential'] = processed_df['search_volume'] * (1 / (processed_df['position'] + 1))
    processed_df['opportunity_score'] = processed_df['search_volume'] * (11 - processed_df['position']) / 10
    processed_df['priority_level'] = processed_df.apply(calculate_priority_level, axis=1)
    
    # Note: Competition and share of voice analysis removed as those endpoints don't exist in SEOMonitor API v3
    
    # Store data for learning (session state)
    store_learning_data(processed_df, campaign_id)
    
    return processed_df

def calculate_priority_level(row):
    """Calculate priority level based on multiple factors"""
    volume = row.get('search_volume', 0)
    position = row.get('position', 0)
    difficulty = row.get('difficulty', 0)
    
    # High priority: High volume, good position, low difficulty
    if volume > 1000 and position < 5 and difficulty < 50:
        return "HIGH"
    elif volume > 500 and position < 10 and difficulty < 70:
        return "MEDIUM"
    else:
        return "LOW"

def add_competition_analysis(df, competitors_df):
    """Add competition analysis to keyword data"""
    # This would analyze competitor rankings and market share
    df['competitor_count'] = competitors_df.groupby('keyword').size().reindex(df['keyword']).fillna(0)
    df['market_dominance'] = df.apply(lambda x: "HIGH" if x['competitor_count'] > 5 else "MEDIUM" if x['competitor_count'] > 2 else "LOW", axis=1)
    return df

def add_share_of_voice_analysis(df, sov_df):
    """Add share of voice analysis"""
    # This would analyze how much of the search market we capture
    df['sov_percentage'] = sov_df.set_index('keyword')['sov'].reindex(df['keyword']).fillna(0)
    df['sov_status'] = df['sov_percentage'].apply(lambda x: "STRONG" if x > 20 else "MODERATE" if x > 10 else "WEAK")
    return df

def store_learning_data(df, campaign_id):
    """Store data for AI learning and historical analysis"""
    if 'learning_data' not in st.session_state:
        st.session_state['learning_data'] = {}
    
    # Store current data
    st.session_state['learning_data'][campaign_id] = {
        'timestamp': datetime.now(),
        'data': df.to_dict('records'),
        'summary_stats': {
            'total_keywords': len(df),
            'avg_volume': df['search_volume'].mean(),
            'high_priority': len(df[df['priority_level'] == 'HIGH']),
            'shopping_keywords': len(df[df['ranking_type'] == 'shopping']),
            'avg_position': df['position'].mean()
        }
    }
    
    st.success("🧠 Data stored for AI learning and analysis")

def get_ai_recommendations(keyword_data, product_data):
    """Generate AI-powered recommendations with detailed reasoning"""
    recommendations = []
    
    for _, product in product_data.iterrows():
        product_title = product.get('title', '')
        product_description = product.get('description', '')
        
        # Find relevant keywords for this product
        relevant_keywords = find_relevant_keywords(keyword_data, product_title, product_description)
        
        # Generate optimization recommendations
        title_rec = optimize_title_with_reasoning(product_title, relevant_keywords)
        desc_rec = optimize_description_with_reasoning(product_description, relevant_keywords)
        
        recommendations.append({
            'product_id': product.get('id', ''),
            'current_title': product_title,
            'optimized_title': title_rec['optimized'],
            'title_reasoning': title_rec['reasoning'],
            'current_description': product_description,
            'optimized_description': desc_rec['optimized'],
            'description_reasoning': desc_rec['reasoning'],
            'priority_score': title_rec['priority_score'],
            'expected_impact': title_rec['expected_impact']
        })
    
    return recommendations

def find_relevant_keywords(keyword_data, title, description):
    """Find keywords most relevant to this product"""
    # Simple keyword matching - could be enhanced with NLP
    # Handle NaN values in title/description
    title = str(title) if pd.notna(title) else ""
    description = str(description) if pd.notna(description) else ""
    product_text = f"{title} {description}".lower()
    
    relevant = []
    for _, keyword_row in keyword_data.iterrows():
        # Handle NaN values in keyword
        keyword = str(keyword_row['keyword']) if pd.notna(keyword_row['keyword']) else ""
        if keyword and any(word in product_text for word in keyword.lower().split()):
            relevant.append(keyword_row)
    
    return pd.DataFrame(relevant)

def optimize_title_with_reasoning(current_title, relevant_keywords):
    """Optimize title with detailed AI reasoning"""
    if relevant_keywords.empty:
        return {
            'optimized': current_title,
            'reasoning': "No relevant keywords found in SEOMonitor data",
            'priority_score': 0,
            'expected_impact': "LOW"
        }
    
    # Find best keyword to integrate
    best_keyword = relevant_keywords.loc[relevant_keywords['traffic_potential'].idxmax()]
    
    # Generate optimized title
    optimized_title = integrate_keyword_intelligently(current_title, best_keyword['keyword'])
    
    # Generate detailed reasoning
    reasoning = f"""
    🎯 OPTIMIZATION REASONING:
    
    📊 KEYWORD ANALYSIS:
    • Selected: "{best_keyword['keyword']}"
    • Search Volume: {best_keyword['search_volume']:,} monthly searches
    • Current Position: #{best_keyword['position']} 
    • Traffic Potential: {best_keyword['traffic_potential']:.1f}
    • Priority Level: {best_keyword['priority_level']}
    
    🧠 AI DECISION LOGIC:
    • High search volume ({best_keyword['search_volume']:,}) indicates strong demand
    • Position #{best_keyword['position']} shows ranking opportunity
    • Integration maintains brand identity while improving SEO
    • Expected to improve Google Shopping visibility
    
    📈 EXPECTED IMPACT:
    • Better product grid placement
    • Increased click-through rates
    • Higher conversion potential
    """
    
    return {
        'optimized': optimized_title,
        'reasoning': reasoning,
        'priority_score': best_keyword['traffic_potential'],
        'expected_impact': "HIGH" if best_keyword['traffic_potential'] > 100 else "MEDIUM"
    }

def optimize_description_with_reasoning(current_description, relevant_keywords):
    """Optimize description with detailed AI reasoning"""
    if relevant_keywords.empty:
        return {
            'optimized': current_description,
            'reasoning': "No relevant keywords found for description optimization"
        }
    
    # Find secondary keywords for description
    secondary_keywords = relevant_keywords.nlargest(3, 'search_volume')['keyword'].tolist()
    
    # Generate optimized description
    optimized_description = enhance_description_with_keywords(current_description, secondary_keywords)
    
    reasoning = f"""
    🎯 DESCRIPTION OPTIMIZATION:
    
    📊 KEYWORDS INTEGRATED:
    • Primary: "{secondary_keywords[0]}" ({relevant_keywords.iloc[0]['search_volume']:,} volume)
    • Secondary: "{secondary_keywords[1]}" ({relevant_keywords.iloc[1]['search_volume']:,} volume)
    • Tertiary: "{secondary_keywords[2]}" ({relevant_keywords.iloc[2]['search_volume']:,} volume)
    
    🧠 OPTIMIZATION STRATEGY:
    • Natural keyword integration for better relevance
    • Maintains product appeal while improving SEO
    • Targets multiple search intents
    • Enhances Google Shopping algorithm understanding
    """
    
    return {
        'optimized': optimized_description,
        'reasoning': reasoning
    }

def integrate_keyword_intelligently(title, keyword):
    """Intelligently integrate keyword into title"""
    # Handle NaN values
    title = str(title) if pd.notna(title) else ""
    keyword = str(keyword) if pd.notna(keyword) else ""
    
    if not title or not keyword:
        return title
    
    # Simple integration - could be enhanced with NLP
    if keyword.lower() not in title.lower():
        # Add keyword naturally
        words = keyword.split()
        if len(words) == 1:
            return f"{title} - {keyword.title()}"
        else:
            return f"{title} | {keyword.title()}"
    return title

def enhance_description_with_keywords(description, keywords):
    """Enhance description with relevant keywords"""
    # Handle NaN values
    description = str(description) if pd.notna(description) else ""
    enhanced = description
    
    for keyword in keywords:
        keyword = str(keyword) if pd.notna(keyword) else ""
        if keyword and keyword.lower() not in description.lower():
            enhanced += f" {keyword.title()}"
    return enhanced

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
            if st.button("🔍 Fetch ALL Keywords (5K+)"):
                with st.spinner("🔄 Fetching comprehensive keyword data..."):
                    df_seo = fetch_comprehensive_seomonitor_data()
                    
                    if not df_seo.empty:
                        st.session_state['seomonitor_data'] = df_seo
                        st.success(f"✅ Fetched {len(df_seo)} keywords with intelligence analysis!")
                        
                        # Show comprehensive stats
                        st.subheader("🧠 Intelligence Analysis")
                        col1, col2, col3, col4 = st.columns(4)
                        with col1:
                            st.metric("Total Keywords", len(df_seo))
                        with col2:
                            st.metric("High Priority", len(df_seo[df_seo['priority_level'] == 'HIGH']))
                        with col3:
                            st.metric("Shopping Keywords", len(df_seo[df_seo['ranking_type'] == 'shopping']))
                        with col4:
                            st.metric("Avg Traffic Potential", f"{df_seo['traffic_potential'].mean():.1f}")
                        
                        # Show learning data
                        if 'learning_data' in st.session_state:
                            learning = st.session_state['learning_data'][campaign_id]
                            st.subheader("📚 AI Learning Summary")
                            st.json(learning['summary_stats'])
                    else:
                        st.error("❌ Failed to fetch comprehensive data")

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
    st.header("🧠 AI-Powered Strategic Optimization")
    
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
                if 'learning_data' in st.session_state:
                    learning = st.session_state['learning_data']
                    st.info(f"🧠 AI Learning: {len(learning)} datasets")
            else:
                st.warning("⚠️ No SEOMonitor data")
        with col2:
            if df_sitebulb is not None:
                st.success(f"✅ Sitebulb: {len(df_sitebulb)} pages")
            else:
                st.warning("⚠️ No Sitebulb data")
        with col3:
            st.success(f"✅ GMC Feed: {len(df_gmc)} products")
        
        # AI-Powered Optimization Button
        if st.button("🚀 Generate AI-Powered Optimizations", type="primary"):
            if df_seo is not None:
                with st.spinner("🧠 AI is analyzing and optimizing your product feed..."):
                    # Generate AI recommendations with detailed reasoning
                    recommendations = get_ai_recommendations(df_seo, df_gmc)
                    
                    # Store recommendations in session state
                    st.session_state['ai_recommendations'] = recommendations
                    
                    st.success(f"✅ Generated {len(recommendations)} AI-powered optimizations!")
                    
                    # Show optimization summary
                    st.subheader("📊 Optimization Summary")
                    high_impact = len([r for r in recommendations if r['expected_impact'] == 'HIGH'])
                    medium_impact = len([r for r in recommendations if r['expected_impact'] == 'MEDIUM'])
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("High Impact", high_impact)
                    with col2:
                        st.metric("Medium Impact", medium_impact)
                    with col3:
                        st.metric("Total Optimizations", len(recommendations))
            else:
                st.error("❌ SEOMonitor data required for AI optimization. Please fetch keyword data first.")
        
        # Display AI Recommendations
        if 'ai_recommendations' in st.session_state:
            recommendations = st.session_state['ai_recommendations']
            
            st.subheader("🎯 AI Optimization Results")
            
            # Filter options
            col1, col2 = st.columns(2)
            with col1:
                impact_filter = st.selectbox("Filter by Impact", ["All", "HIGH", "MEDIUM", "LOW"])
            with col2:
                show_reasoning = st.checkbox("Show Detailed AI Reasoning", value=True)
            
            # Filter recommendations
            if impact_filter != "All":
                filtered_recs = [r for r in recommendations if r['expected_impact'] == impact_filter]
            else:
                filtered_recs = recommendations
            
            st.write(f"Showing {len(filtered_recs)} optimizations")
            
            # Display each recommendation
            for i, rec in enumerate(filtered_recs[:10]):  # Show first 10
                with st.expander(f"🎯 Product {i+1}: {rec['current_title'][:50]}..."):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.subheader("📝 Title Optimization")
                        st.write(f"**Current:** {rec['current_title']}")
                        st.write(f"**Optimized:** {rec['optimized_title']}")
                        st.write(f"**Priority Score:** {rec['priority_score']:.1f}")
                        st.write(f"**Expected Impact:** {rec['expected_impact']}")
                    
                    with col2:
                        st.subheader("📄 Description Optimization")
                        st.write(f"**Current:** {rec['current_description'][:100]}...")
                        st.write(f"**Optimized:** {rec['optimized_description'][:100]}...")
                    
                    if show_reasoning:
                        st.subheader("🧠 AI Reasoning")
                        st.markdown(rec['title_reasoning'])
                        st.markdown(rec['description_reasoning'])
            
            if len(filtered_recs) > 10:
                st.info(f"Showing first 10 of {len(filtered_recs)} optimizations. Use filters to narrow down results.")

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
        
        # Export optimized feed (full dataset with reasons)
        st.write("**Export Optimized Feed (with reasons):**")
        df_seo = st.session_state.get('seomonitor_data')
        
        generate_full = st.button("🧠 Generate Full Optimization for All Products")
        if generate_full:
            if df_seo is None or len(df_seo) == 0:
                st.error("❌ SEOMonitor data not found. Go to 'SEOMonitor API' and click 'Fetch ALL Keywords (5K+)'.")
            else:
                with st.spinner("Analyzing products and generating full optimization with justifications..."):
                    try:
                        # Use AI reasoning engine built earlier
                        recommendations = get_ai_recommendations(df_seo, df_gmc)
                        recs_df = pd.DataFrame(recommendations)
                        
                        # Combine with the original GMC feed (row-aligned)
                        # We avoid overwriting existing columns; we append optimized + reasoning columns
                        export_df = df_gmc.copy().reset_index(drop=True)
                        # Ensure equal length; if mismatch, align by min length
                        min_len = min(len(export_df), len(recs_df))
                        export_df = export_df.iloc[:min_len].copy()
                        recs_df = recs_df.iloc[:min_len].copy()
                        
                        # Append columns
                        export_df['optimized_title'] = recs_df['optimized_title']
                        export_df['optimized_description'] = recs_df['optimized_description']
                        export_df['priority_score'] = recs_df['priority_score']
                        export_df['expected_impact'] = recs_df['expected_impact']
                        export_df['title_reasoning'] = recs_df['title_reasoning']
                        export_df['description_reasoning'] = recs_df['description_reasoning']
                        
                        # Store for later download
                        st.session_state['optimized_export_df'] = export_df
                        st.success(f"✅ Generated optimized dataset for {len(export_df)} products.")
                    except Exception as e:
                        st.error(f"❌ Failed to generate optimizations: {str(e)}")
        
        # Download buttons when ready
        if 'optimized_export_df' in st.session_state:
            optimized_export_df = st.session_state['optimized_export_df']
            
            # CSV
            csv_optimized = optimized_export_df.to_csv(index=False)
            st.download_button(
                label="⬇️ Download Optimized CSV (with reasons)",
                data=csv_optimized,
                file_name=f"optimized_with_reasons_{st.session_state.get('gmc_file', 'gmc_feed')}.csv",
                mime="text/csv"
            )
            
            # XLSX
            from io import BytesIO
            xlsx_buffer = BytesIO()
            with pd.ExcelWriter(xlsx_buffer, engine='xlsxwriter') as writer:
                optimized_export_df.to_excel(writer, index=False, sheet_name='Optimized')
            xlsx_buffer.seek(0)
            st.download_button(
                label="⬇️ Download Optimized XLSX (with reasons)",
                data=xlsx_buffer,
                file_name=f"optimized_with_reasons_{st.session_state.get('gmc_file', 'gmc_feed')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        
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