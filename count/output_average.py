import os
import json
import argparse

def calculate_average_from_folders(folder1, folder2, output_file):
    folder1_path = os.path.join("/home/intern/mjgwak/theanine/outputs", folder1)
    folder2_path = os.path.join("/home/intern/mjgwak/theanine/outputs", folder2)

    def extract_key(filename):
        return '_'.join(filename.split('_')[2:])
    
    folder1_files = {extract_key(f): f for f in os.listdir(folder1_path) if f.endswith('.json')}
    folder2_files = {extract_key(f): f for f in os.listdir(folder2_path) if f.endswith('.json')}
    common_files = set(folder1_files.keys()).intersection(set(folder2_files.keys()))
    
    averages = {}
    
    for file_name in common_files:
        file1 = os.path.join(folder1_path, folder1_files[file_name])
        file2 = os.path.join(folder2_path, folder2_files[file_name])
        
        with open(file1, 'r') as f1, open(file2, 'r') as f2:
            data1 = json.load(f1)
            data2 = json.load(f2)
        
        theanine_wins_avg = round((data1["Theanine wins"] + data2["Theanine wins"]) / 2, 3)
        tie_avg = round((data1["tie"] + data2["tie"]) / 2, 3)
        baseline_wins_avg = round((data1["Baseline wins"] + data2["Baseline wins"]) / 2, 3)
        
        total_avg = round(theanine_wins_avg + tie_avg + baseline_wins_avg, 3)
        
        averages[file_name] = {
            "Theanine wins average": theanine_wins_avg,
            "Tie average": tie_avg,
            "Baseline wins average": baseline_wins_avg,
            "Sum of averages": total_avg
        }
    
    output_file1 = os.path.join(folder1_path, output_file)
    output_file2 = os.path.join(folder2_path, output_file)
    
    with open(output_file1, 'w') as outfile1, open(output_file2, 'w') as outfile2:
        json.dump(averages, outfile1, indent=4)
        json.dump(averages, outfile2, indent=4)
    
    print(f"Averages saved to {output_file1} and {output_file2}")

def main():
    parser = argparse.ArgumentParser(description="Calculate and save the averages from JSON files in two folders.")
    parser.add_argument("folder1", type=str, help="Name of the first folder")
    parser.add_argument("folder2", type=str, help="Name of the second folder")
    parser.add_argument("output_file", type=str, help="Name of the output JSON file")
    
    args = parser.parse_args()
    
    calculate_average_from_folders(args.folder1, args.folder2, args.output_file)

if __name__ == '__main__':
    main()
