import os
import re

from dotenv import load_dotenv
from google import genai

from utils.config import SYSTEM_PROMPT

load_dotenv()


class TechSupportChat:
    def __init__(self, api_key=None, max_history=15):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "GEMINI_API_KEY not found in environment variables."
            )

        self.client = genai.Client(api_key=self.api_key)
        self.model = "gemini-2.5-flash"
        self.conversation_history = []
        self.max_history = max_history
        self.troubleshooting_state = self._initial_troubleshooting_state()

    @staticmethod
    def _initial_troubleshooting_state():
        return {
            "user_os": None,
            "user_device": None,
            "issue_type": None,
            "attempted_solutions": [],
            "user_tech_level": "unknown",
            "system_info": {},
            "current_step": None,
            "escalation_needed": False,
        }

    def add_to_history(self, role, content, metadata=None):
        message = {
            "role": role,
            "content": content,
            "metadata": metadata if metadata is not None else {},
        }
        self.conversation_history.append(message)

        if len(self.conversation_history) > self.max_history:
            system_messages = [
                item for item in self.conversation_history
                if item["role"] == "system"
            ]
            non_system_messages = [
                item for item in self.conversation_history
                if item["role"] != "system"
            ]
            remaining_limit = max(0, self.max_history - len(system_messages))
            self.conversation_history = system_messages + non_system_messages[
                -remaining_limit:
            ] if remaining_limit else system_messages

    def update_troubleshooting_state(self, key, value):
        if key not in self.troubleshooting_state:
            return

        if key == "attempted_solutions" and isinstance(value, str):
            if value not in self.troubleshooting_state[key]:
                self.troubleshooting_state[key].append(value)
        else:
            self.troubleshooting_state[key] = value

    def get_conversation_context(self):
        context_parts = [SYSTEM_PROMPT]
        state = self.troubleshooting_state
        troubleshooting_details = []

        if state["user_os"]:
            troubleshooting_details.append(f"User OS: {state['user_os']}")
        if state["user_device"]:
            troubleshooting_details.append(f"Device: {state['user_device']}")
        if state["issue_type"]:
            troubleshooting_details.append(f"Issue Type: {state['issue_type']}")
        if state["attempted_solutions"]:
            solutions = ", ".join(state["attempted_solutions"])
            troubleshooting_details.append(f"Attempted Solutions: {solutions}")
        if state["user_tech_level"] != "unknown":
            troubleshooting_details.append(
                f"User Tech Level: {state['user_tech_level']}"
            )
        recent_changes = state["system_info"].get("recent_changes")
        if recent_changes:
            troubleshooting_details.append(f"Recent Changes: {recent_changes}")
        if state["current_step"]:
            troubleshooting_details.append(f"Current Step: {state['current_step']}")
        if state["escalation_needed"]:
            troubleshooting_details.append("Human Escalation: recommended")

        if troubleshooting_details:
            context_parts.append(
                "TROUBLESHOOTING CONTEXT: "
                + "; ".join(troubleshooting_details)
            )

        for message in self.conversation_history:
            if message["role"] == "system":
                continue
            label = "User" if message["role"] == "user" else "Support"
            context_parts.append(f"{label}: {message['content']}")

        return "\n\n".join(context_parts)

    def analyze_user_input(self, user_input):
        text = user_input.lower()

        if re.search(r"\bwindows\b", text):
            self.update_troubleshooting_state("user_os", "Windows")
        elif re.search(r"\bmac(?:os)?\b", text):
            self.update_troubleshooting_state("user_os", "macOS")
        elif re.search(r"\blinux\b", text):
            self.update_troubleshooting_state("user_os", "Linux")
        elif re.search(r"\bios\b|\biphone\b", text):
            self.update_troubleshooting_state("user_os", "iOS")
        elif re.search(r"\bandroid\b", text):
            self.update_troubleshooting_state("user_os", "Android")

        if "laptop" in text:
            self.update_troubleshooting_state("user_device", "Laptop")
        elif re.search(r"\bdesktop\b|\bpc\b", text):
            self.update_troubleshooting_state("user_device", "Desktop")
        elif re.search(r"\bphone\b|\biphone\b", text):
            self.update_troubleshooting_state("user_device", "Phone")
        elif re.search(r"\btablet\b|\bipad\b", text):
            self.update_troubleshooting_state("user_device", "Tablet")

        issue_types = (
            (("crash", "crashes", "crashing", "freeze", "freezing"), "Software Crash"),
            (("wifi", "wi-fi", "internet", "connection", "network", "bluetooth"), "Connectivity"),
            (("login", "password", "account", "sign in", "sign-in", "two-factor", "2fa"), "Authentication"),
            (("slow", "performance", "lag", "sluggish"), "Performance"),
            (("cracked", "broken screen", "physical damage", "will not turn on", "won't turn on"), "Hardware"),
            (("setting", "configuration", "driver", "update"), "Configuration"),
        )
        for terms, issue_type in issue_types:
            if any(term in text for term in terms):
                self.update_troubleshooting_state("issue_type", issue_type)
                break

        detected_solutions = []
        if "restart" in text or "reboot" in text:
            detected_solutions.append("System restart")
        if "driver" in text and "update" in text:
            detected_solutions.append("Driver update")
        if "reinstall" in text:
            detected_solutions.append("Software reinstall")

        for solution in detected_solutions:
            self.update_troubleshooting_state("attempted_solutions", solution)
        if not detected_solutions and any(
            term in text for term in ("tried", "already", "attempted", "tested")
        ):
            self.update_troubleshooting_state(
                "attempted_solutions", f"User-reported: {user_input.strip()}"
            )

        if any(term in text for term in ("beginner", "not technical", "new to computers")):
            self.update_troubleshooting_state("user_tech_level", "beginner")
        elif any(term in text for term in ("advanced user", "I am technical", "command line")):
            self.update_troubleshooting_state("user_tech_level", "advanced")

        if any(term in text for term in (
            "cracked",
            "broken screen",
            "physical damage",
            "does not turn on",
            "doesn't turn on",
            "not powering on",
            "no power",
        )):
            self.update_troubleshooting_state("escalation_needed", True)

        if any(term in text for term in (
            "account locked",
            "can't access my account",
            "cannot access my account",
            "administrator permission",
            "admin privileges",
            "security breach",
            "unauthorized access",
            "compromised",
            "malware",
            "phishing",
            "hacked",
        )):
            self.update_troubleshooting_state("escalation_needed", True)
        if "locked" in text and any(
            term in text for term in ("account", "sign in", "login")
        ):
            self.update_troubleshooting_state("escalation_needed", True)
        if any(term in text for term in (
            "urgent",
            "time-sensitive",
            "frustrated",
            "fed up",
            "angry",
        )):
            self.update_troubleshooting_state("escalation_needed", True)

        recent_change_markers = (
            "after installing",
            "after updating",
            "after i changed",
            "after changing",
            "recently changed",
        )
        if any(marker in text for marker in recent_change_markers):
            self.troubleshooting_state["system_info"]["recent_changes"] = user_input

    def chat(self, user_input):
        try:
            self.analyze_user_input(user_input)
            conversation_context = self.get_conversation_context()
            self.add_to_history("user", user_input)
            full_prompt = (
                f"{conversation_context}\n\nUser: {user_input}\n\nSupport:"
            )
            response = self.client.models.generate_content(
                model=self.model,
                contents=full_prompt,
            )
            response_text = getattr(response, "text", None)
            if not response_text or not response_text.strip():
                return "I didn't receive a valid response. Please try again."

            response_text = response_text.strip()
            self.add_to_history("assistant", response_text)
            return response_text
        except Exception as error:
            return f"Sorry, I encountered an error: {error}"

    def reset_conversation(self):
        self.conversation_history.clear()
        self.troubleshooting_state = self._initial_troubleshooting_state()

    def get_troubleshooting_summary(self):
        state = self.troubleshooting_state
        summary_parts = []

        if state["issue_type"]:
            summary_parts.append(f"Issue: {state['issue_type']}")

        system_parts = [
            value for value in (state["user_os"], state["user_device"]) if value
        ]
        if system_parts:
            summary_parts.append(f"System: {' '.join(system_parts)}")

        if state["attempted_solutions"]:
            summary_parts.append(
                f"Attempted: {', '.join(state['attempted_solutions'])}"
            )

        if not summary_parts:
            return "No troubleshooting information gathered yet."
        return " | ".join(summary_parts)


def answer_support_query(query, assistant=None):
    try:
        if assistant is None:
            assistant = TechSupportChat()
        return assistant.chat(query)
    except Exception as error:
        return f"Sorry, I encountered an error: {error}"


def interactive_mode():
    """Interactive technical support mode."""
    print("Technical Support Assistant - Interactive Mode")
    print("Type 'quit' to exit, 'reset' to start new conversation, 'summary' for troubleshooting summary")
    print("=" * 70)

    assistant = TechSupportChat()

    while True:
        user_input = input("\nYou: ").strip()

        if user_input.lower() in ["quit", "exit", "bye"]:
            print("Thank you for using technical support. Have a great day!")
            break

        if user_input.lower() == "reset":
            assistant.reset_conversation()
            print("Conversation reset. Starting fresh troubleshooting session!")
            continue

        if user_input.lower() == "summary":
            summary = assistant.get_troubleshooting_summary()
            print(f"\nTroubleshooting Summary: {summary}")
            continue

        if not user_input:
            continue

        response = assistant.chat(user_input)
        print(f"\nSupport: {response}")


def main():
    """Run an interactive technical support session."""
    interactive_mode()


if __name__ == "__main__":
    main()
