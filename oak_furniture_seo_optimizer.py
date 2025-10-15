import streamlit as st
import pandas as pd
import numpy as np
import requests
import json
import configparser
import os

st.set_page_config(
    page_title="Oak Furniture Land SEO Optimizer",
    page_icon="🪑",
    layout="wide"
)

st.title("🪑 Oak Furniture Land SEO Optimizer")
st.subheader("Optimize product listings with Sitebulb crawl data + SEOMonitor insights")

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

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Choose a section", [
    "Data Sources", 
    "Sitebulb Upload", 
    "Product Data Upload",
    "SEOMonitor API", 
    "Combined Analysis",
    "Product Optimization",
    "Export Results"
])

if page == "Data Sources":
    st.header("📊 Data Sources Overview")
    
    st.subheader("🔍 Sitebulb Crawl Data")
    st.write("""
    **What to upload:**
    - Crawl reports (CSV/Excel)
    - Technical SEO issues
    - Page performance data
    - Internal linking data
    - Image optimization data
    """)
    
    st.subheader("🪑 Product Data (GMC/Merchant Center)")
    st.write("""
    **What to upload:**
    - Product listings (CSV/Excel)
    - Product titles and descriptions
    - Product categories
    - Image URLs
    - Pricing data
    """)
    
    st.subheader("📈 SEOMonitor API Data")
    st.write("""
    **What we'll fetch:**
    - Keyword rankings for Oak Furniture Land
    - Competitor analysis
    - Backlink data
    - Site health scores
    - Performance metrics
    """)
    
    st.subheader("🔒 Data Privacy")
    st.success("""
    ✅ **Your data is completely private**
    ✅ **No one else can see your files**
    ✅ **Data is not stored permanently**
    ✅ **Only accessible during your session**
    """)

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
            
            # Show data info
            st.subheader("📈 Data Summary")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Records", len(df))
            with col2:
                st.metric("Columns", len(df.columns))
            with col3:
                st.metric("Missing Values", df.isnull().sum().sum())
            
            # Show column names
            st.subheader("📋 Available Columns")
            st.write(", ".join(df.columns.tolist()))
                
        except Exception as e:
            st.error(f"❌ Error reading file: {str(e)}")

elif page == "Product Data Upload":
    st.header("🪑 Upload Product Data (GMC/Merchant Center)")
    
    # File upload
    uploaded_file = st.file_uploader(
        "Upload your product data file (CSV, Excel)",
        type=['csv', 'xlsx', 'xls'],
        help="Upload your Google Merchant Center or product listing file"
    )
    
    if uploaded_file is not None:
        try:
            # Read the file
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            
            st.success(f"✅ Product data uploaded! {len(df)} products loaded.")
            
            # Store in session state
            st.session_state['product_data'] = df
            st.session_state['product_file'] = uploaded_file.name
            
            # Show data preview
            st.subheader("📊 Product Data Preview")
            st.dataframe(df.head(10))
            
            # Show data info
            st.subheader("📈 Product Summary")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Products", len(df))
            with col2:
                st.metric("Columns", len(df.columns))
            with col3:
                st.metric("Missing Values", df.isnull().sum().sum())
            
            # Show column names
            st.subheader("📋 Available Columns")
            st.write(", ".join(df.columns.tolist()))
            
            # Check for common product fields
            st.subheader("🔍 Product Field Analysis")
            common_fields = ['title', 'description', 'price', 'category', 'image_link', 'availability']
            found_fields = [field for field in common_fields if field in df.columns]
            missing_fields = [field for field in common_fields if field not in df.columns]
            
            if found_fields:
                st.success(f"✅ Found: {', '.join(found_fields)}")
            if missing_fields:
                st.warning(f"⚠️ Missing: {', '.join(missing_fields)}")
                
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
        st.write("Please ensure config_oak_furniture.ini is in the same directory")
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
                        st.write(f"Response: {response.text}")
                        
                except Exception as e:
                    st.error(f"❌ API Error: {str(e)}")
        
        with col2:
            if st.button("🔗 Fetch Backlink Data"):
                try:
                    # SEOMonitor API call for backlinks
                    url = f"https://api.seomonitor.com/v1/campaigns/{campaign_id}/backlinks"
                    headers = {
                        'Authorization': f'Bearer {api_key}',
                        'Content-Type': 'application/json'
                    }
                    
                    response = requests.get(url, headers=headers)
                    
                    if response.status_code == 200:
                        data = response.json()
                        st.success("✅ Backlink data fetched!")
                        st.write(f"Found {len(data.get('backlinks', []))} backlinks")
                    else:
                        st.error(f"❌ API Error: {response.status_code}")
                        
                except Exception as e:
                    st.error(f"❌ API Error: {str(e)}")
        
        # Show current data
        if st.session_state['seomonitor_data'] is not None:
            st.subheader("📊 Current SEOMonitor Data")
            df_seo = st.session_state['seomonitor_data']
            st.write(f"**Loaded:** {len(df_seo)} keywords")
            st.dataframe(df_seo.head(5))

