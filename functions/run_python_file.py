import os
import subprocess

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
    # check to make sure file path is in working_directory

        # turns working directory into full path
        working_dir_abs = os.path.abspath(working_directory)

        # build full path to target and collapses and .. segments
        target_path = os.path.normpath(os.path.join(working_dir_abs, file_path))

        # returns shared parent of target and working_dir_abs. If it's working_dir_abs then we are good to go
        is_inside = os.path.commonpath([working_dir_abs, target_path]) == working_dir_abs

        # check for if it's outside of working dict
        if is_inside is False:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        # checks if the target is a file
        if os.path.isfile(target_path) is False:
            return f'Error: "{file_path}" does not exist or is not a regular file'

        # checks to make sure file is a python file
        if not target_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        # use subprocess to run the file
        command = ["python", target_path]

        # if additional args were provided extend them into the list
        if args:
            command.extend(args)

        # subprocess call
        result = subprocess.run(
            command,
            cwd=working_dir_abs,
            capture_output=True,
            text=True,
            timeout=30,
        )

        # output string
        output_string = []

        #return code != 0
        if result.returncode != 0:
            output_string.append(f"Process exited with code {result.returncode}")

        # no output
        if not result.stdout and not result.stderr:
            output_string.append("No output produced")

        if result.stdout:
            output_string.append(f"STDOUT: {result.stdout}")

        if result.stderr:
            output_string.append(f"STDERR: {result.stderr}")

        return "\n".join(output_string)

        
    except Exception as e:
        return f"Error: executing Python file: {e}"