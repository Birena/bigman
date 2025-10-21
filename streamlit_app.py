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
            
            # Create optimized DataFrame
            optimized_data = []
            for rec in recommendations:
                # Find original product data
                original_product = df_gmc[df_gmc['id'] == rec['product_id']].iloc[0] if 'id' in df_gmc.columns else df_gmc.iloc[int(rec['product_id'].split('_')[1]) if '_' in rec['product_id'] else 0]
                
                # Create optimized product row
                optimized_row = original_product.to_dict()
                optimized_row['title'] = rec['optimized_title']
                optimized_row['description'] = rec['optimized_description']
                optimized_row['optimization_priority'] = rec['priority_score']
                optimized_row['expected_impact'] = rec['expected_impact']
                optimized_row['title_reasoning'] = rec['title_reasoning']
                optimized_row['description_reasoning'] = rec['description_reasoning']
                
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
            
            # Export optimized Excel
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
            
            # Show summary
            st.success(f"✅ Ready to export {len(optimized_data)} optimized products!")
            
            # Show sample of optimizations
            st.subheader("📋 Sample Optimizations")
            sample_df = df_optimized[['title', 'optimized_title', 'expected_impact', 'title_reasoning']].head(5)
            st.dataframe(sample_df)
            
        else:
            st.warning("⚠️ No optimizations found. Please run 'Strategic Optimization' first.")ata'] = None
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
        
        if st.button("🚀 Generate AI-Powered Optimizations", type="primary"):
            if df_seo is not None:
                with st.spinner("🧠 AI is analyzing and optimizing all products..."):
                    # Initialize progress bar
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    # Get optimization recommendations
                    recommendations = []
                    total_products = len(df_gmc)
                    
                    for i, (_, product) in enumerate(df_gmc.iterrows()):
                        # Update progress
                        progress = (i + 1) / total_products
                        progress_bar.progress(progress)
                        status_text.text(f"🎯 Optimizing product {i+1}/{total_products}: {product.get('title', 'Unknown')[:50]}...")
                        
                        # Find relevant keywords for this product
                        product_title = str(product.get('title', ''))
                        product_desc = str(product.get('description', ''))
                        product_text = f"{product_title} {product_desc}".lower()
                        
                        # Find matching keywords
                        relevant_keywords = []
                        for _, keyword_row in df_seo.iterrows():
                            keyword = str(keyword_row.get('keyword', ''))
                            if keyword and any(word in product_text for word in keyword.lower().split()):
                                relevant_keywords.append(keyword_row)
                        
                        if relevant_keywords:
                            # Get best keyword
                            best_keyword = max(relevant_keywords, key=lambda x: x.get('search_volume', 0))
                            
                            # Optimize title
                            optimized_title = product_title
                            if best_keyword['keyword'].lower() not in product_title.lower():
                                optimized_title = f"{product_title} | {best_keyword['keyword'].title()}"
                            
                            # Optimize description
                            optimized_desc = product_desc
                            if len(relevant_keywords) > 1:
                                secondary_keyword = relevant_keywords[1]['keyword']
                                if secondary_keyword.lower() not in product_desc.lower():
                                    optimized_desc = f"{product_desc} {secondary_keyword.title()}"
                            
                            # Calculate priority score
                            search_volume = best_keyword.get('search_volume', 0)
                            priority_score = min(100, search_volume / 10)  # Scale to 0-100
                            
                            recommendations.append({
                                'product_id': product.get('id', f'product_{i}'),
                                'current_title': product_title,
                                'optimized_title': optimized_title,
                                'current_description': product_desc,
                                'optimized_description': optimized_desc,
                                'priority_score': priority_score,
                                'expected_impact': 'HIGH' if priority_score > 50 else 'MEDIUM' if priority_score > 20 else 'LOW',
                                'title_reasoning': f"Added high-volume keyword '{best_keyword['keyword']}' ({search_volume:,} monthly searches) to improve Google Shopping visibility",
                                'description_reasoning': f"Enhanced with secondary keyword '{secondary_keyword}' for better search relevance" if len(relevant_keywords) > 1 else "Description optimized for search intent"
                            })
                        else:
                            # No relevant keywords found
                            recommendations.append({
                                'product_id': product.get('id', f'product_{i}'),
                                'current_title': product_title,
                                'optimized_title': product_title,
                                'current_description': product_desc,
                                'optimized_description': product_desc,
                                'priority_score': 0,
                                'expected_impact': 'LOW',
                                'title_reasoning': "No relevant keywords found in SEOMonitor data",
                                'description_reasoning': "No optimization opportunities identified"
                            })
                    
                    # Store recommendations
                    st.session_state['optimization_recommendations'] = recommendations
                    
                    # Clear progress
                    progress_bar.empty()
                    status_text.empty()
                    
                    # Show results
                    st.success(f"✅ Generated optimizations for {len(recommendations)} products!")
                    
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
                    
                    st.info("💡 Optimizations complete! Go to 'Export Optimized Feed' to download your optimized GMC feed.")
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
            
            # Create optimized DataFrame
            optimized_data = []
            for rec in recommendations:
                # Find original product data
                original_product = df_gmc[df_gmc['id'] == rec['product_id']].iloc[0] if 'id' in df_gmc.columns else df_gmc.iloc[int(rec['product_id'].split('_')[1]) if '_' in rec['product_id'] else 0]
                
                # Create optimized product row
                optimized_row = original_product.to_dict()
                optimized_row['title'] = rec['optimized_title']
                optimized_row['description'] = rec['optimized_description']
                optimized_row['optimization_priority'] = rec['priority_score']
                optimized_row['expected_impact'] = rec['expected_impact']
                optimized_row['title_reasoning'] = rec['title_reasoning']
                optimized_row['description_reasoning'] = rec['description_reasoning']
                
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
            
            # Export optimized Excel
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
            
            # Show summary
            st.success(f"✅ Ready to export {len(optimized_data)} optimized products!")
            
            # Show sample of optimizations
            st.subheader("📋 Sample Optimizations")
            sample_df = df_optimized[['title', 'optimized_title', 'expected_impact', 'title_reasoning']].head(5)
            st.dataframe(sample_df)
            
        else:
            st.warning("⚠️ No optimizations found. Please run 'Strategic Optimization' first.")

# Footer
st.markdown("---")
st.markdown("🛒 Oak Furniture Land GMC Feed Optimizer | Strategic SEO + PPC Integration")