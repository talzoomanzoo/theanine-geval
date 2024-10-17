import argparse
import json

# Define a function to calculate the average of "Theanine wins", "tie", and "Baseline wins"
def calculate_average(file1, file2, output_file):
    # Load the JSON data from the files
    with open(file1, 'r') as f1, open(file2, 'r') as f2:
        data1 = json.load(f1)
        data2 = json.load(f2)
    
    # Extract the relevant values and calculate averages, rounding to 3 decimal places
    theanine_wins_avg = round((data1["Theanine wins"] + data2["Theanine wins"]) / 2, 3)
    tie_avg = round((data1["tie"] + data2["tie"]) / 2, 3)
    baseline_wins_avg = round((data1["Baseline wins"] + data2["Baseline wins"]) / 2, 3)
    
    # Calculate the sum of the averages
    total_avg = round(theanine_wins_avg + tie_avg + baseline_wins_avg, 3)
    
    # Prepare the result dictionary
    averages = {
        f"{file1} Theanine wins": data1["Theanine wins"],
        f"{file1} tie" : data1["tie"],
        f"{file1} Baseline wins" : data1["Baseline wins"],
        f"{file2} Theanine wins": data2["Theanine wins"],
        f"{file2} tie" : data2["tie"],
        f"{file2} Baseline wins" : data2["Baseline wins"],
        "Theanine wins average": theanine_wins_avg,
        "Tie average": tie_avg,
        "Baseline wins average": baseline_wins_avg,
        "Sum of averages": total_avg
    }

    # Save the result to a JSON file
    with open(output_file, 'w') as outfile:
        json.dump(averages, outfile, indent=4)
    
    print(f"Averages saved to {output_file}")

# Set up argparse to handle input and output file paths
def main():
    parser = argparse.ArgumentParser(description="Calculate and save the averages from two JSON files.")
    parser.add_argument("file1", type=str, help="Path to the first input JSON file")
    parser.add_argument("file2", type=str, help="Path to the second input JSON file")
    parser.add_argument("output_file", type=str, help="Path to save the output JSON file")
    
    args = parser.parse_args()
    
    # Call the function with parsed arguments
    calculate_average(args.file1, args.file2, args.output_file)

if __name__ == "__main__":
    main()
