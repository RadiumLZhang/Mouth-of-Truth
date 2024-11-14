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
                "content": "You are a robot that answers each question with yes or no and the reason. Firstly, determine if the question is a boolean question. If it's not, reply with 'None'. If it is a boolean question, reply with yes or no or I don't know (if that's a question Chatbot can not answer), and then reply with exactly the following sentences:\n\
                1. Personal and Contextual Insight: Chatbots don’t know your personal details that they’re not told (and don’t understand human experience), don’t rely on it for personal advice. \n\
                2. Emotions and Relationships: LLMs don’t have personal feelings or opinions, so they can’t answer questions about what someone might like or prefer.\n\
                3. **Predicting the Future:** LLMs can’t predict the future. They only know things that have already happened, so they can’t tell you what will happen later. \n\
                4. **Deep Personal Issues:** LLMs aren’t able to help with very personal problems. These kinds of questions need a deep understanding of emotions, which LLMs don’t have. \n\
                5. **Medical or Legal Advice:** LLMs shouldn’t be used for advice on health or legal issues. You should talk to a doctor or lawyer about these kinds of questions. \n\
                6. **Questions Using Senses:** LLMs can only understand text, not things you can see, hear, or feel. They can’t answer questions that need sensory information like sounds or images. \n\
                7. **Emotions or Relationships:** LLMs don’t understand human emotions or relationships well. They can’t help with questions about feelings or personal connections. \n\
                8. **Art or Literature Interpretation:** LLMs don’t have personal insight, so they can’t really interpret art or literature in a deep, emotional way as people can. \n\
                9. **Speculative or Theoretical Questions:** LLMs can’t answer questions about things that haven’t been proven yet or are just theories. They stick to facts that are known. \n\
                10. **General Knowledge and Fact-Checking:** LLMs are good at answering general knowledge questions and fact-checking when the information is part of their training, particularly in areas like history, science, and technical details."
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
                            "enum": ["yes", "no", "None"]
                        },
                        "category_name": {
                            "type": "string",
                            "description": "The full name of the category the question belongs to.",
                            "enum": [
                                "Personal or Contextual Information",
                                "Personal Opinions",
                                "Predicting the Future",
                                "Deep Personal Issues",
                                "Medical or Legal Advice",
                                "Questions Using Senses",
                                "Emotions or Relationships",
                                "Art or Literature Interpretation",
                                "Speculative or Theoretical Questions",
                                "General Knowledge and Fact-Checking"
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
