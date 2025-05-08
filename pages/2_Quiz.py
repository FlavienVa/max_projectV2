import streamlit as st
import st_tailwind as tw
from components.quiz_questions import QUIZ_QUESTIONS

def main():
    st.title("Travel Preferences Quiz")
    st.markdown("Answer these questions to help us find your perfect Swiss itinerary!")
    
    # Initialize session state for quiz answers if not exists
    if 'quiz_answers' not in st.session_state:
        st.session_state.quiz_answers = {}
    
    # Display questions
    for i, question in enumerate(QUIZ_QUESTIONS):
        st.subheader(f"Question {i+1}: {question['question']}")
        
        # Use the question text as the key
        answer = st.radio(
            "Select your answer:",
            question['options'],
            key=f"q_{question['question']}",
            index=None
        )
        
        # Store answer in session state
        if answer:
            st.session_state.quiz_answers[question['question']] = answer
    
    # Navigation buttons
    with tw.container(classes="flex justify-between mt-8"):
        if tw.button("Back to Home", classes="bg-gray-200 text-gray-800 px-4 py-2 rounded"):
            st.switch_page("app.py")
        
        if len(st.session_state.quiz_answers) == len(QUIZ_QUESTIONS):
            if tw.button("See Results", classes="bg-blue-500 text-white px-4 py-2 rounded"):
                st.switch_page("pages/3_Results.py")
        else:
            st.warning("Please answer all questions to proceed.")

if __name__ == "__main__":
    main() 