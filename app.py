import os
import shutil

import streamlit as st

from src.manager import QuizManager, rerun
from src.generator import QuestionGenerator

@st.cache_resource
def get_quiz_manager()->QuizManager:
    return QuizManager()

def main():
    st.set_page_config(page_title="Quiz Buddy AI" , page_icon="🎧🎧")

    if 'quiz_manager'not in st.session_state:
        st.session_state.quiz_manager = get_quiz_manager()

    if 'quiz_generated'not in st.session_state:
        st.session_state.quiz_generated = False

    if 'quiz_submitted'not in st.session_state:
        st.session_state.quiz_submitted = False

    if 'rerun_trigger'not in st.session_state:
        st.session_state.rerun_trigger = False
        try:
            shutil.rmtree("results")
        except:
            pass
        

    st.title("Quiz Buddy AI")

    st.sidebar.header("Quiz Settings")
    
    question_type=st.sidebar.selectbox(
        "Select Question Type" ,
        ["Multiple Choice" , "Fill in the Blank"],
        index=0
    )
    
    topic = st.sidebar.text_input("Enter Topic" , placeholder="History, Geography")
    
    difficulty = st.sidebar.selectbox(
        "Dificulty Level",
        ["Easy" , "Medium" , "Hard"],
        index=1
    )
    
    num_questions=st.sidebar.number_input(
        "Number of Questions",
        min_value=1,  max_value=10 , value=5
    )
    
    if st.sidebar.button('Generate Quiz'):
        st.session_state.quiz_submitted = False
        generator = QuestionGenerator()
        success = st.session_state.quiz_manager.generate_questions(
            generator,
            topic,
            question_type,
            difficulty,
            num_questions
        )
        st.session_state.quiz_generated = success
        rerun()
        
    if st.session_state.quiz_generated and st.session_state.quiz_manager.questions:
        st.header('Quiz')
        st.session_state.quiz_manager.attempt_quiz()
        
        if st.button('Submit Quiz'):
            st.session_state.quiz_manager.evaluate_quiz()
            st.session_state.quiz_submitted = True
            rerun()
    
    if st.session_state.quiz_submitted:
        st.header("Quiz Results")
        results_df = st.session_state.quiz_manager.generate_result_dataframe()
        
        if not results_df.empty:
            correct_count = results_df["is_correct"].sum()
            total_questions = len(results_df)
            score_percentage = (correct_count/total_questions)*100
            st.write(f"Score : {score_percentage}")
            
            for _, result in results_df.iterrows():
                question_num = result['question_number']
                if result['is_correct']:
                    st.success(f"✅ Question {question_num} : {result['question']}")
                    st.write(f"Your answer : {result['user_answer']}")
                else:
                    st.error(f"❌ Question {question_num} : {result['question']}")
                    st.write(f"Your answer : {result['user_answer']}")
                    st.write(f"Correct answer : {result['correct_answer']}")
                    
                st.markdown("-------")
            
            if st.button("Save Results"):
                saved_file = st.session_state.quiz_manager.save_to_csv()
                if saved_file:
                    with open(saved_file,'rb') as f:
                        downloaded = st.download_button(
                                        label="Download Results",
                                        data= f.read(),
                                        file_name=os.path.basename(saved_file),
                                        mime='text/csv'
                                    )
                        if not downloaded:
                            shutil.rmtree('results')
                else:
                    st.warning("No results avialble")


    
if __name__ == "__main__":
    main()
