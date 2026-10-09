import os

def get_file_content(working_directory: str, file_path: str) -> str:

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
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        # checks if the target is a file
        if os.path.isfile(target_path) is False:
            return f'Error: File not found or is not a regular file: "{file_path}"'

        # open and read file up to 10000 chars
        with open(target_path, "r") as f:
            MAX_CHARS = 10000
            content = f.read(MAX_CHARS)

            # after reading content check 1 more character to see if there is more
            if f.read(1):
                content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'

        return content

    # catches any other errors
    except Exception as e:
        return f"Error: {e}"


        