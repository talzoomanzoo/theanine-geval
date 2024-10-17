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

# Function to determine the speaker by analyzing the text after the last "###"
def determine_speaker(model_input):
    # Search for the last occurrence of "### " and get the word after it
    match = re.findall(r"###\s*(Parent|Child):", model_input)
    if match:
        return match[-1]  # Return the last match (either "Parent" or "Child")
    return "Unknown"  # Default in case no match is found

# Function to transform the input JSON format into the desired output format
def transform_json(input_data):
    transformed_data = []

    for utter_id, data in input_data.items():
        # Extract memory_text using the helper function
        model_input = data.get("model_input", "")
        memory_text = extract_memory_text(model_input)

        # Determine the speaker based on the last occurrence of "###"
        speaker = determine_speaker(model_input)

        # Extract other relevant fields and create the final entry
        transformed_entry = {
            "utter_id": utter_id,
            "current_dialogue": data.get("current_dialogue", "").strip(),
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
    parser.add_argument("output_path", type=str, help="Path to save the transformed output JSON file")

    args = parser.parse_args()

    # Load input JSON data
    with open(args.input_path, "r") as infile:
        input_data = json.load(infile)

    # Transform the input data
    transformed_data = transform_json(input_data)

    # Save the transformed data to the output file
    with open(args.output_path, "w") as outfile:
        json.dump(transformed_data, outfile, indent=4)

    print(f"Transformation complete. Output saved to {args.output_path}")

if __name__ == "__main__":
    main()
