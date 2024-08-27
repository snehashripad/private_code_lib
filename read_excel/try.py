import json


def load_json(filepath):
    """Load JSON data from a file."""
    with open(filepath, "r", encoding="utf-8") as file:
        return json.load(file)


def process_source_data(source_data):
    """Create a mapping from node value to its associated data."""
    node_to_data = {}
    for entry in source_data.get('children', []):
        node = entry.get('id')
        if node:
            node_to_data[node] = entry
    return node_to_data


def update_target_data(target_data, node_to_data):
    """Update target data based on node to data mapping."""
    for entry in target_data:
        village_name = entry.get('Village')
        if village_name in node_to_data:
            # Replace the Village key with the corresponding node data
            node_data = node_to_data[village_name]
            entry.update({
                'Village': node_data.get('village_name', ''),
                'booth_address': node_data.get('booth_address', ''),
                'booth_info': node_data.get('booth_info', ''),
                'booth_map': node_data.get('booth_map', '')
            })
    return target_data


def write_json(obj, filepath):
    """Write JSON data to a file."""
    try:
        with open(filepath, "w", encoding="utf-8") as file:
            json.dump(obj, file, indent=4, ensure_ascii=False)
        print(f"Successfully wrote JSON to {filepath}")
    except Exception as e:
        print(f"Error writing JSON to {filepath}: {e}")


if __name__ == '__main__':
    source_filepath = r"C:\path\to\source.json"
    target_filepath = r"D:\path\to\target.json"

    # Load JSON data from files
    source_data = load_json(source_filepath)
    target_data = load_json(target_filepath)

    # Process the source data to create a mapping
    node_to_data = process_source_data(source_data)

    # Update the target data based on the node to data mapping
    updated_data = update_target_data(target_data, node_to_data)

    # Write the updated target data back to the target file
    write_json(updated_data, target_filepath)
