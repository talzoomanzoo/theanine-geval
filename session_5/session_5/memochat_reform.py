import json
import argparse
import re

# Function to extract memory_text from model_input by capturing text after "Related Evidences:" and "Recent Dialogs:"
def extract_memory_text(model_input):
    # Use regex to capture the text after "Related Evidences:" and "Recent Dialogs:"
    related_evidences_match = re.search(r"Related Evidences:\s*(.*)\n", model_input, re.DOTALL)
    recent_dialogs_match = re.search(r"Recent Dialogs:\s*(.*)\n", model_input, re.DOTALL)

    related_evidences = related_evidences_match.group(1).strip() if related_evidences_match else ""
    recent_dialogs = recent_dialogs_match.group(1).strip() if recent_dialogs_match else ""

    # Combine the captured parts to form the memory_text
    memory_text = f"Related Evidences: {related_evidences}\nRecent Dialogs: {recent_dialogs}"
    
    return memory_text

# Function to determine the speaker by analyzing the reference data
def determine_speaker(utter_id, reference_data):
    # Get the speaker information from the reference data
    speaker = "Unknown"
    for ref in reference_data:
        if ref.get("utter_id") == utter_id:
            speaker = ref.get("speaker", "Unknown")
            break
    return speaker

def get_current_dialogue(utter_id, reference_data):
    # Get the speaker information from the reference data
    current_dialogue = "Unknown"
    for ref in reference_data:
        if ref.get("utter_id") == utter_id:
            current_dialogue = ref.get("current_dialogue", "Unknown")
            break
    return current_dialogue

# Function to transform the input JSON format into the desired output format
def transform_json(input_data, reference_data):
    transformed_data = []

    for utter_id, data in input_data.items():
        # Extract memory_text using the helper function
        model_input = data.get("model_input", "")
        memory_text = extract_memory_text(model_input)

        # Determine the speaker based on the reference data
        speaker = determine_speaker(utter_id, reference_data)

        # Extract other relevant fields and create the final entry
        transformed_entry = {
            "utter_id": utter_id,
            "current_dialogue": get_current_dialogue(utter_id, reference_data),
            "memory_text": memory_text,
            "speaker": speaker,  # Determine if the speaker is Parent or Child
            "raw_prediction": data.get("prediction", "").strip()  # Convert prediction to raw_prediction
        }
        transformed_data.append(transformed_entry)

    return transformed_data

# Main function to handle input/output paths using argparse
def main():
    parser = argparse.ArgumentParser(description="Transform JSON structure for dialogue bot data.")
    parser.add_argument("input_path", type=str, help="Path to the input JSON file")
    parser.add_argument("reference_path", type=str, help="Path to the reference JSON file")
    parser.add_argument("output_path", type=str, help="Path to save the transformed output JSON file")

    args = parser.parse_args()

    # Load input JSON data
    with open(args.input_path, "r") as infile:
        input_data = json.load(infile)

    # Load reference JSON data
    with open(args.reference_path, "r") as reffile:
        reference_data = json.load(reffile)

    # Transform the input data
    transformed_data = transform_json(input_data, reference_data)

    # Save the transformed data to the output file
    with open(args.output_path, "w") as outfile:
        json.dump(transformed_data, outfile, indent=4)

    print(f"Transformation complete. Output saved to {args.output_path}")

if __name__ == "__main__":
    main()
