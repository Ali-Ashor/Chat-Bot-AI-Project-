
import customtkinter as ctk
from tkinter import END
from groq import Groq
import threading

# ==========================================
# GROQ API KEY
# ==========================================

client = Groq(
    api_key="Enter your API"
)

# ==========================================
# APP SETTINGS
# ==========================================

ctk.set_appearance_mode("grey")
ctk.set_default_color_theme("dark-blue")

app = ctk.CTk()
app.geometry("1400x800")
app.title("SB ChatBot")

# ==========================================
# SIDEBAR
# ==========================================

sidebar = ctk.CTkFrame(app, width=250, corner_radius=0)
sidebar.pack(side="left", fill="y")

logo = ctk.CTkLabel(
    sidebar,
    text="SB Assistant",
    font=("Arial", 28, "bold")
)
logo.pack(pady=30)

# ==========================================
# NEW CHAT BUTTON
# ==========================================

def clear_chat():
    chat_area.delete("1.0", END)
    chat_area.insert(
        END,
        "SB Assistant:\nHello! How can I help you today?\n\n"
    )

new_chat_btn = ctk.CTkButton(
    sidebar,
    text="+ New Chat",
    height=45,
    corner_radius=15,
    font=("Arial", 16, "bold"),
    command=clear_chat
)

new_chat_btn.pack(padx=20, pady=10, fill="x")


main_frame = ctk.CTkFrame(app, corner_radius=0)
main_frame.pack(side="right", fill="both", expand=True)

header = ctk.CTkLabel(
    main_frame,
    text="SB ChatBot",
    font=("Arial", 30, "bold")
)

header.pack(pady=20)

# ==========================================
# CHAT AREA
# ==========================================

chat_frame = ctk.CTkFrame(main_frame, corner_radius=20)
chat_frame.pack(fill="both", expand=True, padx=20, pady=10)

chat_area = ctk.CTkTextbox(
    chat_frame,
    wrap="word",
    font=("Consolas", 16),
    corner_radius=15
)

chat_area.pack(fill="both", expand=True, padx=15, pady=15)

chat_area.insert(
    END,
    "SB Assistant:\nHello! How can I help you today?\n\n"
)

# ==========================================
# INPUT FRAME
# ==========================================

input_frame = ctk.CTkFrame(main_frame, height=100)
input_frame.pack(fill="x", padx=20, pady=20)

entry = ctk.CTkEntry(
    input_frame,
    height=55,
    font=("Arial", 16),
    corner_radius=20,
    placeholder_text="Type your message here..."
)

entry.pack(
    side="left",
    fill="x",
    expand=True,
    padx=(10, 10),
    pady=15
)

send_btn = ctk.CTkButton(
    input_frame,
    text="Send",
    width=120,
    height=55,
    corner_radius=20,
    font=("Arial", 16, "bold")
)

send_btn.pack(side="right", padx=10, pady=15)

# ==========================================
# AI RESPONSE FUNCTION
# ==========================================

def get_ai_response(prompt):

    try:

        completion = client.chat.completions.create(

            model="llama-3.3-70b-versatile",

            messages=[
                {
                    "role": "system",
                    "content": "You are a professional AI assistant."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=0.7,
            max_tokens=1024

        )

        return completion.choices[0].message.content

    except Exception as e:

        return f"Error: {e}"

# ==========================================
# PROCESS AI RESPONSE
# ==========================================

def process_ai_response(user_message):

    ai_reply = get_ai_response(user_message)

    # Remove typing text
    chat_area.delete("end-3l", "end")

    # Insert AI response
    chat_area.insert(
        END,
        f"User:\n{ai_reply}\n\n"
    )

    chat_area.see(END)

# ==========================================
# SEND MESSAGE FUNCTION
# ==========================================

def send_message(event=None):

    user_message = entry.get().strip()

    if user_message == "":
        return

    # Show user message
    chat_area.insert(
        END,
        f" You:\n{user_message}\n\n"
    )

    entry.delete(0, END)

    # Typing effect
    chat_area.insert(
        END,
        "SB Assistant:\nTyping...\n\n"
    )

    chat_area.see(END)

    # Threading
    threading.Thread(
        target=process_ai_response,
        args=(user_message,),
        daemon=True
    ).start()

# ==========================================
# ENTER KEY SUPPORT
# ==========================================

entry.bind("<Return>", send_message)

send_btn.configure(command=send_message)

# ==========================================
# START APP
# ==========================================

app.mainloop()