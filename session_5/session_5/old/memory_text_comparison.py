import pandas as pd
import json
import argparse

# Function to transform multiple JSON data files to a single Excel file
def json_to_excel(input_files, output_file):
    all_data = []
    row_names = set()
    
    # Loop over each input file and process it
    for input_file in input_files:
        with open(input_file, 'r') as file:
            json_data = json.load(file)
        
        # Extract the data from the JSON objects in the current file
        data = []
        current_row_names = []
        for entry in json_data:
            current_row_names.append(entry['utter_id'])
            row_data = {}
            for key, value in entry.items():
                if key != 'utter_id':
                    row_data[key] = value
            data.append(row_data)
        
        # Create a DataFrame for the current file
        df = pd.DataFrame(data, index=current_row_names)
        
        # Append data and update the row names set
        all_data.append(df)
        row_names.update(current_row_names)
    
    # Merge all dataframes by their index (utter_id) and use file names as column keys
    combined_df = pd.concat(all_data, axis=1, join="outer", keys=[input_file for input_file in input_files])

    # Save DataFrame to Excel
    combined_df.to_excel(output_file)

    print(f"Data successfully written to {output_file}")

# Main function to handle argparse inputs
def main():
    parser = argparse.ArgumentParser(description="Convert multiple JSON files to a single Excel file.")
    parser.add_argument('input_files', type=str, nargs='+', help='List of input JSON files')
    parser.add_argument('output_file', type=str, help='Path to the output Excel file')

    args = parser.parse_args()

    # Call the conversion function with multiple input files
    json_to_excel(args.input_files, args.output_file)

if __name__ == "__main__":
    main()
