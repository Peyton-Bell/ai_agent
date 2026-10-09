from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content

print("===TEST 1===")
result = get_file_content("calculator", "lorem.txt")
print(f"lorem.txt length: {len(result)}")
print(f"lorem.txt truncated: {'truncated' in result}")

print("===TEST 2===")
print(get_file_content("calculator", "main.py"))

print("===TEST 3===")
print(get_file_content("calculator", "pkg/calculator.py"))

print("===TEST 4===")
print(get_file_content("calculator", "/bin/cat"))

print("===TEST 5===")
print(get_file_content("calculator", "pkg/does_not_exist.py"))