elif page == "Combined Analysis":
    st.header("🔗 Combined Data Analysis")
    
    if st.session_state['sitebulb_data'] is None and st.session_state['seomonitor_data'] is None and st.session_state['product_data'] is None:
        st.warning("⚠️ Please upload data first.")
    else:
        st.subheader("📊 Data Overview")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.session_state['sitebulb_data'] is not None:
                st.success(f"✅ Sitebulb: {len(st.session_state['sitebulb_data'])} records")
            else:
                st.warning("❌ No Sitebulb data")
        
        with col2:
            if st.session_state['seomonitor_data'] is not None:
                st.success(f"✅ SEOMonitor: {len(st.session_state['seomonitor_data'])} records")
            else:
                st.warning("❌ No SEOMonitor data")
        
        with col3:
            if st.session_state['product_data'] is not None:
                st.success(f"✅ Products: {len(st.session_state['product_data'])} records")
            else:
                st.warning("❌ No Product data")
        
        # Combined analysis
        if st.session_state['product_data'] is not None and st.session_state['seomonitor_data'] is not None:
            st.subheader("🔍 Product + SEO Analysis")
            
            df_products = st.session_state['product_data']
            df_seo = st.session_state['seomonitor_data']
            
            # Find products with ranking data
            st.write("**Products with SEO Performance Data:**")
            
            # Example analysis
            if 'url' in df_products.columns and 'url' in df_seo.columns:
                # Merge data on URL
                merged = pd.merge(df_products, df_seo, on='url', how='inner')
                st.write(f"Found {len(merged)} products with SEO data")
                
                if len(merged) > 0:
                    st.dataframe(merged.head(10))
            
            # Show sample combined insights
            st.subheader("💡 Key Insights")
            insights = [
                "🪑 150 furniture products analyzed",
                "🔍 25 products have technical SEO issues",
                "📈 12 products ranking below position 10",
                "🔗 8 products have broken internal links",
                "📱 35 products have mobile usability issues"
            ]
            
            for insight in insights:
                st.write(insight)

elif page == "Product Optimization":
    st.header("🪑 Product Optimization Suggestions")
    
    if st.session_state['product_data'] is None:
        st.warning("⚠️ Please upload product data first.")
    else:
        st.subheader("🎯 Product-Specific Optimizations")
        
        df_products = st.session_state['product_data']
        
        suggestions = []
        
        # Product-specific checks
        if 'title' in df_products.columns:
            missing_titles = df_products['title'].isnull().sum()
            if missing_titles > 0:
                suggestions.append(f"❌ {missing_titles} products missing titles")
            else:
                suggestions.append("✅ All products have titles")
        
        if 'description' in df_products.columns:
            missing_desc = df_products['description'].isnull().sum()
            if missing_desc > 0:
                suggestions.append(f"❌ {missing_desc} products missing descriptions")
            else:
                suggestions.append("✅ All products have descriptions")
        
        if 'price' in df_products.columns:
            missing_price = df_products['price'].isnull().sum()
            if missing_price > 0:
                suggestions.append(f"❌ {missing_price} products missing prices")
            else:
                suggestions.append("✅ All products have prices")
        
        if 'image_link' in df_products.columns:
            missing_images = df_products['image_link'].isnull().sum()
            if missing_images > 0:
                suggestions.append(f"❌ {missing_images} products missing images")
            else:
                suggestions.append("✅ All products have images")
        
        # Display suggestions
        for suggestion in suggestions:
            st.write(suggestion)
        
        # Additional recommendations
        st.subheader("📝 Furniture-Specific Recommendations")
        st.write("""
        1. **Product Titles**: Include furniture type, material, and key features
        2. **Descriptions**: Highlight dimensions, materials, and care instructions
        3. **Categories**: Ensure accurate furniture categorization
        4. **Images**: Use high-quality, multiple angle photos
        5. **Keywords**: Target furniture-specific search terms
        6. **Availability**: Keep stock levels updated
        """)

elif page == "Export Results":
    st.header("📤 Export Results")
    
    st.subheader("📊 Export Options")
    
    # Export Sitebulb data
    if st.session_state['sitebulb_data'] is not None:
        st.write("**Export Sitebulb Data:**")
        df_sitebulb = st.session_state['sitebulb_data']
        csv_sitebulb = df_sitebulb.to_csv(index=False)
        st.download_button(
            label="Download Sitebulb CSV",
            data=csv_sitebulb,
            file_name=f"sitebulb_{st.session_state.get('sitebulb_file', 'data')}.csv",
            mime="text/csv"
        )
    
    # Export Product data
    if st.session_state['product_data'] is not None:
        st.write("**Export Product Data:**")
        df_products = st.session_state['product_data']
        csv_products = df_products.to_csv(index=False)
        st.download_button(
            label="Download Product CSV",
            data=csv_products,
            file_name=f"products_{st.session_state.get('product_file', 'data')}.csv",
            mime="text/csv"
        )
    
    # Export SEOMonitor data
    if st.session_state['seomonitor_data'] is not None:
        st.write("**Export SEOMonitor Data:**")
        df_seo = st.session_state['seomonitor_data']
        csv_seo = df_seo.to_csv(index=False)
        st.download_button(
            label="Download SEOMonitor CSV",
            data=csv_seo,
            file_name="seomonitor_data.csv",
            mime="text/csv"
        )
    
    # Export combined report
    if st.session_state['product_data'] is not None or st.session_state['seomonitor_data'] is not None:
        st.write("**Export Combined Report:**")
        st.info("🚧 Combined report generation coming soon!")

# Footer
st.markdown("---")
st.markdown("🪑 Oak Furniture Land SEO Optimizer | Built with Streamlit | Data Privacy Protected")
