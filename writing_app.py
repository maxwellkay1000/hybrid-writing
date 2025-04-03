import streamlit as st
import openai
import os

# Set OpenAI API key
openai.api_key = os.environ.get("OPENAI_API_KEY")

st.title("🔎 Story Writing Task")
st.write("""
Story Writing Task
In the text box below, please write a short story (about four sentences long) that includes the following three words: “stamp,” “send,” and “letter.”
Be as creative as you can—your story can be any style you imagine.
 
Important: You are required to use ChatGPT to help write your story. We have already set it up for you, and you must use it at least once during your writing process. You can use ChatGPT to help brainstorm, get information, improve phrasing, write or co-write the text of your story, or in any other way that is useful.

You can prompt ChatGPT as many times and as often as you’d like. Feel free to copy and paste any parts from the interaction and edit them as much as you like if you want to change what ChatGPT wrote.
 
Important reminders:
Please use the same ChatGPT session and window throughout this task.
Do not use any tool for writing other than ChatGPT.
At the end of the session, please do not delete your session history.
Once you feel ready, you may click the “Next” button to submit your story.


Use the chatbot on the left to help organize your thoughts. On the right, you have space to work on a draft and then finalize your reflection.
""")

# Initialize session state for chatbot messages and user input
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": "You are a helpful assistant for reflective writing exercises."}
    ]
if "user_input" not in st.session_state:
    st.session_state["user_input"] = ""

# Function to handle sending chat messages
def send_message():
    user_input = st.session_state.user_input
    if user_input.strip():
        st.session_state["messages"].append({"role": "user", "content": user_input})
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=st.session_state["messages"]
            )
            bot_message = response["choices"][0]["message"]["content"]
            st.session_state["messages"].append({"role": "assistant", "content": bot_message})
        except openai.OpenAIError as e:
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
    st.subheader("Draft Notes")
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
        "Write your final reflection here...",
        value=st.session_state["final_submission"],
        height=200,
        key="final_submission_area"
    )
    if st.button("Submit Final"):
        if final_submission.strip():
            st.session_state["final_submission"] = final_submission
            st.success("Your final version has been submitted!")
        else:
            st.error("Please write your final reflection before submitting.")




