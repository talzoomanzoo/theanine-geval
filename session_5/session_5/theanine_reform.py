import json
import argparse
import csv

# Function to filter and transform the input JSON format to the desired output format
def filter_and_transform_json(input_data, reference_data, memory_file):
    output_data = []
    
    # Load dialogues and memories from the CSV file
    dialogues_memories = {}
    with open(reference_data, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            dialogues_memories[row['dialogue']] = row['memory']
    
    # Load memory file
    with open(memory_file, 'r') as memfile:
        memory_data = json.load(memfile)
    
    # Create a dictionary for quick lookup of summaries by dataID
    memory_dict = {mem['dataID']: mem['summary'] for mem in memory_data}
    
    for content in input_data:
        # Check if the current dialogue is in the dialogues set
        if content["current_dialogue"] in dialogues_memories:
            # Combine memory into a single memory_text field
            memory_text = "\n".join(content['memory_text'].split('\n'))
            
            # Extract the dataID from utter_id
            data_id = content["utter_id"].split('-')[0]
            
            # Add the filtered and transformed data to the output
            output_entry = {
                "utter_id": content["utter_id"],
                "current_dialogue": content["current_dialogue"],
                "memory_text": memory_text,
                "speaker": content["speaker"],
                "raw_prediction": content["raw_prediction"]
            }
            
            # Add previous summary if dataID matches
            if data_id in memory_dict:
                output_entry["previous_summary"] = memory_dict[data_id]
            
            # Add memory from CSV if dialogue matches
            if content["current_dialogue"] in dialogues_memories:
                output_entry["previous_summary"] = dialogues_memories[content["current_dialogue"]]

            output_data.append(output_entry)
    
    # Ensure output_data maintains the same order as input_data
    output_data_sorted = sorted(output_data, key=lambda x: input_data.index(next(item for item in input_data if item["utter_id"] == x["utter_id"])))
    
    return output_data_sorted

# Main function to parse arguments and process the JSON file
def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Filter and transform a JSON file based on dialogues in a CSV file.")
    parser.add_argument('input_file', type=str, help='Input JSON file path')
    parser.add_argument('reference_file', type=str, help='Reference CSV file path')
    parser.add_argument('memory_file', type=str, help='Memory JSON file path')
    parser.add_argument('output_file', type=str, help='Output JSON file path')
    
    # Parse the arguments
    args = parser.parse_args()

    # Read the input JSON file
    with open(args.input_file, 'r') as infile:
        input_data = json.load(infile)
    
    # Filter and transform the input data
    filtered_transformed_data = filter_and_transform_json(input_data, args.reference_file, args.memory_file)

    # Write the filtered and transformed data to the output JSON file
    with open(args.output_file, 'w') as outfile:
        json.dump(filtered_transformed_data, outfile, indent=4)

# Entry point of the script
if __name__ == "__main__":
    main()
