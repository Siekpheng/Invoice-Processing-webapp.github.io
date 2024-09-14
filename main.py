import boto3
from botocore.exceptions import ClientError

# Initialize the Textract client
textract_client = boto3.client('textract')

def extract_data_from_invoice(document_path):
    with open(document_path, 'rb') as document:
        document_bytes = document.read()

    try:
        response = textract_client.analyze_document(
            Document={'Bytes': document_bytes},
            FeatureTypes=['FORMS', 'TABLES']
        )
        return response
    except ClientError as e:
        print(f"An error occurred: {e}")
        return None

def save_table_data(response, file):
    if response:
        for block in response['Blocks']:
            if block['BlockType'] == 'KEY_VALUE_SET':
                if 'KEY' in block['EntityTypes']:
                    key = ''
                    for relationship in block.get('Relationships', []):
                        if relationship['Type'] == 'CHILD':
                            for child_id in relationship['Ids']:
                                child_block = next(
                                    b for b in response['Blocks'] if b['Id'] == child_id)
                                if child_block['BlockType'] == 'WORD':
                                    key += child_block['Text'] + ' '
                                elif child_block['BlockType'] == 'SELECTION_ELEMENT':
                                    if child_block['SelectionStatus'] == 'SELECTED':
                                        key += '[X] '
                    file.write(f"Key: {key.strip()}\n")
                if 'VALUE' in block['EntityTypes']:
                    value = ''
                    for relationship in block.get('Relationships', []):
                        if relationship['Type'] == 'CHILD':
                            for child_id in relationship['Ids']:
                                child_block = next(
                                    b for b in response['Blocks'] if b['Id'] == child_id)
                                if child_block['BlockType'] == 'WORD':
                                    value += child_block['Text'] + ' '
                    file.write(f"Value: {value.strip()}\n")
            elif block['BlockType'] == 'TABLE':
                file.write("Detected a table:\n")
                for relationship in block.get('Relationships', []):
                    if relationship['Type'] == 'CHILD':
                        for child_id in relationship['Ids']:
                            cell_block = next(
                                b for b in response['Blocks'] if b['Id'] == child_id)
                            if cell_block['BlockType'] == 'CELL':
                                cell_text = ''
                                for cell_relationship in cell_block.get('Relationships', []):
                                    if cell_relationship['Type'] == 'CHILD':
                                        for cell_child_id in cell_relationship['Ids']:
                                            word_block = next(
                                                b for b in response['Blocks'] if b['Id'] == cell_child_id)
                                            if word_block['BlockType'] == 'WORD':
                                                cell_text += word_block['Text'] + ' '
                                file.write(f"Table cell text: {cell_text.strip()}\n")

# Specify the paths to your receipt files and the output file
document_paths = ['images/invoice.jpg']
output_file_path = 'output.txt'

# Extract data and save to file for both receipts
with open(output_file_path, 'w') as output_file:
    for idx, document_path in enumerate(document_paths, start=1):
        response = extract_data_from_invoice(document_path)
        output_file.write(f"--- Receipt {idx} ---\n")
        save_table_data(response, output_file)
        output_file.write("\n\n")  # Add space between receipts
