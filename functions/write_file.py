import os

def write_file(working_directory: str, file_path: str, content: str) -> str:
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
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        # checks if the target is a directory
        if os.path.isdir(target_path) is True:
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        # check to make sure all parent directories of file_path exist
        os.makedirs(os.path.dirname(target_path), exist_ok=True)

        # open the file in write mode and overwrite with content
        with open(target_path, "w") as f:
            f.write(content)
            
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
   
    except Exception as e:
         return f"Error: {e}"


