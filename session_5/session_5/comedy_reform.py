import json
import argparse
import re

# Function to transform the input JSON format to the desired output format
def transform_json(input_data, reference_data):
    output_data = []
    
    for utter_id, content in input_data.items():
        # Combine memory into a single memory_text field
        combined_dialogue = "\n".join(content["current_dialogue"])
        memory_text = "\n".join(content['memory'])
        
        # Get the speaker information from the reference data
        speaker = "Unknown"
        for ref in reference_data:
            if ref.get("utter_id") == utter_id:
                speaker = ref.get("speaker", "Unknown")
                break

        # Clean the raw_prediction
        if ":" in content['response']:
            raw_prediction = content['response'].split(":")[-1]
        else:
            raw_prediction = content['response']

        # Add the transformed data to the output
        output_data.append({
            "utter_id": utter_id,
            "current_dialogue": combined_dialogue,
            "memory_text": memory_text,
            "speaker": speaker,
            "raw_prediction": raw_prediction
        })
    
    return output_data

# Main function to parse arguments and process the JSON file
def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Transform a JSON file from one format to another.")
    parser.add_argument('input_file', type=str, help='Input JSON file path')
    parser.add_argument('reference_file', type=str, help='Reference JSON file path')
    parser.add_argument('output_file', type=str, help='Output JSON file path')
    
    # Parse the arguments
    args = parser.parse_args()

    # Read the input JSON file
    with open(args.input_file, 'r') as infile:
        input_data = json.load(infile)
    
    # Read the reference JSON file
    with open(args.reference_file, 'r') as reffile:
        reference_data = json.load(reffile)

    # Transform the input data
    transformed_data = transform_json(input_data, reference_data)

    # Write the transformed data to the output JSON file
    with open(args.output_file, 'w') as outfile:
        json.dump(transformed_data, outfile, indent=4)

# Entry point of the script
if __name__ == "__main__":
    main()
