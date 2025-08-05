import streamlit as st

# Simple test version
st.set_page_config(
    page_title="Text to Teamwork",
    page_icon="📋"
)

st.title("📋 Text to Teamwork Converter")
st.success("✅ App is running successfully!")

st.write("This is a test to verify the deployment works.")

# Test basic imports
try:
    import pandas as pd
    st.success("✅ Pandas imported")
    
    from text_to_teamwork import TextToTeamworkConverter
    st.success("✅ Main module imported")
    
    st.info("🎉 All systems working! The full app should work now.")
    
except Exception as e:
    st.error(f"❌ Error: {e}")
    st.code(str(e)) 