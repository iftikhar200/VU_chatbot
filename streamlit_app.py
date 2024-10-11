import streamlit as st
from langchain_groq import ChatGroq

# Show title and description.
st.title("💬 Educational Chatbot")
st.write(
    "This chatbot uses the Groq model (LLaMA 3) to generate educational responses. "
    "You need to provide your Groq API key, which you can get from your Groq account."
)

# Ask user for their Groq API key via `st.text_input`.
openai_api_key = st.text_input("Groq API Key", type="password")
if not openai_api_key:
    st.info("Please add your Groq API key to continue.", icon="🗝️")
else:
    # Create a ChatGroq client.
    llm = ChatGroq(
        temperature=0,
        api_key=openai_api_key,
        model_name="llama3-70b-8192"
    )

    # Create a session state variable to store the chat messages. This ensures that the
    # messages persist across reruns.
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display the existing chat messages via `st.chat_message`.
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Create a chat input field to allow the user to enter a message.
    if prompt := st.chat_input("Ask me an educational question!"):

        # Store and display the current prompt.
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate a response using the Groq API.
        input_prompt = f"""
        You are an educational chatbot designed to provide information and answer questions related to various subjects, such as science, math, literature, history, and more. Your primary goal is to help users learn and grow. If a user asks a question that is not related to education, respond politely with a friendly message, encouraging them to ask about something educational.

        Example Responses:

        Educational Query:
        User: "Can you explain photosynthesis?"
        Chatbot: "Sure! Photosynthesis is the process by which green plants convert sunlight into energy. Would you like to know more about how it works?"

        Off-Topic Query:
        User: "What's your favorite movie?"
        Chatbot: "That's a great question! However, I'm here to help with educational topics. What would you like to learn about today?"

        User: "{prompt}"
        Chatbot:
        """

        # Invoke the Groq model.
        response = llm.invoke(input_prompt)

        # Display the assistant's response.
        with st.chat_message("assistant"):
            st.markdown(response.content)

        # Append the response to the session state.
        st.session_state.messages.append({"role": "assistant", "content": response.content})
