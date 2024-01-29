from openai import OpenAI

api_key = "sk-tjdLt6Pu69aLn4BL238d43EeE0884547993cA43b1cEcFa76"
base_url = "https://api.132999.xyz/v1"

client = OpenAI(
    api_key=api_key,
    base_url=base_url
)

class ChatGPTSession:
    def __init__(self, model='gpt-3.5-turbo', max_history=5):
        self.model = model
        self.max_history = max_history
        self.conversation_history = []

    def add_message(self, role, content):
        """
        Add a message to the conversation history and ensure it doesn't exceed the max_history limit.
        
        :param role: 'user' or 'system' indicating who is sending the message.
        :param content: The content of the message.
        """
        self.conversation_history.append({"role": role, "content": content})
        # Limit the history length.
        self.conversation_history = self.conversation_history[-self.max_history:]

    def get_response(self, user_input):
        """
        Get a response from the GPT model based on the user input and past conversation.

        :param user_input: The latest input from the user.
        :return: The GPT model's output as a string.
        """
        # Add the user's message to the conversation history.
        self.add_message('user', user_input)

        # Generate the model's response.
        chat_completion = client.chat.completions.create(
            messages=self.conversation_history,
            model=self.model,
        )

        # Assuming the response is structured correctly.
        model_response = chat_completion.choices[0].message.content

        # Add the model's response to the conversation history.
        self.add_message('system', model_response)

        return model_response

if __name__ == "__main__":
    # Example usage:
    session = ChatGPTSession(max_history=5)
    response = session.get_response("Hello, how are you?")
    print(response)
    # Continue the conversation...
    response = session.get_response("Tell me more about AI.")
    print(response)

