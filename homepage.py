import base64
import streamlit as st
from PIL import Image
import numpy as np
import io
from streamlit_option_menu import option_menu # <-- Import the new component

# --- Page Configuration ---
st.set_page_config(page_title="Shadow Ink", layout="wide")
st.title("Shadow Ink ✒️")

# --- Background Image Functionality ---
def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Use a placeholder or ensure background.png exists
# To avoid errors, you can wrap this in a try-except block
try:
    img = get_img_as_base64("background.png")
    page_bg_img = f"""
    <style>
    [data-testid="stAppViewContainer"] > .main {{
        background-image: url("data:image/png;base64,{img}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    [data-testid="stHeader"] {{
        background: rgba(0,0,0,0);
    }}
    </style>
    """
    st.markdown(page_bg_img, unsafe_allow_html=True)
except FileNotFoundError:
    st.warning("background.png not found. The app will run with a plain background.")


# --- Core Steganography Functions ---
def encode_message(image: Image.Image, message: str, passkey: str) -> Image.Image:
    """
    Encodes the message into the image using LSB steganography,
    prepending the passkey and a separator.
    """
    image = image.convert("RGB")
    data = np.array(image)
    full_message = f"{passkey}:{message}"
    
    # Convert each character to its 8-bit binary representation
    binary_message = ''.join(format(ord(char), '08b') for char in full_message)
    # Add a unique End-Of-File (EOF) marker
    binary_message += '1111111111111110' 

    if len(binary_message) > data.size:
        raise ValueError("Message is too long to encode in this image.")

    flat_data = data.flatten()
    for i in range(len(binary_message)):
        # Modify the least significant bit
        flat_data[i] = (flat_data[i] & 0b11111110) | int(binary_message[i])

    encoded_data = flat_data.reshape(data.shape)
    encoded_image = Image.fromarray(encoded_data.astype('uint8'), 'RGB')
    return encoded_image

def decode_message(image: Image.Image, passkey: str) -> str:
    """
    Decodes the message from the image, validates the passkey,
    and returns the hidden message.
    """
    image = image.convert("RGB")
    data = np.array(image).flatten()
    
    binary_message = ""
    eof_marker = "1111111111111110"
    
    for pixel_value in data:
        binary_message += str(pixel_value & 1)
        # Check if the EOF marker is found
        if binary_message.endswith(eof_marker):
            break
    else:
        return "No hidden message found or message is corrupted (EOF marker not found)."

    binary_message = binary_message[:-len(eof_marker)]

    message_chars = []
    for i in range(0, len(binary_message), 8):
        byte = binary_message[i:i+8]
        if len(byte) == 8:
            message_chars.append(chr(int(byte, 2)))
    
    decoded_full_message = "".join(message_chars)

    if ':' not in decoded_full_message:
        return "Incorrect passkey or corrupted data."

    embedded_passkey, message = decoded_full_message.split(':', 1)
    
    if embedded_passkey == passkey:
        return message
    else:
        return "Incorrect passkey!"


# --- App Introduction ---
st.markdown(
    """
    *Steganography is the practice of hiding secret information within an ordinary medium such as an image.
    Unlike encryption, which makes data unreadable, steganography conceals the existence of the message itself.
    This application allows you to hide or reveal messages within image files using the Least Significant Bit (LSB) technique.*
    """
)
st.markdown("### Hide or reveal secret messages in your images")

option = option_menu(
    menu_title=None,  # No title for the menu
    options=["Encode", "Decode"],
    icons=["lock-fill", "unlock-fill"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "transparent"},
        "icon": {"font-size": "20px"},
        "nav-link": {
            "font-size": "18px",
            "text-align": "center",
            "margin": "0px 5px",
            "padding": "10px 15px",
            "--hover-color": "#444",
            "border-radius": "8px",
        },
        "nav-link-selected": {"background-color": "#FF4500", "color": "white"},
    }
)

if option == 'Encode':
    uploaded_image = st.file_uploader("Upload Image (PNG/JPEG)", type=["png", "jpg", "jpeg"])
    message = st.text_area("Enter message to encode")
    passkey = st.text_input("Enter passkey for decoding", type="password")

    if st.button("Encode"):
        if uploaded_image and message and passkey:
            try:
                image = Image.open(uploaded_image)
                encoded_img = encode_message(image, message, passkey)

                buf = io.BytesIO()
                encoded_img.save(buf, format='PNG')
                byte_im = buf.getvalue()

                st.success("Message successfully encoded into image.")
                st.image(encoded_img, caption="Encoded Image", use_column_width=True)
                st.download_button("Download Encoded Image", data=byte_im, file_name="encoded_image.png", mime="image/png")
            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.warning("Please upload an image, enter a message, and a passkey.")

elif option == 'Decode':
    st.subheader("Decode a Message")
    uploaded_image = st.file_uploader("Upload an image to decode", type=["png", "jpg", "jpeg"])
    passkey = st.text_input("Enter the passkey", type="password")

    if st.button("Decode Message", type="primary"):
        if uploaded_image and passkey:
            with st.spinner("Decoding..."):
                try:
                    image = Image.open(uploaded_image)
                    hidden_msg = decode_message(image, passkey)

                    if hidden_msg == "Incorrect passkey!":
                        st.error(hidden_msg)
                    elif "corrupted" in hidden_msg or "No hidden message" in hidden_msg:
                        st.warning(hidden_msg)
                    else:
                        st.success("Message decoded successfully:")
                        st.code(hidden_msg, language='text')

                except Exception as e:
                    st.error(f"An error occurred: {e}")
        else:
            st.warning("Please upload an image and enter the passkey.")
