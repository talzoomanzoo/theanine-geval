import os
import json
import argparse

def count_yes_no_na(folder_path, output_file_path):
    # Initialize counters for "Yes", "No", and "NA"
    yes_count = 0
    no_count = 0
    na_count = 0

    # Loop through each file in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith('.json'):
            file_path = os.path.join(folder_path, filename)
            
            # Open and load the JSON file
            with open(file_path, 'r') as f:
                data = json.load(f)
            
            # Extract the Judgement part from the prediction
            prediction_text = data.get('prediction', '')
            if "Judgement: \"Yes\"" in prediction_text or "Judgement: Yes" in prediction_text:
                yes_count += 1
            elif "Judgement: \"No\"" in prediction_text or "Judgement: No" in prediction_text:
                no_count += 1
            else:
                na_count += 1

    # Calculate the total count including and excluding NA
    total_count_with_na = yes_count + no_count + na_count
    total_count_without_na = yes_count + no_count

    # Calculate ratios
    yes_ratio_with_na = yes_count / total_count_with_na if total_count_with_na > 0 else 0
    no_ratio_with_na = no_count / total_count_with_na if total_count_with_na > 0 else 0

    yes_ratio_without_na = yes_count / total_count_without_na if total_count_without_na > 0 else 0
    no_ratio_without_na = no_count / total_count_without_na if total_count_without_na > 0 else 0

    # Output the counts and ratios
    print(f"Yes count: {yes_count}")
    print(f"No count: {no_count}")
    print(f"NA count: {na_count}")
    print(f"Yes ratio (with NA): {yes_ratio_with_na:.2f}")
    print(f"No ratio (with NA): {no_ratio_with_na:.2f}")
    print(f"Yes ratio (without NA): {yes_ratio_without_na:.2f}")
    print(f"No ratio (without NA): {no_ratio_without_na:.2f}")

    # Prepare the data to be saved in a JSON file
    output_data = {
        "yes_count": yes_count,
        "no_count": no_count,
        "na_count": na_count,
        "yes_ratio_with_na": yes_ratio_with_na,
        "no_ratio_with_na": no_ratio_with_na,
        "yes_ratio_without_na": yes_ratio_without_na,
        "no_ratio_without_na": no_ratio_without_na
    }

    # Save the result into a JSON file
    with open(output_file_path, 'w') as outfile:
        json.dump(output_data, outfile, indent=4)

    print(f"Results saved to {output_file_path}")

if __name__ == '__main__':
    # Set up argument parsing
    parser = argparse.ArgumentParser(description='Count Yes, No, NA judgements and calculate ratios.')
    parser.add_argument('folder_path', type=str, help='Path to the folder containing the JSON files.')
    parser.add_argument('output_file_path', type=str, help='Path to save the output JSON file.')

    # Parse the arguments
    args = parser.parse_args()

    # Run the counting function with the provided arguments
    count_yes_no_na(args.folder_path, args.output_file_path)
