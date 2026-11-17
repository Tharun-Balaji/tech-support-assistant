import os
from dotenv import load_dotenv
from google import genai
# TODO: Import SYSTEM_PROMPT from utils.config

# TODO: Load environment variables

class TechSupportChat:
    
    def __init__(self, api_key=None, max_history=15):
        # TODO: Initialize API key from parameter or env var GEMINI_API_KEY
        self.api_key = None

        # TODO: Raise ValueError if no key found with message: "GEMINI_API_KEY not found in environment variables."
        
        # TODO: Initialize Gemini client
        self.client = None

        # TODO: Set the model to "gemini-2.5-flash"
        self.model = None

        # TODO: Initialize conversation history storage as a list
        self.conversation_history = None

        # TODO: Set max_history limit for conversation history
        self.max_history = None

        # TODO: Initialize troubleshooting_state with the following keys and values:
                #
                # user_os              → None
                # user_device          → None
                # issue_type           → None
                # attempted_solutions  → []
                # user_tech_level      → "unknown"
                # system_info          → {}
                # current_step         → None
                # escalation_needed    → False
        self.troubleshooting_state = None
    
    def add_to_history(self, role, content, metadata=None):
        # TODO: Add message to conversation history with optional metadata using the keys:
                # 'role', 'content', 'metadata' (if not given set to empty dictionary)
        # TODO: If conversation history exceeds max_history, preserve all system messages,
                # keep only the most recent non-system messages within the remaining limit,
                # and update conversation_history with the system messages followed by recent messages.
        pass
    
    def update_troubleshooting_state(self, key, value):
        # TODO: Check whether the provided key exists in troubleshooting_state.

        # TODO: If the key is "attempted_solutions" and the value is a string,
        # add it only when it is not already present.

        # TODO: For all other valid keys, update the troubleshooting state
        # with the provided value.
        pass
    
    def get_conversation_context(self):
        # TODO: Start the conversation context with the system prompt.

        # TODO: Check whether the troubleshooting state contains any available information.

        # TODO: Add the available troubleshooting details to the context using these labels:
                # "User OS: <user_os>", "Device: <user_device>",
                # "Issue Type: <issue_type>", "Attempted Solutions: <solutions>",
                # and "User Tech Level: <user_tech_level>".

        # TODO: Format the troubleshooting information under the
        # "TROUBLESHOOTING CONTEXT: " section and joining the information with the ";" operator.

        # TODO: Iterate through the conversation history and extract each message's role and content.

        # TODO: Format user messages with the "User:" label and assistant messages
        # with the "Support:" label.

        # TODO: Combine all context parts into a single string separated by blank lines.
        pass

    def analyze_user_input(self, user_input):
        # TODO: Convert the user input to lowercase for case-insensitive matching.

        # TODO: Detect the user's operating system:
        # - "windows" → set user_os to "Windows"
        # - "mac" or "macos" → set user_os to "macOS"
        # - "linux" → set user_os to "Linux"

        # TODO: Detect the user's device type:
        # - "laptop" → set user_device to "Laptop"
        # - "desktop" → set user_device to "Desktop"
        # - "phone" → set user_device to "Phone"

        # TODO: Detect the issue type:
        # - "crash", "crashes", "crashing", "freeze", or "freezing" → "Software Crash"
        # - "wifi", "internet", "connection", or "network" → "Connectivity"
        # - "login", "password", "account", or "sign in" → "Authentication"
        # - "slow", "performance", "lag", or "sluggish" → "Performance"

        # TODO: Detect attempted solutions:
        # - "restart" or "reboot" → add "System restart"
        # - "update" together with "driver" → add "Driver update"
        # - "reinstall" → add "Software reinstall"
        pass
    
    def chat(self, user_input):
        # TODO: Analyze the user's input to update the troubleshooting state using the analyze_user_input() function.

        # TODO: Add the current user input to conversation history with role "user" using the add_to_history() function.

        # TODO: Get the complete conversation context including the system prompt,
        # troubleshooting context, and previous conversation messages using the get_conversation_context() function.

        # TODO: Create the full prompt in this format:
        # "<conversation_context>\n\nUser: <user_input>\n\nSupport:"

        # TODO: Call the Gemini API using self.client.models.generate_content()
        # with self.model as the model and the full prompt as the contents.

        # TODO: If the API response text is None or empty/blank,
        # return "I didn't receive a valid response. Please try again."

        # TODO: Remove leading/trailing whitespace from the API response.

        # TODO: Add the assistant's response to conversation history
        # with role "assistant".

        # TODO: Return the generated response.

        # TODO: Handle exceptions and return the error in this format:
        # "Sorry, I encountered an error: <error_message>"
        pass
    
    def reset_conversation(self):
        # TODO: Clear conversation history
        # TODO: Reset troubleshooting state
        pass
    
    def get_troubleshooting_summary(self):
        # TODO: Check whether any troubleshooting information has been gathered.
        # If no information is available, return:
        # "No troubleshooting information gathered yet."

        # TODO: Create a list to store the summary information.

        # TODO: If an issue type is available, add it in this format:
        # "Issue: <issue_type>"

        # TODO: If the user's OS or device is available, add the available
        # system information in this format:
        # "System: <user_os> <user_device>"

        # TODO: If attempted solutions are available, add them in this format:
        # "Attempted: <solution1>, <solution2>, ..."

        # TODO: Combine the summary parts using " | " as the separator.

        # TODO: If no summary information is available, return:
        # "No troubleshooting information available."
        pass

