import json
import argparse
import re

def transform_json(input_data):
    transformed_data = []
    
    for utter_id, details in input_data.items():
        # Retrieve memory list and combine it into memory_text
        if "retrieved_memory_list" in details:
            memory_text = "\n".join([f"{i+1}. {text}" for i, text in enumerate(details["retrieved_memory_list"])])
        else:
            memory_text = ""

        # Handle response to determine speaker and raw_prediction
        response_text = details.get("response", "")
        raw_prediction = response_text
        combined_dialogue = " ".join(details["current_dialogue"])
        
        speaker_pattern = r'(Speaker [A-Z]):'
        speakers = re.findall(speaker_pattern, combined_dialogue)
        last_speaker = speakers[-1]
        
        if last_speaker== "Speaker A":
            speaker = "Speaker B"
            raw_prediction = re.sub(r"Speaker [A-Z]:", "", raw_prediction)
        elif last_speaker== "Speaker B":
            speaker = "Speaker A"
            raw_prediction = re.sub(r"Speaker [A-Z]:", "", raw_prediction)
        else:
            speaker = "Unknown"
        
        # Create the transformed entry
        transformed_data.append({
            "utter_id": utter_id,
            "current_dialogue": combined_dialogue,  # Assuming it's a list
            "memory_text": memory_text,
            "speaker": speaker,
            "raw_prediction": raw_prediction
        })
    
    return transformed_data

def main():
    # Argument parser setup
    parser = argparse.ArgumentParser(description="Transform JSON data format.")
    parser.add_argument("input_json", help="Path to the input JSON file.")
    parser.add_argument("output_json", help="Path to the output JSON file.")

    args = parser.parse_args()

    # Read input JSON
    with open(args.input_json, 'r') as infile:
        input_data = json.load(infile)

    # Transform the JSON data
    transformed_data = transform_json(input_data)

    # Write the transformed data to the output file
    with open(args.output_json, 'w') as outfile:
        json.dump(transformed_data, outfile, indent=4)

if __name__ == "__main__":
    main()
