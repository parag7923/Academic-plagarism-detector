import streamlit as st
import os
import zipfile
import fitz
import difflib
import shutil
import easyocr

def extract_zip(file_path, extract_to='test'):
    if not os.path.exists(extract_to):
        os.makedirs(extract_to)
    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)

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
        st.error(f"Error processing {pdf_path}: {e}")
    return text

def detect_plagiarism(texts, file_names):
    plagiarism_results = []
    no_plagiarism_files = []
    n = len(texts)
    for i in range(n):
        for j in range(i + 1, n):
            similarity = difflib.SequenceMatcher(None, texts[i], texts[j]).ratio()
            if similarity > 0.7:
                plagiarism_results.append((file_names[i], file_names[j], similarity))
            else:
                no_plagiarism_files.extend([file_names[i], file_names[j]])
    no_plagiarism_files = list(set(no_plagiarism_files) - set([x[0] for x in plagiarism_results]) - set([x[1] for x in plagiarism_results]))
    return plagiarism_results, no_plagiarism_files

def main():
    st.title("Plagiarism Feedback Generator")
    uploaded_file = st.file_uploader("Upload a ZIP file containing PDFs", type=["zip"])

    if uploaded_file:
        zip_path = "uploaded.zip"
        with open(zip_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success("File uploaded successfully! Click on Process to start detection.")

        if st.button("Process"):
            extract_to = 'test'
            extract_zip(zip_path, extract_to)
            
            pdf_files = [f for f in os.listdir(extract_to) if f.endswith('.pdf')]
            if not pdf_files:
                st.error("No PDF files found.")
                return

            texts = [extract_text_from_pdf(os.path.join(extract_to, pdf)) for pdf in pdf_files]
            results, no_plagiarism_files = detect_plagiarism(texts, pdf_files)

            if results:
                st.write("### Detected Plagiarized Files:")
                for file1, file2, sim in results:
                    st.write(f"{file1} and {file2} - Similarity: {sim*100:.2f}%")
            else:
                st.success("No plagiarism detected among any files.")
            
            if no_plagiarism_files:
                st.write("### Files with No Plagiarism Detected:")
                for file in no_plagiarism_files:
                    st.write(f"- {file}")
            
            shutil.rmtree(extract_to)
            os.remove(zip_path)

if __name__ == "__main__":
    main()
