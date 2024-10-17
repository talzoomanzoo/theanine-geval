import json
import argparse

# Function to determine the speaker by analyzing the reference data
def determine_speaker(utter_id, reference_data):
    # Get the speaker information from the reference data
    speaker = "Unknown"
    for ref in reference_data:
        if ref.get("utter_id") == utter_id:
            speaker = ref.get("speaker", "Unknown")
            break
    return speaker

# Function to transform the input JSON into the desired format
def transform_json(input_json, reference_data):
    result = []
    
    for utter_id, data in input_json.items():
        # Extract the part before the first dash, e.g., "e0" from "e0-s5-t1"
        utter_id_prefix = utter_id.split('-')[0]
        
        # Check if the utter_id starts with "e" followed by a number between 0 and 49
        if utter_id_prefix.startswith('e'):
            number_part = int(utter_id_prefix[1:])
            if 0 <= number_part <= 49:
                # Dynamically combine memory items into a single string
                combined_memory = "\n".join([f"{idx + 1}. {item}" for idx, item in enumerate(data["memory"])])
                combined_dialogue = "\n".join(data["current_dialogue"])
                
                # Determine the speaker based on the reference data
                speaker = determine_speaker(utter_id, reference_data)

                # Prepare the transformed dictionary
                transformed_data = {
                    "utter_id": utter_id,
                    "current_dialogue": combined_dialogue, 
                    "memory_text": combined_memory,
                    "speaker": speaker,
                    "raw_prediction": data["response"]
                }
                
                result.append(transformed_data)
    
    return result

# Function to handle input and output files using argparse
def main():
    parser = argparse.ArgumentParser(description="Transform JSON file format")
    parser.add_argument('input_file', type=str, help="Path to the input JSON file")
    parser.add_argument('reference_file', type=str, help="Path to the reference JSON file")
    parser.add_argument('output_file', type=str, help="Path to the output JSON file")
    
    args = parser.parse_args()
    
    # Read the input JSON file
    with open(args.input_file, 'r') as infile:
        input_json = json.load(infile)
    
    # Read the reference JSON file
    with open(args.reference_file, 'r') as reffile:
        reference_data = json.load(reffile)
    
    # Transform the JSON
    transformed_json = transform_json(input_json, reference_data)
    
    # Write the transformed JSON to the output file
    with open(args.output_file, 'w') as outfile:
        json.dump(transformed_json, outfile, indent=4)
    
if __name__ == "__main__":
    main()
