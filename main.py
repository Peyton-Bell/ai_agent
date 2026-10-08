import os
from dotenv import load_dotenv
from openai import OpenAI
import argparse

def main():

    # setup for parser
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User Prompt")
    args = parser.parse_args()

    # setup api key for openrouter
    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if api_key is None:
        raise RuntimeError("Couldn't find API key")


    # Creating OpenAI client
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    # Hardcoding response
    response = client.chat.completions.create(
        model = "openrouter/free",
        messages = [
            {
                "role": "user",
                "content": args.user_prompt,
            }
        ]
    )

    # print token metadata
    if response.usage is not None:
        print(f"Prompt tokens: {response.usage.prompt_tokens}")
        print(f"Response tokens: {response.usage.completion_tokens}")
    else:
        print("Token usage not available because response.usage = None")

    # print response from model
    print(f"Response: {response.choices[0].message.content}")


if __name__ == "__main__":
    main()
