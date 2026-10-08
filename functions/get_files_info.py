import os

def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        # get absolute path of working directory
        working_dir_abs = os.path.abspath(working_directory)

        # use join and normpath to get true form of the path
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))

        # check if we have valid commonpath for target dir
        # Will be True or False
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs

        if valid_target_dir is False:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        # guardrails for LLM so it doesn't go outside of working directory
        elif not os.path.isdir(directory):
            return f'Error: "{directory}" is not a directory'

        # return success message if the directory is good to use
        else:
            return f'Success: "{directory}" is within the working directory'

    # if any other errors occur catch them here
    except Exception as e:
        print(f"Error: {e}")


get_files_info("calculator")