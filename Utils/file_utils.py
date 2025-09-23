import os

# def get_files(target_dirs, exclude_dirs):
#     """
#     Recursively collect source files from target_dirs excluding any in exclude_dirs.
#     """
#     source_files = []
#     exclude_dirs = set(os.path.abspath(d) for d in exclude_dirs)

#     for directory in target_dirs:
#         for root, _, files in os.walk(directory):
#             abs_root = os.path.abspath(root)
#             if any(abs_root.startswith(excluded) for excluded in exclude_dirs):
#                 continue
#             for file in files:
#                 if file.endswith(('.py', '.js', '.json', '.yml', '.yaml', '.env')):
#                     source_files.append(os.path.join(root, file))

#     return source_files


def get_files(directories, exclude_dirs):
    all_files = []
    for directory in directories:
        for root, dirs, files in os.walk(directory):
            # Exclude unwanted directories
            if any(excluded in root for excluded in exclude_dirs):
                continue
            for file in files:
                full_path = os.path.join(root, file)
                all_files.append(full_path)
    return all_files

def is_binary(file_path: str, blocksize: int = 1024) -> bool:
    """
    Determine if a file is binary by reading a small portion of it.

    Args:
        file_path (str): The path to the file to check.
        blocksize (int): Number of bytes to read for detection.

    Returns:
        bool: True if file is binary, False if it's likely text.
    """
    try:
        with open(file_path, 'rb') as file:
            chunk = file.read(blocksize)
            if not chunk:
                return False  # Empty files are not binary
            # If a high percentage of null bytes or non-text chars, treat as binary
            text_characters = bytearray({7, 8, 9, 10, 12, 13, 27} | set(range(0x20, 0x100)))
            non_text = chunk.translate(None, text_characters)
            return float(len(non_text)) / len(chunk) > 0.30
    except Exception as e:
        print(f"[!] Failed to check if file is binary: {file_path}: {e}")
        return True  # Assume binary on error
