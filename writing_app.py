
import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))




def participant_id_page():
    """Page to collect participant ID before proceeding to the story task"""
    st.title("🔍 Story Writing Study")
    st.markdown("---")
    
    st.markdown("""
    ### Welcome to the Story Writing Research Study
    
    Before we begin, please enter your participant ID below. This ID should have been provided to you 
    by the research team.
    """)
    
    # Create input field for participant ID
    participant_id = st.text_input(
        "Participant ID:",
        placeholder="Enter your participant ID (e.g., P001, SUBJ123, etc.)",
        help="Enter the ID exactly as provided by the research team"
    )
    
    # Validation and proceed button
    if participant_id:
        # Basic validation
        if len(participant_id.strip()) < 3:
            st.warning("Please enter a valid participant ID (at least 3 characters)")
        else:
            st.success(f"Participant ID: {participant_id}")
            
            # Button to proceed to the main task
            if st.button("Proceed to Story Writing Task", type="primary"):
                # Store participant ID in session state
                st.session_state.participant_id = participant_id.strip()
                st.session_state.page = "story_task"
                st.rerun()
    else:
        st.info("Please enter your participant ID to continue.")
    
    # Optional: Add contact information
    st.markdown("---")
    st.markdown("""
    **Questions?** Contact the research team if you need assistance with your participant ID.
    """)

def story_writing_page():
    """Your existing story writing task page"""
    # Display participant ID in sidebar for reference
    if 'participant_id' in st.session_state:
        st.sidebar.info(f"Participant: {st.session_state.participant_id}")
    
    st.title("🔎 Story Writing Task")
    st.write("""
    Story Writing Task
    In the text box below, please write a short story (about four sentences long) that includes the following three words: **"stamp," "send," and "letter."**
    Be as creative as you can—your story can be any style you imagine.
     
    Important: You are required to use the bot to help write your story. We have already set it up for you, and you must use it at least once during your writing process. You can use the bot to help brainstorm, get information, improve phrasing, write or co-write the text of your story, or in any other way that is useful.

    You can prompt the bot as many times and as often as you'd like. Feel free to copy and paste any parts from the interaction and edit them as much as you like if you want to change what the bot wrote.
     
    **Important reminders**:
    Please use the same session and window throughout this task.
    Do not use any tool for writing other than the bot provided.
    At the end of the session, please do not delete your session history.
    Once you feel ready, you may click the "Next" button to submit your story.


    Use the chatbot on the left to help organize your thoughts. On the right, you have space to work on a draft and then finalize your reflection.
    """)

    # Initialize session state for chatbot messages and user input
    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            {"role": "system", "content": "How can I help you with writing the short story?"}
        ]
    if "user_input" not in st.session_state:
        st.session_state["user_input"] = ""

    # Function to handle sending chat messages
    def send_message():
        user_input = st.session_state.user_input
        if user_input.strip():
            st.session_state["messages"].append({"role": "user", "content": user_input})
            try:
                response = client.chat.completions.create(
                    model="gpt-4",
                    messages=st.session_state["messages"]
                )
                bot_message = response.choices[0].message.content
                st.session_state["messages"].append({"role": "assistant", "content": bot_message})
            except Exception as e:
                error_msg = f"Error: {e}"
                st.session_state["messages"].append({"role": "assistant", "content": error_msg})
        st.session_state.user_input = ""

    # Create a two-column layout
    col1, col2 = st.columns(2)

    # Left panel: Chatbot interface
    with col1:
        st.subheader("Chat with the Bot")
        # Display the chat history
        for msg in st.session_state["messages"]:
            if msg["role"] == "user":
                st.markdown(f"**You:** {msg['content']}")
            else:
                st.markdown(f"**Bot:** {msg['content']}")
        # Input for sending new messages
        st.text_input(
            "Your Message",
            placeholder="Ask me anything to organize your thoughts...",
            key="user_input",
            on_change=send_message
        )

    # Right panel: Draft notes and Final Submission
    with col2:
        st.subheader("Sketchpad")
        # Initialize draft notes session state if needed
        if "draft_notes" not in st.session_state:
            st.session_state["draft_notes"] = ""
        draft_notes = st.text_area(
            "Write your draft notes here...",
            value=st.session_state["draft_notes"],
            height=200,
            key="draft_notes_area"
        )
        if st.button("Save Draft"):
            if draft_notes.strip():
                st.session_state["draft_notes"] = draft_notes
                st.success("Draft notes saved locally.")
            else:
                st.error("Please write something in your draft notes before saving.")

        st.write("---")

        st.subheader("Final Submission")
        # Initialize final submission session state if needed
        if "final_submission" not in st.session_state:
            st.session_state["final_submission"] = ""
        final_submission = st.text_area(
            "Write your final version here...",
            value=st.session_state["final_submission"],
            height=200,
            key="final_submission_area"
        )
        if st.button("Submit Final"):
            if final_submission.strip():
                st.session_state["final_submission"] = final_submission
                st.success("Your final version has been submitted!")
                # Optional: Save data with participant ID
                save_participant_data(st.session_state.participant_id, final_submission)
            else:
                st.error("Please write your final version before submitting.")

def save_participant_data(participant_id, story_text):
    """Save participant data to a file (optional)"""
    import datetime
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    try:
        with open("participant_data.txt", "a", encoding="utf-8") as f:
            # Escape any commas or newlines in the story text for CSV format
            clean_story = story_text.replace("\n", " ").replace(",", ";")
            f.write(f"{timestamp},{participant_id},{clean_story}\n")
    except Exception as e:
        st.error(f"Error saving data: {e}")

def main():
    """Main app function with page routing"""
    
    # Initialize session state
    if 'page' not in st.session_state:
        st.session_state.page = "participant_id"
    if 'participant_id' not in st.session_state:
        st.session_state.participant_id = None
    
    # Page routing
    if st.session_state.page == "participant_id":
        participant_id_page()
    elif st.session_state.page == "story_task":
        story_writing_page()
    else:
        # Fallback to participant ID page
        st.session_state.page = "participant_id"
        participant_id_page()

if __name__ == "__main__":
    main()