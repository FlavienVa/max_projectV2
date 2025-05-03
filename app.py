import streamlit as st
import st_tailwind as tw

# Page configuration
st.set_page_config(
    page_title="Swiss Tourism Guide",
    page_icon="🇨🇭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Tailwind
tw.initialize_tailwind()

# Main page content
def main():
    st.title("🇨🇭 Swiss Tourism Guide")
    st.markdown("""
    Welcome to your personalized Swiss travel experience! 
    Take our quiz to discover your perfect Swiss itinerary.
    """)
    
    # Navigation buttons
    with tw.container(classes="flex justify-center gap-4 mt-8"):
        if tw.button("Start Quiz", classes="bg-blue-500 text-white px-6 py-3 rounded-lg hover:bg-blue-600"):
            st.switch_page("pages/2_Quiz.py")

if __name__ == "__main__":
    main()
