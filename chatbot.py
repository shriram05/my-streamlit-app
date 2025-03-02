
from dotenv import load_dotenv
from groq import Groq 
import os 
import gradio as gr

# Load environment variables and initialize Groq client
load_dotenv()
llm = Groq(api_key=os.getenv("GROQ_API_KEY"))

def get_completion_from_messages(messages, model="mixtral-8x7b-32768", temperature=0):
    """
    Get a completion from the Groq API based on the conversation history
    
    Args:
        messages: List of message objects with 'role' and 'content'
        model: The model to use for completion
        temperature: Controls randomness (0 = deterministic, 1 = creative)
    
    Returns:
        The content of the assistant's response
    """
    response = llm.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
    )
    return response.choices[0].message.content

def predict(message, history):
    """
    Process user message and conversation history to generate a response
    
    Args:
        message: The current user message
        history: List of previous [user_message, assistant_response] pairs
    
    Returns:
        Generated response from the assistant
    """
    # Format conversation history for the API
    messages = []
    for historymessage in history:
        messages.append({'role': 'user', 'content': historymessage[0]})
        messages.append({'role': 'assistant', 'content': historymessage[1]})
    
    # Add the current message
    messages.append({'role': 'user', 'content': message})
    
    # Get response from the model
    response = get_completion_from_messages(messages)
    
    # Debug prints
    print(" History = ", history)
    print(" Message = ", message)
    
    return response

# The ChatInterface is imported and used in app.py
# This allows the module to be imported without automatically launching
# when imported by another script
if __name__ == "__main__":
    # If this file is run directly, launch the chat interface
    chat_interface = gr.ChatInterface(predict)
    chat_interface.launch()