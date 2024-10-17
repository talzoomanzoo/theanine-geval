import os
import json
import argparse

def count_likert(folder_path, output_file_path):
    # Initialize counters for Likert scale scores and N/A
    one_count = 0
    two_count = 0
    three_count = 0
    four_count = 0
    five_count = 0
    na_count = 0

    # Loop through each file in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith('.json'):
            file_path = os.path.join(folder_path, filename)
            
            # Open and load the JSON file
            with open(file_path, 'r') as f:
                data = json.load(f)
            
            # Extract the prediction text
            prediction_text = data.get('prediction', '')
            
            # Check for Helpfulness Score in the prediction text
            if "Helpfulness Score: \"1\"" in prediction_text or "Helpfulness Score: 1" in prediction_text:
                one_count += 1
            elif "Helpfulness Score: \"2\"" in prediction_text or "Helpfulness Score: 2" in prediction_text:
                two_count += 1
            elif "Helpfulness Score: \"3\"" in prediction_text or "Helpfulness Score: 3" in prediction_text:
                three_count += 1
            elif "Helpfulness Score: \"4\"" in prediction_text or "Helpfulness Score: 4" in prediction_text:
                four_count += 1
            elif "Helpfulness Score: \"5\"" in prediction_text or "Helpfulness Score: 5" in prediction_text:
                five_count += 1
            else:
                na_count += 1

    # Calculate totals and averages
    total_count_with_na = one_count + two_count + three_count + four_count + five_count + na_count
    total_count_without_na = one_count + two_count + three_count + four_count + five_count

    # Calculate weighted sum for the average
    weighted_sum = (one_count * 1) + (two_count * 2) + (three_count * 3) + (four_count * 4) + (five_count * 5)

    # Average with N/A considered as 0
    if total_count_with_na > 0:
        avg_with_na = weighted_sum / total_count_with_na
    else:
        avg_with_na = 0

    # Average without N/A
    if total_count_without_na > 0:
        avg_without_na = weighted_sum / total_count_without_na
    else:
        avg_without_na = 0

    # Output results to the specified file
    with open(output_file_path, 'w') as output_file:
        output_data = {
            'one_count': one_count,
            'two_count': two_count,
            'three_count': three_count,
            'four_count': four_count,
            'five_count': five_count,
            'na_count': na_count,
            'average_with_na': avg_with_na,
            'average_without_na': avg_without_na
        }
        json.dump(output_data, output_file, indent=4)

    print(f"Results saved to {output_file_path}")

if __name__ == '__main__':
    # Set up argument parsing
    parser = argparse.ArgumentParser(description='Count likert scale and calculate ratios.')
    parser.add_argument('folder_path', type=str, help='Path to the folder containing the JSON files.')
    parser.add_argument('output_file_path', type=str, help='Path to save the output JSON file.')

    # Parse the arguments
    args = parser.parse_args()

    # Run the counting function with the provided arguments
    count_likert(args.folder_path, args.output_file_path)
