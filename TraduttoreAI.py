import json
import os
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import openai

CONFIG_FILE = "config.json"

def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f)

def load_config():
    config = {}
    if os.path.isfile(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            config = json.load(f)
    return config

def translate():
    language = language_combobox.get()
    input_text = input_textbox.get("1.0", "end-1c")
    if len(input_text.strip()) == 0:
        messagebox.showerror("Errore", "Inserire del testo da tradurre.")
    else:
        response = openai.Completion.create(
            engine="text-davinci-002", # specifica l'engine di OpenAI da utilizzare per la traduzione
            prompt=f"Translate '{input_text}' to {language}.",
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.5
        )
        output_text = response.choices[0].text.strip()
        output_textbox.delete("1.0", "end")
        output_textbox.insert("1.0", output_text)

def save_api_key():
    openai.api_key = api_key_textbox.get("1.0", "end-1c")
    config = load_config()
    config["api_key"] = openai.api_key
    save_config(config)
    settings_window.destroy()

root = tk.Tk()
root.title("Traduttore con OpenAI")

# carica la configurazione
config = load_config()
openai.api_key = config.get("api_key", "")

# finestra delle impostazioni
settings_window = tk.Toplevel(root)
settings_window.title("Impostazioni")
api_key_label = ttk.Label(settings_window, text="Inserisci la tua chiave API:")
api_key_label.grid(column=0, row=0, padx=5, pady=5)
api_key_textbox = tk.Text(settings_window, width=50, height=1)
api_key_textbox.insert("1.0", openai.api_key)
api_key_textbox.grid(column=1, row=0, padx=5, pady=5)
save_button = ttk.Button(settings_window, text="Salva", command=save_api_key)
save_button.grid(column=1, row=1, padx=5, pady=5)

language_label = ttk.Label(root, text="Lingua finale:")
language_label.grid(column=0, row=0, padx=5, pady=5)

language_combobox = ttk.Combobox(root, values=["ita", "fra", "esp", "eng"]) # sostituire con le lingue desiderate
language_combobox.grid(column=1, row=0, padx=5, pady=5)
language_combobox.current(0)

input_label = ttk.Label(root, text="Testo da tradurre:")
input_label.grid(column=0, row=1, padx=5, pady=5)

input_textbox = tk.Text(root, width=50, height=10, wrap="word")
input_textbox.grid(column=1, row=1, padx=5, pady=5)

output_label = ttk.Label(root, text="Testo tradotto:")
output_label.grid(column=0, row=2, padx=5, pady=5)

output_textbox = tk.Text(root, width=50, height=10, wrap="word")
output_textbox.grid(column=1, row=2, padx=5, pady=5)

translate_button = ttk.Button(root, text="Traduci", command=translate)
translate_button.grid(column=1, row=3, padx=5, pady=5)

root.mainloop()