def answer_support_query(query, assistant=None):
    # TODO: Create TechSupportChat instance if not provided
    # TODO: Call TechSupportChat.chat function with user query
    # TODO: Handle exceptions and return error message: "Sorry, I encountered an error: {error_message}"
    pass


def interactive_mode():
    """Interactive technical support mode"""
    print("Technical Support Assistant - Interactive Mode")
    print("Type 'quit' to exit, 'reset' to start new conversation, 'summary' for troubleshooting summary")
    print("=" * 70)
    
    assistant = TechSupportChat()
    
    while True:
        user_input = input("\nYou: ").strip()
        
        if user_input.lower() in ['quit', 'exit', 'bye']:
            print("Thank you for using technical support. Have a great day!")
            break
        
        if user_input.lower() == 'reset':
            assistant.reset_conversation()
            print("Conversation reset. Starting fresh troubleshooting session!")
            continue
        
        if user_input.lower() == 'summary':
            summary = assistant.get_troubleshooting_summary()
            print(f"\nTroubleshooting Summary: {summary}")
            continue
        
        if not user_input:
            continue
        
        response = assistant.chat(user_input)
        print(f"\nSupport: {response}")


def main():
    """Main function to demonstrate the technical support assistant."""
    print("Technical Support Assistant - Multi-Turn Chat")
    print("Type 'quit' to exit, 'reset' to start new conversation, 'summary' for troubleshooting summary")
    print("=" * 70)
    
    sample_conversations = [
        [
            "My browser keeps crashing every time I try to open it.",
            "I'm using Chrome on Windows 11.",
            "I restarted already, and it crashes right when I click the Chrome icon.",
            "Yes, it opens fine in safe mode."
        ],
        [
            "My WiFi keeps disconnecting randomly throughout the day.",
            "It's happening on my laptop, but my phone stays connected fine.",
            "It's a Dell Inspiron from 2021, and it seems to happen mostly when I'm on video calls.",
            "I updated the driver but the issue is still happening."
        ]
    ]
    
    # Demonstrate conversation examples
    assistant = None  # TODO: Initialize assistant
    
    for i, conversation in enumerate(sample_conversations):
        print(f"\n--- Sample Troubleshooting Session {i+1} ---")
        for query in conversation:
            print(f"\nUser: {query}")
            response = answer_support_query(query, assistant)
            print(f"Support: {response}")
        
        if assistant:
            summary = assistant.get_troubleshooting_summary()
            print(f"\nTroubleshooting Summary: {summary}")
            assistant.reset_conversation()

if __name__ == "__main__":
    main()
