import pandas as pd

def read_text_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    return [line.strip() for line in lines if line.strip()]

def process_table_data(lines):
    table_data = []
    is_table_section = False
    item_name = ""
    quantity = ""
    price = ""
    
    for line in lines:
        if "Detected a table:" in line:
            is_table_section = True
            continue
        if is_table_section:
            if line.startswith("Table cell text:"):
                cell_text = line.replace("Table cell text: ", "").strip()
                
                # Append item, quantity, and price based on the position
                if not item_name:
                    item_name = cell_text
                elif not quantity:
                    quantity = cell_text
                elif not price:
                    price = cell_text
                    # Once all three are collected, append to table data
                    if item_name and quantity and price:
                        table_data.append({'Item Name': item_name, 'Quantity': quantity, 'Price': price})
                        item_name, quantity, price = "", "", ""
    
    return table_data

def process_key_value_data(lines):
    key_value_data = []
    current_key = ""
    
    for line in lines:
        if line.startswith("Key:"):
            current_key = line.replace("Key: ", "").strip()
        elif line.startswith("Value:"):
            value = line.replace("Value: ", "").strip()
            if current_key:
                key_value_data.append({'Key': current_key, 'Value': value})
                current_key = ""
    
    return key_value_data

def save_data_to_excel(table_data, key_value_data, output_path):
    # Create a Pandas Excel writer using Openpyxl
    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        # Save table data in the first rows
        df_table = pd.DataFrame(table_data)
        df_table.to_excel(writer, sheet_name='Receipt Data', index=False, startrow=0)

        # Save key-value data starting right after the table
        start_row = len(df_table) + 2  # Leave a row space between table and key-value data
        df_key_value = pd.DataFrame(key_value_data)
        df_key_value.to_excel(writer, sheet_name='Receipt Data', index=False, startrow=start_row)

# Specify the path to your text file and the output Excel file
text_file_path = 'output.txt'
output_file_path = 'output_combined.xlsx'

# Read and process data
lines = read_text_file(text_file_path)
table_data = process_table_data(lines)
key_value_data = process_key_value_data(lines)

# Save to Excel
save_data_to_excel(table_data, key_value_data, output_file_path)
