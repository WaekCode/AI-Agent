import os
from dotenv import load_dotenv
from google import genai
import sys
from google.genai import types
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.run_python import run_python_file
from functions.write_file import write_file


# Load variables from .env file
load_dotenv()

# Read the API key from environment variables
api_key = os.getenv("GEMINI_API_KEY")

if api_key:
    print("API key loaded successfully!")
else:
    print("API key not found. Please check your .env file.")


client = genai.Client(api_key=api_key)


user = sys.argv[1] if len(sys.argv) > 1 else None
if not user:
    print("Error: Please provide a prompt as a command line argument.")
    print('Usage: python3 main.py "Your prompt here"')
    exit(1)  # Exit with code 1 as instructed



messages = [
    types.Content(role="user", parts=[types.Part(text=user)]),
]

system_prompt = '''"""
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
""""'''


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

####################################################################
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to write to, relative to the working directory.",
            ),

            'content': types.Schema(
                type=types.Type.STRING,
                description='the content to write in to the file'
            ),
        },
    ),
)

####################################################################
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file located in the specified directory and returns the standard output or error.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the Python file to execute, relative to the working directory.",
            ),
        },
    ),
)

####################################################################
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads and returns the full content of a specified file within the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to read, relative to the working directory.",
            ),
        },
    ),
)

####################################################################

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file
    ]
)


def call_function(function_call_part, verbose=False):
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")

    function_mapping = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "write_file": write_file,
        "run_python_file": run_python_file
    }

    function_name = function_call_part.name
    args = dict(function_call_part.args)
    args["working_directory"] = "./calculator"

    if function_name in function_mapping:
        the_function = function_mapping[function_name]
        function_result = the_function(**args)
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"result": function_result},
                )
            ],
        )
    else:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )


def main():
    verbose = '--verbose' in sys.argv
    MAX_ITERS = 20
    iters = 0

    while iters < MAX_ITERS:
        iters += 1

        response = client.models.generate_content(
            model='gemini-2.0-flash-001',
            contents=messages,
            config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt),
        )

        if verbose:
            print(f"\nIteration {iters}:")
            print("Prompt tokens:", response.usage_metadata.prompt_token_count)
            print("Response tokens:", response.usage_metadata.candidates_token_count)

        # Add all candidates' content to messages
        if response.candidates:
            for candidate in response.candidates:
                messages.append(candidate.content)

        # If no function calls, print final text and break
        if not response.function_calls:
            print("\nFinal LLM Response:")
            print(response.text)
            break

        # Call all functions requested and append their results
        function_responses = []
        for function_call_part in response.function_calls:
            function_call_result = call_function(function_call_part, verbose)
            if (not function_call_result.parts or
                not hasattr(function_call_result.parts[0], "function_response")):
                raise Exception("Function call did not return a valid function_response.")
            if verbose:
                print(f"-> Function response: {function_call_result.parts[0].function_response.response}")
            function_responses.append(function_call_result.parts[0])

        if not function_responses:
            raise Exception("No function responses generated, exiting.")

        messages.append(types.Content(role="tool", parts=function_responses))

    else:
        print(f"Maximum iterations ({MAX_ITERS}) reached without completion.")


if __name__ == "__main__":
    main()
