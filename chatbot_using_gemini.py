import google.generativeai as genai
import PIL.Image
import chainlit as cl

genai.configure(api_key='gemini_api_key')

# Initialize the generative model and start the chat
model = genai.GenerativeModel(model_name="gemini-1.5-flash")
chat_session = model.start_chat(history=[])

def load_image(image_path):
    """
    Load an image from the specified path using PIL.

    Args:
        image_path (str): The path to the image file.

    Returns:
        PIL.Image: The loaded image object.
    """
    image = PIL.Image.open(image_path)
    return image

@cl.on_message
async def handle_message(message: cl.Message):
    """
    Process incoming messages, handle images, and respond using a generative AI model.

    Args:
        message (cl.Message): The incoming message object.
    """
    try:
        prompt = message.content
        image_files = [file for file in message.elements if "image" in file.mime]

        if image_files:
            image = load_image(image_files[0].path)
            prompt = [prompt, image]

        response = chat_session.send_message(prompt)
        response_message = cl.Message(content=response.text)

        await response_message.send()

    except Exception as e:
        error_message = cl.Message(content=f"An error occurred: {str(e)}")
        await error_message.send()
