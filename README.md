# Shadow Ink ✒

**Shadow Ink** is a secure, user-friendly web application for hiding and revealing secret messages inside images using the Least Significant Bit (LSB) steganography technique. Unlike encryption, which makes data unreadable, steganography conceals the very existence of the message. Shadow Ink provides a beautiful interface, user authentication, and a seamless experience for private communication.

---

## 🚀 Features

- **User Authentication**  
  Secure sign-up and sign-in system with SQLite database.

- **Steganography**  
  Hide (encode) and reveal (decode) messages in images using the LSB technique.

- **Beautiful Interface**  
  Custom background, modern layout, and clear instructions.

- **Image Support**  
  Works with PNG and JPEG images.

- **Downloadable Results**  
  Download your encoded images with a single click.

---

## 🖼️ Demo

*Conceal. Reveal. Communicate in Silence.*

---

## 🛠️ Installation

1. **Clone the Repository**
    ```
    git clone https://github.com/your-username/shadow-ink.git
    cd shadow-ink
    ```

2. **Install Dependencies**
    ```
    pip install -r requirements.txt
    ```

3. **Add a Background Image**  
   Place your background image as `background.png` in the project root.

4. **Run the Application**
    ```
    streamlit run signin.py
    ```
    By default, the authentication page runs at [http://localhost:8501](http://localhost:8501).  
    On successful sign-in, the main app (homepage) will open in a new tab.

---

## 📄 Usage

1. **Sign Up** for a new account, or **Sign In** if you already have one.
2. After logging in, you will be redirected to the main Shadow Ink app.
3. Choose **Encode** to hide a message in an image, or **Decode** to reveal a hidden message.
4. Upload your image, enter your secret message (for encoding), and follow the prompts.
5. Download the resulting image or view the decoded message.

---

## 🧑‍💻 Project Structure

shadow-ink/
│
├── signin.py # Authentication (Sign In/Sign Up) page
├── homepage.py # Main steganography app (encode/decode)
├── users.db # SQLite database (created at runtime)
├── background.png # Custom background image
├── requirements.txt # Python dependencies
└── README.md
