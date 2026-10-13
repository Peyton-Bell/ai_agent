import os
from dotenv import load_dotenv
from openai import OpenAI
import argparse
from prompt import system_prompt
from available_functions import available_function
import json

def main():

    # setup for parser
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User Prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable Verbose Output")
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

    # Response from model
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt}
        ]
    response = client.chat.completions.create(
        model = "openrouter/free",
        messages = messages,
        tools=available_function,
    )


    # print user prompt adn which model is used
    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Model used: {response.model}")

    # print token metadata
    if response.usage is not None:
        if args.verbose:
            print(f"Prompt tokens: {response.usage.prompt_tokens}")
            print(f"Response tokens: {response.usage.completion_tokens}")
    else:
        print("Token usage not available because response.usage = None")

    # print response from model
    message = response.choices[0].message
    if message.tool_calls:
        for tool_call in message.tool_calls:
            function_args = json.loads(tool_call.function.arguments or "{}")
            print(f"Calling function: {tool_call.function.name}({function_args})")
    
    print(message.content)


if __name__ == "__main__":
    main()
