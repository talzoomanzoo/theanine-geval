import os
import json
import argparse

def count_win_loss_tie(folder_path, output_file_path):
    # Initialize counters for "Yes", "No", "Tie", and "NA"
    win_count = 0
    loss_count = 0
    tie_count = 0
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
            if "\n\nChoice: 1" in prediction_text:
                win_count += 1
            elif "\n\nChoice: 2" in prediction_text:
                loss_count += 1
            elif "\n\nChoice: tie" in prediction_text:
                tie_count += 1
            else:
                na_count += 1

    # Calculate the total count including and excluding NA
    total_count_with_na = win_count + loss_count + tie_count + na_count
    total_count_without_na = win_count + loss_count + tie_count

    # Calculate ratios
    win_ratio_with_na = win_count / total_count_with_na if total_count_with_na > 0 else 0
    loss_ratio_with_na = loss_count / total_count_with_na if total_count_with_na > 0 else 0
    tie_ratio_with_na = tie_count / total_count_with_na if total_count_with_na > 0 else 0
    na_ratio_with_na = na_count / total_count_with_na if total_count_with_na > 0 else 0

    win_ratio_without_na = win_count / total_count_without_na if total_count_without_na > 0 else 0
    loss_ratio_without_na = loss_count / total_count_without_na if total_count_without_na > 0 else 0
    tie_ratio_without_na = tie_count / total_count_without_na if total_count_without_na > 0 else 0

    # Output the counts and ratios
    print(f"win_count: {win_count}")
    print(f"loss_count: {loss_count}")
    print(f"tie_count: {tie_count}")
    print(f"na_count: {na_count}")
    print(f"total_count: {total_count_with_na}")
    
    print(f"win_ratio (with NA): {win_ratio_with_na:.4f}")
    print(f"loss_ratio (with NA): {loss_ratio_with_na:.4f}")
    print(f"tie_ratio (with NA): {tie_ratio_with_na:.4f}")
    
    print(f"Theanine wins: {win_ratio_without_na:.4f}")
    print(f"Tie: {tie_ratio_without_na:.4f}")
    print(f"Baseline wins: {loss_ratio_without_na:.4f}")

    # Prepare the data to be saved in a JSON file
    output_data = {
        "win_count": win_count,
        "loss_count": loss_count,
        "tie_count": tie_count,
        "na_count": na_count,
        "total_count": total_count_with_na,
        "win_ratio_with_na": win_ratio_with_na,
        "loss_ratio_with_na": loss_ratio_with_na,
        "tie_ratio_with_na": tie_ratio_with_na,
        "Theanine wins": win_ratio_without_na,
        "tie": tie_ratio_without_na,
        "Baseline wins": loss_ratio_without_na
    }

    # Save the result into a JSON file
    with open(output_file_path, 'w') as outfile:
        json.dump(output_data, outfile, indent=4)

    print(f"Results saved to {output_file_path}")

if __name__ == '__main__':
    # Set up argument parsing
    parser = argparse.ArgumentParser(description='Count win, loss, tie judgements and calculate ratios.')
    parser.add_argument('folder_path', type=str, help='Path to the folder containing the JSON files.')
    parser.add_argument('output_file_path', type=str, help='Path to save the output JSON file.')

    # Parse the arguments
    args = parser.parse_args()

    # Run the counting function with the provided arguments
    count_win_loss_tie(args.folder_path, args.output_file_path)
