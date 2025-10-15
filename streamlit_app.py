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
    layout="wide"
)

st.title("🛒 Oak Furniture Land GMC Feed Optimizer")
st.subheader("Strategic product feed optimization using search volume + PPC intelligence")

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
                return
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
                try:
                    # SEOMonitor API call for keyword rankings
                    url = f"https://api.seomonitor.com/v1/campaigns/{campaign_id}/keywords"
                    headers = {
                        'Authorization': f'Bearer {api_key}',
                        'Content-Type': 'application/json'
                    }
                    
                    response = requests.get(url, headers=headers)
                    
                    if response.status_code == 200:
                        data = response.json()
                        
                        # Convert to DataFrame
                        if 'keywords' in data:
                            keywords_data = []
                            for kw in data['keywords']:
                                keywords_data.append({
                                    'keyword': kw.get('keyword', ''),
                                    'position': kw.get('position', 0),
                                    'volume': kw.get('search_volume', 0),
                                    'difficulty': kw.get('difficulty', 0),
                                    'url': kw.get('url', '')
                                })
                            
                            df_keywords = pd.DataFrame(keywords_data)
                            st.session_state['seomonitor_data'] = df_keywords
                            
                            st.success(f"✅ Fetched {len(df_keywords)} keywords!")
                            st.dataframe(df_keywords.head(10))
                        else:
                            st.warning("No keyword data found in response")
                    else:
                        st.error(f"❌ API Error: {response.status_code}")
                        
                except Exception as e:
                    st.error(f"❌ API Error: {str(e)}")

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
        
        st.subheader("🔍 Optimization Analysis")
        
        # Title optimization
        if 'title' in df_gmc.columns:
            st.subheader("📝 Title Optimization")
            
            # Sample title analysis
            sample_titles = df_gmc['title'].head(5)
            for i, title in enumerate(sample_titles):
                with st.expander(f"Product {i+1}: {title[:50]}..."):
                    st.write(f"**Current Title:** {title}")
                    
                    # Analysis
                    st.write("**Analysis:**")
                    if len(title) < 60:
                        st.warning("⚠️ Title too short - missing keywords")
                    elif len(title) > 150:
                        st.warning("⚠️ Title too long - may be truncated")
                    else:
                        st.success("✅ Title length is good")
                    
                    # Recommendations
                    st.write("**Recommendations:**")
                    if 'furniture' not in title.lower():
                        st.write("• Add 'furniture' keyword for category relevance")
                    if 'oak' not in title.lower() and 'oak' in title.lower():
                        st.write("• Emphasize material (oak) for material-specific searches")
                    if len(title.split()) < 5:
                        st.write("• Add more descriptive keywords")
                    
                    # Suggested title
                    suggested_title = f"{title} - Premium Furniture" if 'furniture' not in title.lower() else title
                    st.write(f"**Suggested Title:** {suggested_title}")
        
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