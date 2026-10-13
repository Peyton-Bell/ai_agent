import os
from dotenv import load_dotenv
from openai import OpenAI
import argparse
from prompt import system_prompt
from available_functions import available_function
from functions.call_functions import call_function
import sys

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

    # print user prompt if verbose
    if args.verbose:
        print(f"User prompt: {args.user_prompt}")

    # loop everything so the LLM can figure things out itself
    for _ in range(20):

        # generate response
        response = client.chat.completions.create(
            model = "openrouter/free",
            messages = messages,
            tools=available_function,
        )


        # print which model is used if verbose
        if args.verbose:
            print(f"Model used: {response.model}")

        # print token metadata if verbose
        if response.usage is not None:
            if args.verbose:
                print(f"Prompt tokens: {response.usage.prompt_tokens}")
                print(f"Response tokens: {response.usage.completion_tokens}")
        else:
            print("Token usage not available because response.usage = None")

        
        # Save conversation history so LLM is aware of everything
        message = response.choices[0].message
        messages.append(message)

        # print response from model
        if message.tool_calls:
            for tool_call in message.tool_calls:

                # call the function
                result_message = call_function(tool_call, args.verbose)

                # raise exception if content is empty
                if not result_message["content"]:
                    raise Exception("Content is empty")

                # in verbose mode print the verbose output
                if args.verbose:
                    print(f"-> {result_message['content']}")

                # save tool message in messages list so it has context on every tool call it does
                messages.append(result_message)
    
        else:
            print(message.content)
            break
    # prints if it goes all 20 completions without a final result
    else:
        print("Error: reached the maximum number of iterations without reaching a final result")
        sys.exit(1)


if __name__ == "__main__":
    main()
