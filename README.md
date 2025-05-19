AI-Powered Document Summarizer
An AI-powered document summarizer that extracts, preprocesses, and summarizes text from various sources including PDFs, images, text files, and websites. The project leverages state-of-the-art NLP models and offers multiple output formats such as PDF, Word, and audio summaries.

Features
Summarize Files: Extracts and summarizes text from PDFs, text files, and images.
Summarize Websites: Scrapes content from a given URL and generates a summary.
Preprocessing: Removes unnecessary content like email addresses and phone numbers.
Multi-format Export: Save summaries as:
PDF
Word Document
MP3 Audio File
Multi-tasking: Process multiple files or tasks in one session.
Requirements
Python 3.8 or higher
Dependencies listed in requirements.txt
Key Libraries
transformers: For text summarization.
PyMuPDF (fitz): For PDF text extraction.
pytesseract: For OCR text extraction from images.
gtts: For text-to-speech conversion.
fpdf: For PDF export.
python-docx: For Word document export.
Installation
Clone the repository:
git clone https://github.com/<your-username>/AI-Powered-Document-Summarizer.git
cd AI-Powered-Document-Summarizer


Example Input: File: sample-1.pdf Text: Lorem ipsum Nam liber tempor cum soluta nobis eleifend option congue nihil imperdiet doming... Output: Summary: Nam liber tempor cum soluta nobis eleifend option congue... Exports: summary.pdf summary.docx

Contributing Contributions are welcome! Feel free to submit issues or pull requests.
