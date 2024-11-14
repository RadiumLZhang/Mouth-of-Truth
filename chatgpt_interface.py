from dotenv import load_dotenv
import os
from openai import OpenAI
import json

# Read the OpenAI API key from the environment variable
load_dotenv()

# Read the OpenAI API key from the environment variable
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.")

# Initialize the OpenAI client with the API key
client = OpenAI(api_key=api_key)

def ask_chatgpt(user_input):
    """Send a question to ChatGPT and return the response."""

    # Construct the API call to GPT-4 with the appropriate messages, function calling, and response format
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": "You are a robot that answers each question with yes or no and the reason. Firstly, determine if the question is a yes/no question. If it's not, reply with 'None'. If it is a yes/no question, reply with yes/no or idk, and then reply with exactly the following sentences:\n\
                                1. Personal and Contextual Insight: Chatbots don’t know your personal details that they’re not told (and don’t understand human experience), don’t rely on it for personal advice. \n\
                2. Emotions and Relationships: Chatbots don’t understand emotions or relationships, they don’t have empathy even they pretend they have.\n\
                3. Personal Opinions and Preferences: Chatbots might pretend to have personal opinions but they don’t, so take their opinions with a second thought. \n\
                4. Predicting the Future: Chatbots can’t accurately predict future events. They stick to known facts. \n\
                5. Medical or Legal Advice: Chatbots aren’t suitable for health or legal advice. Consult a professional in these fields. \n\
                6. Sensory and Perceptual Limitations: Chatbots work only with text and can’t interpret physical sensations like smells, tastes, and touch. \n\
                7. Artistic and Literary Interpretation: Chatbots lack personal insight, so they can’t interpret art or literature with emotional depth. \n\
                8. General Knowledge and Fact-Checking: Chatbots excel at general knowledge and fact-checking in areas like history, science, and technology.\n\
                9. Identity and Personhood: Chatbots are not human. They don’t have identities, genders, or personalities."
            },
            {
                "role": "user",
                "content": user_input
            }
        ],
        temperature=1,
        max_tokens=2048,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        functions=[
            {
                "name": "answer_categorize_question",
                "description": "Provides a yes/no answer, the category name, and a justification.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "answer": {
                            "type": "string",
                            "enum": ["yes", "no", "None", "idk"]
                        },
                        "category_name": {
                            "type": "string",
                            "description": "The full name of the category the question belongs to.",
                            "enum": [

                                "Personal and Contextual Insight",

                                "Emotions and Relationships",

                                "Personal Opinions and Preferences",

                                "Predicting the Future",

                                "Medical or Legal Advice",

                                "Sensory and Perceptual Limitations",

                                "Artistic and Literary Interpretation",

                                "General Knowledge and Fact-Checking",

                                "Identity and Personhood"

                            ]
                        },
                        "justification": {
                            "type": "string",
                            "description": "A one-sentence justification for why the question belongs to the category."
                        }
                    },
                    "required": ["answer", "category_name", "justification"]
                }
            }
        ],
        function_call="auto"  # Automatically call the function
    )

    print(response)
    # Extract the function call from the response
    try:
        function_call = response.choices[0].message.function_call
        print(function_call)
    except AttributeError:
        return {
            "answer": "None",
            "category_name": "None",
            "justification": "None"
        }
    # Parse the arguments of the function call

    try:
        arguments = function_call.arguments
        print(arguments)
    except AttributeError:
        return {
            "answer": "None",
            "category_name": "None",
            "justification": "None"
        }


    parsed_data = json.loads(arguments)
    # Display the output: Answer, Category Name, and Justification
    answer = parsed_data["answer"]
    category_name = parsed_data["category_name"]
    justification = parsed_data["justification"]

    # Returning the structured response
    return {
        "answer": answer,
        "category_name": category_name,
        "justification": justification
    }

# Example usage
# question = "will trump win 2025 president election?"
# result = ask_chatgpt(question)
# print(result)
