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

def extract_text_from_pdf(pdf_path, reader, progress_bar, progress_text, current, total):
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
        st.error(f"❗ Error processing {os.path.basename(pdf_path)}: {e}")
    progress_bar.progress(min(current / total, 1.0))
    progress_text.text(f"📄 Processing {current}/{total} - {os.path.basename(pdf_path)}")
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
    st.set_page_config(page_title="Academic Plagiarism Detector", layout="wide")
    st.title("🧑‍💻 Academic Plagiarism Detector")
    st.markdown("**Upload a ZIP file containing multiple PDF documents to detect plagiarism efficiently.**")

    uploaded_file = st.file_uploader("📤 Upload ZIP File", type=["zip"], help="Ensure the ZIP contains only PDF files.")

    if uploaded_file:
        zip_path = "uploaded.zip"
        with open(zip_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success("✅ File uploaded successfully! Click on **Start Processing** to begin.")

        if st.button("🚀 Start Processing"):
            extract_to = 'test'
            extract_zip(zip_path, extract_to)
            pdf_files = [f for f in os.listdir(extract_to) if f.endswith('.pdf')]
            
            if not pdf_files:
                st.error("⚠ No PDF files found. Please check your ZIP file.")
                return

            st.info(f"📁 **Total PDF files detected:** {len(pdf_files)}")
            reader = easyocr.Reader(['en'])

            progress_bar = st.progress(0)
            progress_text = st.empty()

            texts = [extract_text_from_pdf(os.path.join(extract_to, pdf), reader, progress_bar, progress_text, i+1, len(pdf_files)) for i, pdf in enumerate(pdf_files)]
            
            st.success("✅ All files processed successfully!")
            results, no_plagiarism_files = detect_plagiarism(texts, pdf_files)

            if results:
                st.write("## 🚩 Detected Plagiarized Files:")
                for file1, file2, sim in results:
                    st.markdown(f"<p style='font-size:20px;'><strong>{file1}</strong> & <strong>{file2}</strong> - Similarity: <strong>{sim*100:.2f}%</strong></p>", unsafe_allow_html=True)
            else:
                st.success("🎉 No plagiarism detected among any files.")
            
            if no_plagiarism_files:
                st.write("## ✅ Files with No Plagiarism Detected:")
                for file in no_plagiarism_files:
                    st.markdown(f"<p style='font-size:20px;'>📘 <strong>{file}</strong></p>", unsafe_allow_html=True)
            
            shutil.rmtree(extract_to)
            os.remove(zip_path)

if __name__ == "__main__":
    main()
