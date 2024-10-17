import json
import argparse
import random
import os
import csv

# Function to sample instances and filter based on utter_id
def sample_and_filter(input_data, reference_files, num_samples=100):
    # Sample 100 instances from the input data while preserving the order
    random.seed(712)
    sampled_indices = sorted(random.sample(range(len(input_data)), num_samples))
    sampled_data = [input_data[i] for i in sampled_indices]
    
    # Extract utter_ids from the sampled data
    utter_ids = {item['utter_id'] for item in sampled_data}
    # Filter reference files based on the sampled utter_ids
    filtered_data = {}
    for ref_file in reference_files:
        with open(ref_file, 'r') as f:
            data = json.load(f)
            filtered_data[ref_file] = [item for item in data if item['utter_id'] in utter_ids]
    
    return sampled_data, filtered_data

# Function to add previous summary from CSV file
def add_previous_summary(data, csv_file):
    with open(csv_file, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        summary_dict = {row['dialogue']: row['memory'] for row in reader}
    
    for item in data:
        dialogue = item['current_dialogue']
        if dialogue in summary_dict:
            item['previous_summary'] = summary_dict[dialogue]
        else:
            item['previous_summary'] = None
    
    return data

# Main function to parse arguments and process the JSON files
def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Sample instances and filter JSON files based on utter_ids.")
    parser.add_argument('input_file', type=str, help='Input JSON file path')
    parser.add_argument('reference_files', type=str, nargs='+', help='Reference JSON file paths')
    parser.add_argument('output_dir', type=str, help='Output directory path')
    parser.add_argument('dataset', type=str, help='Dataset name')
    parser.add_argument('csv_file', type=str, help='CSV file path for previous summaries')
    # Parse the arguments
    args = parser.parse_args()

    # Read the input JSON file
    with open(args.input_file, 'r') as infile:
        input_data = json.load(infile)
    
    # Sample and filter the data
    sampled_data, filtered_data = sample_and_filter(input_data, args.reference_files)

    # Add previous summary to the sampled data
    sampled_data = add_previous_summary(sampled_data, args.csv_file)
    
    # Add previous summary to each list in filtered_data
    for ref_file in filtered_data:
        filtered_data[ref_file] = add_previous_summary(filtered_data[ref_file], args.csv_file)

    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)

    # Write the sampled data to the output JSON file
    sampled_output_file = f"{args.output_dir}/{args.dataset}_theanine_sampled.json"
    with open(sampled_output_file, 'w') as outfile:
        json.dump(sampled_data, outfile, indent=4)

    # Write the filtered data to separate output JSON files
    for ref_file, data in filtered_data.items():
        output_file = f"{args.output_dir}/{ref_file.split('/')[-1]}"
        with open(output_file, 'w') as outfile:
            json.dump(data, outfile, indent=4)

# Entry point of the script
if __name__ == "__main__":
    main()
