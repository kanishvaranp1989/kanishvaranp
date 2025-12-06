import json

def print_tree(data, indent="", is_last=False, key_name=None):
    """Recursively prints the JSON structure in a tree format."""
    
    # Determine the prefix for the current item
    prefix = indent
    if is_last:
        prefix += "└─ "
        next_indent = indent + "   "
    else:
        prefix += "├─ "
        next_indent = indent + "│  "

    # Format the key and value for printing
    if key_name is not None:
        if isinstance(data, dict):
            label = f'"{key_name}" (object)'
        elif isinstance(data, list):
            label = f'"{key_name}" (array)'
        else:
            label = f'"{key_name}": {json.dumps(data)} ({type(data).__name__})'
    else:
        if isinstance(data, dict):
            label = "(object)"
        elif isinstance(data, list):
            label = "(array)"
        else:
            label = f"{json.dumps(data)} ({type(data).__name__})"

    print(f"{prefix}{label}")

    # Recurse for nested objects or arrays
    if isinstance(data, dict):
        keys = list(data.keys())
        for i, key in enumerate(keys):
            print_tree(data[key], next_indent, i == len(keys) - 1, key)
    elif isinstance(data, list):
        for i, item in enumerate(data):
            print_tree(item, next_indent, i == len(data) - 1, None)

def print_json_tree_from_file_custom(filename):
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
        print_tree(data, key_name="ROOT")
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from the file '{filename}'.")

# Example usage:
print_json_tree_from_file_custom('filename')
