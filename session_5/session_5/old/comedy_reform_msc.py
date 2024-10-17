import json
import argparse
import re

# Function to transform the input JSON format to the desired output format
def transform_json(input_data):
    output_data = []
    
    for utter_id, content in input_data.items():
        # Combine memory into a single memory_text field
        combined_dialogue = " ".join(content["current_dialogue"])
        memory_text = "\n".join(content['memory'])
        speaker_pattern = r'(Speaker [A-Z]):'
        speakers = re.findall(speaker_pattern, combined_dialogue)
        last_speaker = speakers[-1]
        # Identify last speaker from the response
        raw_prediction = content['response']
        if last_speaker == "Speaker A":
            speaker = "Speaker B"
            raw_prediction = re.sub(r"Speaker [A-Z]:", "", raw_prediction)
        elif last_speaker == "Speaker B":
            speaker = "Speaker A"
            raw_prediction = re.sub(r"Speaker [A-Z]:", "", raw_prediction)
        else:
            speaker = "Unknown"  # Fallback in case no prefix is present
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
    parser.add_argument('output_file', type=str, help='Output JSON file path')
    
    # Parse the arguments
    args = parser.parse_args()

    # Read the input JSON file
    with open(args.input_file, 'r') as infile:
        input_data = json.load(infile)
    
    # Transform the input data
    transformed_data = transform_json(input_data)

    # Write the transformed data to the output JSON file
    with open(args.output_file, 'w') as outfile:
        json.dump(transformed_data, outfile, indent=4)

# Entry point of the script
if __name__ == "__main__":
    main()
