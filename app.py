import streamlit as st
import utils
import os

# Page Config
st.set_page_config(
    page_title="Legal Eagle AI",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Premium Look
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }
    
    .stApp {
        background-color: #0e1117;
        color: #fafafa;
    }
    
    /* Card Styles */
    .risk-card {
        background-color: #1e2130;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border-left: 5px solid #ccc;
    }
    
    .risk-high {
        border-left-color: #ff4b4b;
    }
    
    .risk-medium {
        border-left-color: #ffa500;
    }
    
    .risk-low {
        border-left-color: #00cc96;
    }
    
    .card-title {
        font-weight: 600;
        font-size: 1.1em;
        margin-bottom: 8px;
    }
    
    .badge-verified {
        background-color: #00cc96;
        color: white;
        padding: 2px 8px;
        border-radius: 12px;
        font-size: 0.8em;
        margin-left: 8px;
    }
    
    .badge-warning {
        background-color: #ffa500;
        color: black;
        padding: 2px 8px;
        border-radius: 12px;
        font-size: 0.8em;
        margin-left: 8px;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.title("⚖️ Legal Eagle AI")
    st.markdown("### Contract Intelligence")
    
    uploaded_file = st.file_uploader("Upload Contract (PDF)", type="pdf")
    
    contract_type = st.selectbox(
        "Contract Type",
        ["General", "NDA", "Employment", "Lease/Rental", "Service Agreement"]
    )
    
    analyze_btn = st.button("Analyze Contract", type="primary", use_container_width=True)
    
    st.markdown("---")
    st.info("Powered by Gemini 1.5 Flash")

# State Management
if "analysis_results" not in st.session_state:
    st.session_state.analysis_results = None
if "extracted_text" not in st.session_state:
    st.session_state.extracted_text = None

# Main Logic
if uploaded_file:
    # Extract Text if new file
    if analyze_btn:
        with st.spinner("Extracting and analyzing text..."):
            # 1. Ingestion & Pre-processing
            raw_text = utils.extract_text(uploaded_file)
            cleaned_text = utils.clean_text(raw_text)
            st.session_state.extracted_text = cleaned_text
            
            # 2. Segmentation
            chunks = utils.chunk_text(cleaned_text)
            
            # 3. Intelligence & Analysis
            all_risks = []
            progress_bar = st.progress(0)
            
            for i, chunk in enumerate(chunks):
                result = utils.analyze_with_gemini(chunk, contract_type)
                if result and "risks" in result:
                    # 4. Verification
                    verified_result = utils.verify_quotes(result, cleaned_text)
                    all_risks.extend(verified_result["risks"])
                
                # Check for errors in the result
                if result and "error" in result:
                    st.error(f"Error analyzing chunk {i+1}: {result['error']}")
                progress_bar.progress((i + 1) / len(chunks))
            
            st.session_state.analysis_results = all_risks
            st.success("Analysis Complete!")

# Dashboard
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📄 Source Document")
    if st.session_state.extracted_text:
        st.text_area("Extracted Text", st.session_state.extracted_text, height=600)
    else:
        st.markdown("*Upload a document to see the text here.*")

with col2:
    st.subheader("🛡️ Risk Analysis")
    
    if st.session_state.analysis_results:
        risks = st.session_state.analysis_results
        
        # summary stats
        high_risks = len([r for r in risks if r['category'] == 'High'])
        med_risks = len([r for r in risks if r['category'] == 'Medium'])
        
        st.markdown(f"**Found {high_risks} High Risks, {med_risks} Medium Risks**")
        
        for risk in risks:
            category = risk.get('category', 'Low')
            risk_class = f"risk-{category.lower()}"
            verified = risk.get('verified', False)
            
            badge_html = ""
            if verified:
                badge_html = '<span class="badge-verified">✓ Verified</span>'
            else:
                badge_html = '<span class="badge-warning">⚠ Unverified Quote</span>'
                
            card_html = f"""
            <div class="risk-card {risk_class}">
                <div class="card-title">
                    {risk.get('risk_type', 'Unknown Risk')}
                    {badge_html}
                </div>
                <p><strong>Impact:</strong> {risk.get('explanation', 'No details provided.')}</p>
                <hr style="border-color: #333;">
                <p style="font-size: 0.9em; color: #aaa;"><em>Quote: "{risk.get('quote', 'N/A')}"</em></p>
            </div>
            """
            st.markdown(card_html, unsafe_allow_html=True)
            
    else:
        st.markdown("*Analysis results will appear here.*")
