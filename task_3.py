def is_after_6pm():
    now = datetime.now()
    return now.hour >= 18  # 6 PM in 24-hour format
# Function to handle microphone button click
def start_recording():
    if not is_after_6pm():
        messagebox.showerror("Please try after 6 PM IST.")
        return
def recognize_speech():
        r = sr.Recognizer()
        with sr.Microphone() as source:
            text_input.delete("1.0", "end")
            translation_output.delete("1.0", "end")
            message_text.delete("1.0", "end") 
            message_text.insert(tk.END, "Listening...\n")
            audio_data = r.record(source, duration=5)  # Record audio for 5 seconds or adjust as needed
        try:
            message_text.insert(tk.END, "Recognizing...\n")
            recognized_text = r.recognize_google(audio_data)
            print("Recognized Text:", recognized_text)
            text_input.delete("1.0", "end")  # Clear existing text
            text_input.insert("end", recognized_text)
            message_text.delete("1.0", "end") 

       # Check if the text starts with "M" or "O"
           if recognized_text and recognized_text[0].upper() in ['M', 'O']:
                raise ValueError("Please repeat, avoiding words starting with M or O.")

            # Translate the recognized English text to Hindi
            translator = Translator()
            translation = translator.translate(recognized_text, src='en', dest='hi')
            translated_text = translation.text
            translation_output.delete("1.0", "end")  # Clear existing translation
            translation_output.insert("end", translated_text)
        except sr.UnknownValueError:
            messagebox.showerror("Recognition could not understand the audio. Please speak one more time.")
        except ValueError as ve:
            print(f"Error: {ve}")
            translation_output.delete("1.0", "end")  # Clear existing translation
            translation_output.insert("end", str(ve))

    threading.Thread(target=recognize_speech).start()

# Setting up the main window
root = tk.Tk()
root.title("Language Translator")
root.geometry("550x600")

# Font configuration
font_style = "Times New Roman"
font_size = 14

# Frame for input
input_frame = tk.Frame(root)
input_frame.pack(pady=10)

# Heading for input
input_heading = tk.Label(input_frame, text="Enter the text to be translated", font=(font_style, font_size, 'bold'))
input_heading.pack()
# Text input for English sentence
text_input = tk.Text(input_frame, height=5, width=50, font=(font_style, font_size))
text_input.pack()

# Language selection
language_var = tk.StringVar()
language_label = tk.Label(root, text="Select the language to translate to", font=(font_style, font_size, 'bold'))
language_label.pack()
language_select = ttk.Combobox(root, textvariable=language_var, values=["French", "Spanish"], font=(font_style, font_size), state="readonly")
language_select.pack()

# Submit button
submit_button = ttk.Button(root, text="Translate", command=handle_translate)
submit_button.pack(pady=10)

# Frame for output
output_frame = tk.Frame(root)
output_frame.pack(pady=10)
# Heading for output
output_heading = tk.Label(output_frame, text="Translation: ", font=(font_style, font_size, 'bold'))
output_heading.pack()
# Text output for translations
translation_output = tk.Text(output_frame, height=5, width=50, font=(font_style, font_size))
translation_output.pack()

# Microphone button
mic_button = ttk.Button(root, text="🎤", command=start_recording)
mic_button.pack(pady=10)
text_input.bind("<KeyPress>", suggest_words)
message_text = tk.Text(root, height=2, width=50, font=(font_style, font_size))
message_text.pack()
# Running the application
root.mainloop()
