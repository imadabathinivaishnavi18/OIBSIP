import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import random
import time
from collections import deque


class PersonalAssistant:
    def __init__(self):
        # Initialize speech engine and recognizer
        self.engine = pyttsx3.init()
        self.recognizer = sr.Recognizer()

        # Personal settings (session-only, no file)
        self.assistant_name = "Buddy"
        self.user_name = None
        self.favorite_color = None
        self.jokes = [
            "Why did the programmer bring a ladder to work? Because they heard the code was high level.",
            "Why did the computer go to the doctor? Because it had a virus.",
            "Why don’t skeletons fight each other? They don’t have the guts.",
            "Why did the developer go broke? Because he used up all his cache."
        ]

        # Conversation memory (last 5 exchanges)
        self.conversation_history = deque(maxlen=5)

        # Setup speech properties
        self._setup_voice()

    def _setup_voice(self):
        """Configure voice settings for natural speech"""
        self.engine.setProperty("rate", 160)
        voices = self.engine.getProperty("voices")

        # Try to find a natural sounding voice
        for voice in voices:
            if "Zira" in voice.name or "Microsoft Hazel" in voice.name:
                self.engine.setProperty("voice", voice.id)
                break

        # Fallback to second voice if preferred not found
        if len(voices) > 1:
            self.engine.setProperty("voice", voices[1].id)

    def speak(self, text: str):
        """Convert text to speech with natural pacing"""
        if not text:
            return

        print(f"Assistant: {text}")

        phrases = text.split(". ")
        if len(phrases) > 1:
            for phrase in phrases[:-1]:
                self.engine.say(phrase + ". ")
                self.engine.runAndWait()
                time.sleep(0.3)
            self.engine.say(phrases[-1])
        else:
            self.engine.say(text)

        self.engine.runAndWait()
        self.conversation_history.append(("assistant", text))

    def listen(self):
        """
        Listen to user input with error handling.
        If voice input fails, fall back to text input.
        """
        try:
            with sr.Microphone() as source:
                print("Listening...")
                self.recognizer.adjust_for_ambient_noise(source)

                audio = self.recognizer.listen(source, timeout=5)
                user_input = self.recognizer.recognize_google(audio).lower()
                print(f"You (voice): {user_input}")

                self.conversation_history.append(("user", user_input))
                return user_input

        except sr.UnknownValueError:
            self.speak("I didn't catch that. Please type your command.")
        except sr.RequestError:
            self.speak("There seems to be a problem with the speech service. Please type your command.")
        except Exception as e:
            print(f"Speech error: {e}")
            self.speak("There was a problem with the microphone. Please type your command.")

        # Fallback to text input
        text_input = input("Type here: ").strip().lower()
        if text_input:
            print(f"You (text): {text_input}")
            self.conversation_history.append(("user", text_input))
            return text_input
        return None

    def _get_time_greeting(self) -> str:
        """Return time-appropriate greeting"""
        hour = datetime.datetime.now().hour
        if 5 <= hour < 12:
            return "Good morning"
        elif 12 <= hour < 18:
            return "Good afternoon"
        return "Good evening"

    def tell_joke(self):
        """Tell a random joke"""
        joke = random.choice(self.jokes)
        lead_ins = [
            "Here's one for you",
            "Let me think of one",
            "I know a good one",
            "How about this"
        ]
        self.speak(f"{random.choice(lead_ins)}: {joke}")
        time.sleep(1)
        reactions = ["Haha!", "Hehe!", "LOL!", "Funny right?"]
        self.speak(random.choice(reactions))

    def open_google(self):
        """Open google.com in the default browser."""
        self.speak("Opening Google.")
        webbrowser.open("https://www.google.com")

    def web_search(self, query: str | None):
        """Search the web using Google."""
        if not query:
            self.speak("What should I search for?")
            query = self.listen()
        if query:
            self.speak(f"Searching the web for {query}.")
            webbrowser.open(f"https://www.google.com/search?q={query}")

    def personal_chat(self):
        """Engage in personal conversation"""
        if not self.user_name:
            self.speak("First, what's your name?")
            name = self.listen()
            if name:
                self.user_name = name.split()[-1]
                self.speak(f"Nice to meet you, {self.user_name}!")

        if random.random() > 0.7:
            if not self.favorite_color:
                self.speak(f"{self.user_name}, what's your favorite color?")
                color = self.listen()
                if color:
                    self.favorite_color = color.split()[-1]
                    self.speak(f"I'll remember you like {self.favorite_color}!")
            else:
                self.speak("How is your day going?")
                self.listen()

    def handle_command(self, command: str) -> bool:
        """Process user commands"""
        if not command:
            return False

        command = command.lower()

        # Greetings
        if any(word in command for word in ["hello", "hi", "hey"]):
            greeting = self._get_time_greeting()
            if self.user_name:
                self.speak(f"{greeting} {self.user_name}! How are you today?")
            else:
                self.speak(f"{greeting}! What's your name?")
            return True

        # Time
        elif "time" in command:
            current_time = datetime.datetime.now().strftime("%I:%M %p")
            responses = [
                f"It's {current_time} right now.",
                f"The time is {current_time}.",
                f"My clock shows {current_time}."
            ]
            self.speak(random.choice(responses))
            return True

        # Date
        elif "date" in command or "day" in command:
            current_date = datetime.datetime.now().strftime("%A, %B %d, %Y")
            self.speak(f"Today is {current_date}.")
            return True

        # Open Google homepage
        elif "open google" in command or command.strip() == "google":
            self.open_google()
            return True

        # Web search
        elif "search" in command or "look up" in command:
            query = (
                command.replace("search", "")
                .replace("look up", "")
                .replace("for", "")
                .strip()
            )
            self.web_search(query)
            return True

        # Jokes
        elif "joke" in command:
            self.tell_joke()
            return True

        # Personal questions
        elif "your name" in command:
            self.speak(f"My name is {self.assistant_name}.")
            return True

        # Exit
        elif any(word in command for word in ["exit", "quit", "bye", "goodbye"]):
            farewells = [
                "Goodbye! Have a great day!",
                "See you later!",
                "Farewell for now!",
                "Until next time!"
            ]
            self.speak(random.choice(farewells))
            if self.user_name:
                self.speak(f"Take care, {self.user_name}!")
            raise SystemExit

        # Fallback
        else:
            self.speak(
                "I can greet you, tell the time or date, open Google, search the web, "
                "tell you a joke, or just chat with you."
            )
            return True


def main():
    assistant = PersonalAssistant()

    initial_greeting = assistant._get_time_greeting()
    assistant.speak(
        f"{initial_greeting}! I'm {assistant.assistant_name}, your personal assistant."
    )

    if not assistant.user_name:
        assistant.speak("What's your name?")
        name = assistant.listen()
        if name:
            assistant.user_name = name.split()[-1]

    if assistant.user_name:
        assistant.speak(f"Welcome back {assistant.user_name}!")
    else:
        assistant.speak("Let me know if you need anything!")

    while True:
        command = assistant.listen()

        if not assistant.handle_command(command):
            assistant.personal_chat()

        time.sleep(random.uniform(0.5, 1.5))


if __name__ == "__main__":
    main()
