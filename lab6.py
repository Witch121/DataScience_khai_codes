import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import google.generativeai as genai
import json
import os

# Load API key from config.json
def load_api_key():
    try:
        with open("config.json", "r") as file:
            config = json.load(file)
        api_key = config.get("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("API key not found in config.json")
        return api_key
    except (FileNotFoundError, ValueError, json.JSONDecodeError) as e:
        messagebox.showerror("Error", f"API key error: {e}")
        exit()

# Load and configure Gemini AI
API_KEY = load_api_key()
genai.configure(api_key=API_KEY)

# Analyze code for vulnerabilities
def analyze_code(code):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(
            f"Analyze the following code for potential security vulnerabilities. List the risks and suggest fixes:\n{code}"
        )
        return response.text if response.text else "No vulnerabilities detected."
    except Exception as e:
        return f"Error analyzing code: {e}"

# Analyzing text input
def analyze_text():
    code = text_input.get("1.0", tk.END).strip()
    if code:
            result = analyze_code(code)
            output_text.config(state="normal")  # Enable editing to update text
            output_text.delete("1.0", tk.END)
            output_text.insert("1.0", result)
            output_text.config(state="disabled")  # Disable text editing
    else:
            messagebox.showwarning("Error", "Please enter some code!")

# Loading code from a file
def load_file():
    file_path = filedialog.askopenfilename(filetypes=[("Python Files", "*.py"), ("All Files", "*.*")])
    if file_path:
        with open(file_path, "r", encoding="utf-8") as file:
            text_input.delete("1.0", tk.END)
            text_input.insert("1.0", file.read())

# Create main window
root = tk.Tk()
root.title("Code Vulnerability Analyzer (Powered by Gemini)")
root.geometry("700x500")
root.configure(bg="#adade8")

# Set window icon
icon_path = "src/img/avatar1.png"
if os.path.exists(icon_path):
    root.iconphoto(False, tk.PhotoImage(file=icon_path))

# Bit more styling
font_large = ("Arial", 14, "bold")
font_medium = ("Arial", 12)
btn_color = "#52adeb"

# Create main frame for better layout
frame = tk.Frame(root, bg="#adade8", padx=20, pady=20)
frame.pack(pady=10)

# Widgets inside frame
tk.Label(frame, text="Enter your code or upload a file:", font=font_large, bg="#adade8").pack(pady=5)

text_input = scrolledtext.ScrolledText(frame, height=10, width=60, 
                     bg="#ECF0F1",
                     fg="#2C3E50", 
                     font=("Consolas", 12), 
                     insertbackground="black",
                     bd=2, relief="sunken") 
text_input.pack(pady=5)

tk.Button(frame, text="Upload File", command=load_file, bg=btn_color, font=font_medium, padx=10, pady=5).pack(pady=5)
tk.Button(frame, text="Analyze Code", command=analyze_text, bg=btn_color, font=font_medium, padx=10, pady=5).pack(pady=5)

result_label = tk.Label(frame, text="Results will be displayed here", 
                        wraplength=500, 
                        justify="left", 
                        font=font_medium, 
                        bg="#adade8")
result_label.pack(pady=5)

output_text = scrolledtext.ScrolledText(frame, 
                                        height=10, 
                                        width=90, 
                                        wrap="word",
                                        bg="#ECF0F1", 
                                        fg="#2C3E50", 
                                        font=("Consolas", 12))
output_text.pack(pady=5)
output_text.config(state="disabled")  # Read-only

root.mainloop()