import gradio as gr
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Function to handle chat interactions


def chat_with_grok(message, history, system_message, model_name, temperature, max_tokens):
    # In a real implementation, this would call the Grok API
    # For now, we'll just echo the inputs to demonstrate the UI is working
    response = f"You selected model: {model_name}\nSystem message: {system_message}\nTemperature: {temperature}\nMax tokens: {max_tokens}\n\nYour message: {message}"
    history.append((message, response))
    return history


# Create the Gradio interface
with gr.Blocks(theme=gr.themes.Soft(primary_hue="orange")) as demo:
    gr.Markdown("# Grok AI Chat Interface")

    with gr.Row():
        with gr.Column(scale=3):
            # Main chat interface
            chatbot = gr.Chatbot(
                height=600,
                show_copy_button=True,
                avatar_images=(
                    "https://img.icons8.com/fluency/64/user-female-circle.png",
                    "https://img.icons8.com/fluency/64/chatbot.png"),
                bubble_full_width=False,
            )

            # Message input
            msg = gr.Textbox(
                placeholder="Send a message...",
                container=False,
                scale=7,
                show_label=False,
            )

            with gr.Row():
                submit_btn = gr.Button("Send", variant="primary", scale=1)
                clear_btn = gr.Button("Clear", variant="secondary", scale=1)

        with gr.Column(scale=1):
            # Model settings sidebar
            gr.Markdown("### Model Settings")

            model_dropdown = gr.Dropdown(
                choices=["grok-1", "grok-2", "grok-3-beta"],
                value="grok-3-beta",
                label="Model"
            )

            system_message = gr.Textbox(
                placeholder="You are a helpful AI assistant...",
                label="System Message",
                lines=4
            )

            with gr.Accordion("Advanced Settings", open=False):
                temperature = gr.Slider(
                    minimum=0.0,
                    maximum=1.0,
                    value=0.7,
                    step=0.01,
                    label="Temperature"
                )

                max_tokens = gr.Slider(
                    minimum=100,
                    maximum=4000,
                    value=1000,
                    step=100,
                    label="Max Tokens"
                )

    # Set up event handlers
    submit_btn.click(
        chat_with_grok,
        inputs=[msg, chatbot, system_message,
                model_dropdown, temperature, max_tokens],
        outputs=[chatbot],
    ).then(
        lambda: "",
        None,
        msg,
        queue=False
    )

    msg.submit(
        chat_with_grok,
        inputs=[msg, chatbot, system_message,
                model_dropdown, temperature, max_tokens],
        outputs=[chatbot],
    ).then(
        lambda: "",
        None,
        msg,
        queue=False
    )

    clear_btn.click(lambda: None, None, chatbot, queue=False)

# Launch the app
if __name__ == "__main__":
    demo.launch()
