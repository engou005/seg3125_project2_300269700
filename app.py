import gradio as gr
from groq import Groq

# Initialize API client
api_key = "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"
client = Groq(api_key=api_key)

def get_static_anxiety_advice(history):
    """Adds quick anxiety tips as a chatbot response in the conversation history."""
    tips = "Here are some quick tips to manage anxiety:\n\n- Take deep breaths.\n- Practice mindfulness.\n- Get enough sleep.\n- Limit caffeine and alcohol.\n- Talk to a trusted friend.\n- Engage in physical activity."
    history.append(("💡 Quick Tips", tips))
    return history

def get_stream_anxiety_advice(user_input, history):
    """Fetches chatbot response and updates conversation history."""
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are an expert in anxiety management and mental health."},
                {"role": "user", "content": user_input},
            ],
            temperature=0.7,
            max_tokens=300,
            top_p=1
        )
        chatbot_reply = response.choices[0].message.content
    except Exception as e:
        chatbot_reply = f"Error: {e}"

    history.append((user_input, chatbot_reply))
    return history

# Build UI using Gradio's Chatbot component
with gr.Blocks(theme=gr.themes.Soft(primary_hue="blue"), css="""
    body { background-color: #D6EAF8; } /* Baby blue background */
    .chat-container {
        margin: 20px auto;
        max-width: 700px;
        width: 90%;
        background: #D6EAF8; 
        border-radius: 12px;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.2); /* Soft shadow effect */
        padding: 15px;
    }
    #chat_history {
        border: 2px solid rgba(255, 255, 255, 0.4); /* Light semi-transparent border */
        background: rgba(255, 255, 255, 0.6); /* Slight transparency */
        padding: 10px;
        border-radius: 10px;
        box-shadow: 0px 3px 8px rgba(0,0,0,0.15); /* Shadowed messages */
    }
    .message {
        padding: 8px 12px;
        margin: 6px 0;
        border-radius: 8px;
    }
    .user { background: #A7C7E7; align-self: flex-end; } /* Soft blue for user */
    .bot { background: #FFFFFF; align-self: flex-start; } /* White for bot */
    #header-text {
        text-align: center;
        font-size: 25px;
        font-weight: bold;
    }
    #subheader-text {
        text-align: center;
        font-size: 20px;
        font-weight: bold;
    }
""") as interface:

    with gr.Column(elem_classes=["chat-container"]):
        gr.Markdown("<div id='header-text'>Anxiety Support Chatbot</div>")
        gr.Markdown("<div id='subheader-text'>💙 Get expert advice to ease your mind</div>")

        # Chatbot component to display conversation with shadows
        chatbot = gr.Chatbot(label="Chat", elem_id="chat_history")

        # User input box
        user_input = gr.Textbox(placeholder="Type your question here...", lines=2, show_label=False)

        # Buttons
        with gr.Row():
            send_btn = gr.Button("Send", variant="primary")
            advice_btn = gr.Button("💡 Quick Tips", variant="secondary")

        # Button actions
        send_btn.click(get_stream_anxiety_advice, inputs=[user_input, chatbot], outputs=chatbot)
        advice_btn.click(get_static_anxiety_advice, inputs=chatbot, outputs=chatbot)

# Launch interface
interface.launch()
