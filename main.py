import time
import threading
from sensors import user_interaction_detected
from chatgpt_interface import ask_chatgpt
from output_devices import control_led, play_wav_file, stop_playback
from voice_recognition import recognize_speech_from_mic



import tkinter as tk
from tkinter import scrolledtext
class TerminalUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Terminal UI")
        self.root.geometry("480x320")  # Set the resolution to 480x320

        # Create a scrolled text widget with black background and white text
        self.text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=20, font=("Courier", 48), bg="black", fg="white")
        self.text_area.pack(padx=100, pady=10)

        # Disable editing
        self.text_area.config(state=tk.DISABLED)

    def append_text(self, text, prefix=""):
        self.text_area.config(state=tk.NORMAL)
        self.text_area.insert(tk.END, f"{prefix}{text}\n")
        self.text_area.config(state=tk.DISABLED)
        self.text_area.yview(tk.END)  # Auto-scroll to the end

    def clear_text(self):
        self.text_area.config(state=tk.NORMAL)
        self.text_area.delete(1.0, tk.END)
        self.text_area.config(state=tk.DISABLED)
def main():
    root = tk.Tk()
    terminal_ui = TerminalUI(root)

    terminal_ui.append_text("System starting...")

    def run():
        last_was_else = False
        while True:
            if user_interaction_detected():
                #clear the terminal all the past text, all clean
                terminal_ui.clear_text()
                terminal_ui.append_text("Please ask a yes-or-no question, I'm listening...\n")
                control_led("on")  # Turn on LED light when user interaction is detected.
                stop_playback()  # Stop any ongoing playback
                user_input = recognize_speech_from_mic()
                if user_input:
                    terminal_ui.append_text(user_input + "?\n", prefix="User: ")
                    # Stop recognition and process the text with GPT
                    terminal_ui.append_text("Processing user input with GPT...\n")
                    response = ask_chatgpt(user_input)
                    print(response)
                    answer = response['answer'].lower() + ".wav"
                    terminal_ui.append_text("GPT: " + response['answer'] + '\n')
                    try:
                        terminal_ui.append_text("Category: " + response['category_name'] + '\n')
                    except KeyError:
                        # do nothing
                        pass
                    try:
                        categories = {
                            "Personal and Contextual Insight": "Chatbots don’t know your personal details that they’re not told (and don’t understand human experience), don’t rely on it for personal advice.",
                            "Emotions and Relationships": "Chatbots don’t understand emotions or relationships, they don’t have empathy even they pretend they have.",
                            "Personal Opinions and Preferences": "Chatbots might pretend to have personal opinions but they don’t, so take their opinions with a second thought.",
                            "Predicting the Future": "Chatbots can’t accurately predict future events. They stick to known facts.",
                            "Medical or Legal Advice": "Chatbots aren’t suitable for health or legal advice. Consult a professional in these fields.",
                            "Sensory and Perceptual Limitations": "Chatbots work only with text and can’t interpret physical sensations like smells, tastes, and touch.",
                            "Artistic and Literary Interpretation": "Chatbots lack personal insight, so they can’t interpret art or literature with emotional depth.",
                            "General Knowledge and Fact-Checking": "Chatbots excel at general knowledge and fact-checking in areas like history, science, and technology.",
                            "Identity and Personhood": "Chatbots are not human. They don’t have identities, genders, or personalities."
                        }
                        terminal_ui.append_text('Justification: ' + categories[response['category_name']] + '\n')
                        #terminal_ui.append_text('Justification: ' + response['justification'] + '\n')
                    except KeyError:
                        # do nothing
                        pass
                    play_wav_file(answer)
                time.sleep(10)  # Add a small delay to avoid rapid looping
                last_was_else = False
            else:
                terminal_ui.append_text("No user interaction detected.")
                # make the remain part into thread from control led to play wav file
                def else_run():
                    control_led("breathing")  # Revert to breathing light if no user interaction is detected.
                    stop_playback()  # Stop any ongoing playback
                    # Play loop sound to attract attention
                    play_wav_file("intro.wav", loop=True)

                if not last_was_else:
                    threading.Thread(target=else_run, daemon=True).start()
                    last_was_else = True

            play_wav_file("intro.wav", loop=False)
            print("looping")
            time.sleep(10)

    # Run the main loop in a separate thread to keep the GUI responsive
    import threading
    threading.Thread(target=run, daemon=True).start()
    root.mainloop()

if __name__ == "__main__":
    main()
