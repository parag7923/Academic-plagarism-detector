import os
import zipfile
import fitz  # PyMuPDF for PDF handling
import difflib
import shutil
import easyocr

def extract_zip(file_path, extract_to='test'):
    if not os.path.exists(extract_to):
        os.makedirs(extract_to)

    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
    print(f"Extracted to {extract_to}")

def extract_text_from_pdf(pdf_path):
    reader = easyocr.Reader(['en'])
    text = ""
    try:
        doc = fitz.open(pdf_path)
        for page in doc:
            image = page.get_pixmap()
            image.save('temp_page.png')
            result = reader.readtext('temp_page.png', detail=0)
            text += ' '.join(result) + '\n'
        doc.close()
        os.remove('temp_page.png')
    except Exception as e:
        print(f"Error processing {pdf_path}: {e}")
    return text

def detect_plagiarism(texts, file_names):
    plagiarism_results = []
    n = len(texts)
    for i in range(n):
        for j in range(i + 1, n):
            similarity = difflib.SequenceMatcher(None, texts[i], texts[j]).ratio()
            if similarity > 0.7:  # Adjust threshold as needed
                plagiarism_results.append((file_names[i], file_names[j], similarity))
    return plagiarism_results

def scan_for_plagiarism(zip_path):
    extract_to = 'test'
    extract_zip(zip_path, extract_to)
    
    pdf_files = [f for f in os.listdir(extract_to) if f.endswith('.pdf')]
    if not pdf_files:
        print("No PDF files found.")
        return

    texts = [extract_text_from_pdf(os.path.join(extract_to, pdf)) for pdf in pdf_files]
    results = detect_plagiarism(texts, pdf_files)

    if results:
        print("Detected Plagiarized Files:")
        for file1, file2, sim in results:
            print(f"{file1} and {file2} - Similarity: {sim*100:.2f}%")
    else:
        print("No plagiarism detected.")

    shutil.rmtree(extract_to)

