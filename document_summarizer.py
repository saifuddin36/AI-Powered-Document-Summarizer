import os
import re
import fitz  # PyMuPDF for PDF text extraction
import pytesseract  # OCR for scanned documents
from PIL import Image  # For image handling
from transformers import pipeline
from gtts import gTTS  # Text-to-Speech
from langdetect import detect  # Language detection
import requests  # For web scraping
from bs4 import BeautifulSoup
from fpdf import FPDF  # Export to PDF
from docx import Document  # Export to Word


class DocumentSummarizer:
    def __init__(self):
        # Initialize the summarization pipeline
        print("Device set to use CPU")
        self.summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

    def detect_language(self, text):
        try:
            return detect(text)
        except Exception as e:
            print(f"Error detecting language: {e}")
            return None

    def summarize_text(self, text, max_length=None, min_length=None):
        # Dynamically calculate lengths based on input text length
        input_length = len(text.split())

        # Set default max_length and min_length as percentages of input length
        max_length = max_length or int(input_length * 0.6)  # 60% of input length
        min_length = min_length or int(input_length * 0.3)  # 30% of input length

        # Ensure max_length is greater than min_length
        if max_length <= min_length:
            max_length = min_length + 1

        try:
            summary = self.summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)
            return summary[0]['summary_text']
        except Exception as e:
            print(f"Error summarizing text: {e}")
            return None

    def extract_text_from_pdf(self, file_path):
        try:
            doc = fitz.open(file_path)
            text = ""
            for page in doc:
                text += page.get_text()
            return text
        except Exception as e:
            print(f"Error reading PDF: {e}")
            return ""

    def extract_text_from_image(self, image_path):
        try:
            image = Image.open(image_path)
            return pytesseract.image_to_string(image)
        except Exception as e:
            print(f"Error extracting text from image: {e}")
            return ""

    def preprocess_text(self, text):
        # Remove email addresses
        text = re.sub(r'\S+@\S+', '', text)
        # Remove phone numbers
        text = re.sub(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', '', text)
        # Remove generic words like "Your City", "Your Company"
        text = re.sub(r'Your City|Your Company|Your Street|ST \d+|12345', '', text, flags=re.IGNORECASE)
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    def generate_key_points(self, text):
        # Split the text into smaller chunks and summarize each
        sentences = text.split('. ')
        key_points = []
        for sentence in sentences:
            summary = self.summarize_text(sentence, max_length=30, min_length=10)
            if summary:
                key_points.append(summary)
        return key_points

    def scrape_website(self, url):
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.content, "html.parser")
            return soup.get_text()
        except Exception as e:
            print(f"Error scraping website: {e}")
            return ""

    def export_to_pdf(self, content, output_file):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, content)
        pdf.output(output_file)
        print(f"Summary exported to {output_file}")

    def export_to_word(self, content, output_file):
        doc = Document()
        doc.add_paragraph(content)
        doc.save(output_file)
        print(f"Summary exported to {output_file}")

    def text_to_speech(self, text, output_file):
        try:
            tts = gTTS(text)
            tts.save(output_file)
            print(f"Audio summary saved to {output_file}")
        except Exception as e:
            print(f"Error generating audio summary: {e}")

    def summarize_multiple_files(self, file_paths):
        summaries = []
        for file_path in file_paths:
            if file_path.endswith(".pdf"):
                text = self.extract_text_from_pdf(file_path)
            elif file_path.endswith(".txt"):
                with open(file_path, "r", encoding="utf-8") as file:
                    text = file.read()
            elif file_path.endswith((".png", ".jpg", ".jpeg")):
                text = self.extract_text_from_image(file_path)
            else:
                print(f"Unsupported file format: {file_path}")
                continue

            if text:
                cleaned_text = self.preprocess_text(text)
                summary = self.summarize_text(cleaned_text)
                if summary:
                    summaries.append((file_path, summary))
        return summaries

    def run(self):
        print("Welcome to the AI-Powered Document Summarizer!")
        print("Options:")
        print("1. Summarize a document file (PDF, TXT, or Image).")
        print("2. Summarize multiple files.")
        print("3. Enter raw text for summarization.")
        print("4. Summarize a website URL.")

        choice = input("Enter your choice (1/2/3/4): ")

        if choice == "1":
            file_path = input("Enter the path to the document: ")
            if file_path.endswith(".pdf"):
                text = self.extract_text_from_pdf(file_path)
            elif file_path.endswith(".txt"):
                with open(file_path, "r", encoding="utf-8") as file:
                    text = file.read()
            elif file_path.endswith((".png", ".jpg", ".jpeg")):
                text = self.extract_text_from_image(file_path)
            else:
                print("Unsupported file format.")
                return

            cleaned_text = self.preprocess_text(text)
            summary = self.summarize_text(cleaned_text)

            if summary:
                print("\n--- Document Summary ---")
                print(summary)
                self.export_to_pdf(summary, "summary.pdf")
                self.export_to_word(summary, "summary.docx")
                self.text_to_speech(summary, "summary.mp3")

        elif choice == "2":
            file_paths = input("Enter the paths to the files (comma-separated): ").split(",")
            summaries = self.summarize_multiple_files([path.strip() for path in file_paths])
            for file, summary in summaries:
                print(f"\n--- Summary for {file} ---")
                print(summary)

        elif choice == "3":
            raw_text = input("Enter the text you want to summarize: ")
            summary = self.summarize_text(raw_text)
            if summary:
                print("\n--- Document Summary ---")
                print(summary)

        elif choice == "4":
            url = input("Enter the website URL: ")
            text = self.scrape_website(url)
            cleaned_text = self.preprocess_text(text)
            summary = self.summarize_text(cleaned_text)
            if summary:
                print("\n--- Website Summary ---")
                print(summary)

        else:
            print("Invalid choice. Exiting.")


if __name__ == "__main__":
    summarizer = DocumentSummarizer()
    summarizer.run()
