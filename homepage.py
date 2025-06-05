import base64
import streamlit as st
from PIL import Image
import numpy as np
import io

st.set_page_config(page_title="Shadow Ink", layout="wide")
st.title("Shadow Ink✒")

def get_img_as_base64(file):
    with open(file,"rb") as f:
        data=f.read()
    return base64.b64encode(data).decode()

img=get_img_as_base64("background.png")


page_bg_img=f"""
<style>

[data-testid="stAppViewContainer"] {{
background-image:url("data:background/png;base64,{img}");
background-size:cover;
}}

[data-testid="stHeader"] {{
background:rgba(0,0,0,0);
}}
</style>
"""
st.markdown(page_bg_img,unsafe_allow_html=True)

def encode_message(image: Image.Image, message: str) -> Image.Image:
    image = image.convert("RGB")
    data = np.array(image)
    binary_message = ''.join([format(ord(char), '08b') for char in message]) + '1111111111111110'  # EOF marker

    flat_data = data.flatten()
    if len(binary_message) > len(flat_data):
        raise ValueError("Message is too long to encode in the image.")

    for i in range(len(binary_message)):
        flat_data[i] = (flat_data[i] & ~1) | int(binary_message[i])

    encoded_data = flat_data.reshape(data.shape)
    encoded_image = Image.fromarray(encoded_data.astype('uint8'), 'RGB')
    return encoded_image

def decode_message(image: Image.Image) -> str:
    image = image.convert("RGB")
    data = np.array(image).flatten()
    bits = [str(pixel & 1) for pixel in data]

    chars = []
    for i in range(0, len(bits), 8):
        byte = bits[i:i+8]
        if len(byte) < 8:
            break
        char = chr(int(''.join(byte), 2))
        chars.append(char)
        if ''.join(format(ord(c), '08b') for c in chars[-2:]) == '1111111111111110':
            return ''.join(chars[:-2])
    return ''.join(chars)

st.markdown(
    "*Steganography is the practice of hiding secret information within an ordinary medium such as an image, audio, or video. "
    "Unlike encryption, which makes data unreadable, steganography conceals the existence of the message itself. "
    "This application allows you to hide or reveal messages within image files using the Least Significant Bit (LSB) technique.*"
)
st.markdown("Hide or reveal secret messages in images using LSB steganography.")

option = st.radio("Choose operation", ['Encode', 'Decode'])

if option == 'Encode':
    uploaded_image = st.file_uploader("Upload Image (PNG/JPEG)", type=["png", "jpg", "jpeg"])
    message = st.text_area("Enter message to encode")

    if st.button("Encode"):
        if uploaded_image and message:
            try:
                image = Image.open(uploaded_image)
                encoded_img = encode_message(image, message)

                buf = io.BytesIO()
                encoded_img.save(buf, format='PNG')
                byte_im = buf.getvalue()

                st.success("Message successfully encoded into image.")
                st.image(encoded_img, caption="Encoded Image", use_column_width=True)
                st.download_button("Download Encoded Image", data=byte_im, file_name="encoded_image.png", mime="image/png")
            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.warning("Please upload an image and enter a message.")

elif option == 'Decode':
    uploaded_image = st.file_uploader("Upload Image to Decode", type=["png", "jpg", "jpeg"])

    if st.button("Decode"):
        if uploaded_image:
            try:
                image = Image.open(uploaded_image)
                hidden_msg = decode_message(image)
                st.success("Message decoded successfully:")
                st.code(hidden_msg, language='text')
            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.warning("Please upload an image.")