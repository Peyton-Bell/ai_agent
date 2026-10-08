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
        elif not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'


        # Now after it's all validated we can list out the file info here
        file_info_list = []
        for item in os.listdir(target_dir):
            item_path = os.path.join(target_dir, item)
            file_info_list.append(f"- {item}: file_size={os.path.getsize(item_path)} bytes, is_dir={os.path.isdir(item_path)}")
        return "\n".join(file_info_list)

    # if any other errors occur catch them here
    except Exception as e:
        return f"Error: {e}"

