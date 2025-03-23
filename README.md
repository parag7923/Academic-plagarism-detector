# Academic Plagiarism Detector

Academic Plagiarism Detector is a Streamlit-based application that detects plagiarism in academic PDF submissions. It extracts text using OCR and compares documents to identify similarities.

## Features
- Upload a ZIP file containing multiple PDFs
- Extract text from PDF files using OCR
- Detect plagiarism using text similarity comparison
- Display plagiarized file pairs with similarity percentages

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/parag7923/Academic-plagarism-detector.git
    cd Academic-plagarism-detector
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
    ```bash
    pip install --force-reinstall streamlit
    ```


## Running the Application

Start the application using Streamlit:
```bash
streamlit run app.py
```

## Usage
1. Open the application in your browser using the URL provided by Streamlit.
2. Upload a ZIP file containing PDFs.
3. Click the **Process** button to start the plagiarism detection.
4. View the results, including detected plagiarized files and similarity percentages.
