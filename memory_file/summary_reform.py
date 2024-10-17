import json
import argparse

def transform_json(input_data):
    transformed_data = []
    
    # Loop through the first 50 rows
    for i, row in enumerate(input_data[:50]):
        summary = row.get("summary", {})
        
        # Concatenate values where the key starts with s1, s2, s3, and s4
        concatenated_summary = "\n".join(
            value for key, value in summary.items() if key.startswith(("s1", "s2", "s3", "s4"))
        )
        
        # Create a new entry with modified dataID and the concatenated summary
        new_entry = {
            "dataID": f"e{i}",  # Assign dataID from ep0 to ep49
            "summary": concatenated_summary
        }
        
        # Append the transformed entry to the new list
        transformed_data.append(new_entry)
    
    return transformed_data

def main():
    # Argument parser to get the input file and output file
    parser = argparse.ArgumentParser(description="Transform JSON data.")
    parser.add_argument("input_file", type=str, help="Path to the input JSON file")
    parser.add_argument("output_file", type=str, help="Path to save the transformed JSON file")
    
    # Parse the arguments
    args = parser.parse_args()
    
    # Read the input JSON file
    with open(args.input_file, 'r') as infile:
        input_data = json.load(infile)
    
    # Transform the data
    transformed_data = transform_json(input_data)
    
    # Write the transformed data to the output file
    with open(args.output_file, 'w') as outfile:
        json.dump(transformed_data, outfile, indent=4)

if __name__ == "__main__":
    main()
