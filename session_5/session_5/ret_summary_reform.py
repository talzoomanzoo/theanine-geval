import json
import argparse
import re

def determine_speaker(utter_id, reference_data):
    # Get the speaker information from the reference data
    speaker = "Unknown"
    for ref in reference_data:
        if ref.get("utter_id") == utter_id:
            speaker = ref.get("speaker", "Unknown")
            break
    return speaker

def transform_json(input_data, reference_data):
    transformed_data = []
    
    sorted_input_data = sorted(input_data.items(), key=lambda x: int(x[0].split('-')[0][1:]))

    for utter_id, details in sorted_input_data:
        # Retrieve memory list and combine it into memory_text
        if "retrieved_memory_list" in details:
            memory_text = "\n".join([f"{i+1}. {text}" for i, text in enumerate(details["retrieved_memory_list"])])
        else:
            memory_text = ""

        # Handle response to determine raw_prediction
        response_text = details.get("response", "")
        raw_prediction = response_text
        combined_dialogue = "\n".join(details["current_dialogue"])
        
        # Determine the speaker based on the reference data
        speaker = determine_speaker(utter_id, reference_data)
        
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
    parser.add_argument("reference_json", help="Path to the reference JSON file.")
    parser.add_argument("output_json", help="Path to the output JSON file.")

    args = parser.parse_args()

    # Read input JSON
    with open(args.input_json, 'r') as infile:
        input_data = json.load(infile)

    # Read reference JSON
    with open(args.reference_json, 'r') as reffile:
        reference_data = json.load(reffile)

    # Transform the JSON data
    transformed_data = transform_json(input_data, reference_data)

    # Write the transformed data to the output file
    with open(args.output_json, 'w') as outfile:
        json.dump(transformed_data, outfile, indent=4)

if __name__ == "__main__":
    main()
