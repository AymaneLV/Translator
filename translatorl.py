from gtts import gTTS
from easygoogletranslate import EasyGoogleTranslate
import customtkinter as tk
import pyperclip as pp
import os
import playsound

# Initialize the translator
translator = EasyGoogleTranslate(timeout=10)

# Language codes
languages = {
    'English': 'en',
    'Arabic': 'ar',
    'Chinese (Simplified)': 'zh-CN',
    'Chinese (Traditional)': 'zh-TW',
    'French': 'fr',
    'German': 'de',
    'Italian': 'it',
    'Japanese': 'ja',
    'Portuguese': 'pt',
    'Russian': 'ru',
    'Spanish': 'es',
    'Turkish': 'tr',
    
}

# Function to toggle light/dark mode
def toggle_mode():
    if mode_switch.get() == "Dark":  # Dark Mode
        update_theme("#212529", "white", "white" , "#3b3a3a")  # Black background
    else:  # Light Mode
        update_theme("#FFFFFF", "black", "black" , "#cfcaca" )  # White background

def update_theme(bg_color, text_color, border_color , fg_color ):
    app.configure(bg_color=bg_color , fg_color=fg_color)  # Change the app background
    frame.configure(fg_color=bg_color)  # Change frame color
    original_text_box.configure(text_color=text_color, fg_color=fg_color, border_color=border_color)
    translated_text_box.configure(text_color=text_color, fg_color=fg_color, border_color=border_color)
    sun_icon_label.configure(text_color=text_color)
    moon_icon_label.configure(text_color=text_color)

def translate():
    original_text = original_text_box.get("1.0", "end").strip()
    source_lang = languages.get(source_lang_combo.get())
    target_lang = languages.get(target_lang_combo.get())

    if source_lang and target_lang and original_text:
        translated = translator.translate(text=original_text, source_language=source_lang, target_language=target_lang)
        translated_text_box.delete("1.0", "end")
        translated_text_box.insert("1.0", translated)
    else:
        print("Please check your input.")

def clear_fields():
    original_text_box.delete("1.0", "end")
    translated_text_box.delete("1.0", "end")

def invert_languages():
    source, target = source_lang_combo.get(), target_lang_combo.get()
    source_lang_combo.set(target)
    target_lang_combo.set(source)

def copy_to_clipboard():
    pp.copy(translated_text_box.get("1.0", "end").strip())

def read_text(text_box, lang_combo):
    text = text_box.get("1.0", "end").strip()
    lang = languages.get(lang_combo.get())

    if text and lang:
        try:
            tts = gTTS(text=text, lang=lang)
            temp_file = "temp_audio.mp3"
            tts.save(temp_file)
            playsound.playsound(temp_file)
            os.remove(temp_file)
        except Exception as e:
            print(f"Error in text-to-speech: {e}")

# Initialize the main window
app = tk.CTk()
app.title("Light Translate")
app.geometry("520x720")  # Adjusted size for new elements
app.configure(bg_color="#212529")  # Default to dark mode

# UI Elements
frame = tk.CTkFrame(app, corner_radius=10, fg_color="#212529")  # Black background
frame.pack(padx=10, pady=10, fill="both", expand=True)

font = ("Calibri bold", 15)
text_font = ("Calibri bold", 20)

source_lang_combo = tk.CTkComboBox(frame, values=list(languages.keys()), font=font, width=160)
source_lang_combo.set("English")
source_lang_combo.grid(row=0, column=0, padx=10, pady=10)

target_lang_combo = tk.CTkComboBox(frame, values=list(languages.keys()), font=font, width=160)
target_lang_combo.set("Arabic")
target_lang_combo.grid(row=0, column=2, padx=10, pady=10)

invert_button = tk.CTkButton(frame, text="Invert", command=invert_languages, font=font, width=80)
invert_button.grid(row=0, column=1, padx=10, pady=10)

original_text_box = tk.CTkTextbox(
    frame,
    font=text_font,
    height=200,
    corner_radius=10,
    fg_color="#636262",
    text_color="white",
    border_color="white",
    border_width=2,
)
original_text_box.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

read_original_button = tk.CTkButton(frame, text="Read", command=lambda: read_text(original_text_box, source_lang_combo), font=font, width=80)
read_original_button.grid(row=1, column=2, padx=10, pady=10)

translated_text_box = tk.CTkTextbox(
    frame,
    font=text_font,
    height=200,
    corner_radius=10,
    fg_color="#636262",
    text_color="white",
    border_color="white",
    border_width=2,
)
translated_text_box.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

read_translated_button = tk.CTkButton(frame, text="Read", command=lambda: read_text(translated_text_box, target_lang_combo), font=font, width=80)
read_translated_button.grid(row=2, column=2, padx=10, pady=10)

translate_button = tk.CTkButton(frame, text="Translate", command=translate, font=font, width=120, fg_color="#0ead69")
translate_button.grid(row=3, column=0, padx=10, pady=10)

clear_button = tk.CTkButton(frame, text="Clear", command=clear_fields, font=font, width=120, fg_color="#b21e35")
clear_button.grid(row=3, column=1, padx=10, pady=10)

copy_button = tk.CTkButton(frame, text="Copy", command=copy_to_clipboard, font=font, width=120)
copy_button.grid(row=3, column=2, padx=10, pady=10)

# Mode Toggle Switch
mode_switch = tk.CTkSwitch(frame, text="", command=toggle_mode, onvalue="Dark", offvalue="Light", width=60)
mode_switch.select()  # Default to dark mode
mode_switch.grid(row=4, column=1, pady=20)

# Icons for Sun and Moon
sun_icon_label = tk.CTkLabel(frame, text="☀️", font=("Arial", 18), text_color="white")
sun_icon_label.grid(row=4, column=0, sticky="e", padx=10)

moon_icon_label = tk.CTkLabel(frame, text="🌙", font=("Arial", 18), text_color="white")
moon_icon_label.grid(row=4, column=2, sticky="w", padx=10)

app.mainloop()
