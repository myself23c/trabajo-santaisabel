import os
from docx import Document
from fpdf import FPDF
import pandas as pd

def list_files(extension):
    return [f for f in os.listdir('.') if f.endswith(extension)]

def docx_to_pdf(docx_file):
    document = Document(docx_file)
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    for para in document.paragraphs:
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, para.text)
    
    pdf_file = docx_file.replace('.docx', '.pdf')
    pdf.output(pdf_file)
    print(f'{docx_file} has been converted to {pdf_file}')

def csv_to_excel(csv_file, encoding='utf-8'):
    try:
        df = pd.read_csv(csv_file, encoding=encoding, on_bad_lines='skip')
        excel_file = csv_file.replace('.csv', '.xlsx')
        df.to_excel(excel_file, index=False)
        print(f'{csv_file} has been converted to {excel_file}')
    except UnicodeDecodeError:
        print(f"Failed to read {csv_file} with encoding {encoding}. Please specify the correct encoding.")
    except pd.errors.ParserError as e:
        print(f"Error parsing {csv_file}: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    while True:
        print("\nChoose the type of conversion:")
        print("1. DOCX to PDF")
        print("2. CSV to Excel")
        print("3. Exit")
        choice = input("Enter your choice (1/2/3): ")

        if choice == '1':
            docx_files = list_files('.docx')
            if not docx_files:
                print("No DOCX files found in the current directory.")
            else:
                print("DOCX files found:")
                for idx, file in enumerate(docx_files):
                    print(f"{idx + 1}. {file}")
                file_choice = int(input("Enter the number of the file to convert: ")) - 1
                if 0 <= file_choice < len(docx_files):
                    docx_to_pdf(docx_files[file_choice])
                else:
                    print("Invalid choice.")
        elif choice == '2':
            csv_files = list_files('.csv')
            if not csv_files:
                print("No CSV files found in the current directory.")
            else:
                print("CSV files found:")
                for idx, file in enumerate(csv_files):
                    print(f"{idx + 1}. {file}")
                file_choice = int(input("Enter the number of the file to convert: ")) - 1
                if 0 <= file_choice < len(csv_files):
                    encoding = input("Enter the file encoding (default 'utf-8'): ") or 'utf-8'
                    csv_to_excel(csv_files[file_choice], encoding)
                else:
                    print("Invalid choice.")
        elif choice == '3':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == '__main__':
    main()
