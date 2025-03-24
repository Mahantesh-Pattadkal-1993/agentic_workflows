import fitz  # PyMuPDF
import streamlit as st
import tempfile
import os
import logging
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class PDFReader:
    def __init__(self, pdf_path):
        """Initialize with path to PDF file."""
        self.pdf_path = pdf_path
        self.doc = None
        logger.info(f"Initialized PDFReader with path: {pdf_path}")

    def open_pdf(self):
        """Open the PDF file."""
        try:
            logger.info(f"Attempting to open PDF file: {self.pdf_path}")
            self.doc = fitz.open(self.pdf_path)
            logger.info(f"Successfully opened PDF with {len(self.doc)} pages")
            return True
        except Exception as e:
            logger.error(f"Error opening PDF: {str(e)}", exc_info=True)
            st.error(f"Error opening PDF: {e}")
            return False

    def get_text_from_page(self, page_num):
        """Extract text from a specific page."""
        try:
            logger.debug(f"Extracting text from page {page_num}")
            page = self.doc[page_num]
            text = page.get_text()
            logger.debug(f"Successfully extracted {len(text)} characters from page {page_num}")
            return text
        except Exception as e:
            logger.error(f"Error reading page {page_num}: {str(e)}", exc_info=True)
            st.error(f"Error reading page {page_num}: {e}")
            return None

    def get_all_text(self):
        """Extract text from all pages."""
        logger.info("Starting text extraction from all pages")
        if not self.doc:
            logger.info("Opening PDF file before text extraction")
            self.open_pdf()
        
        text = []
        for page_num in range(len(self.doc)):
            logger.debug(f"Processing page {page_num + 1}/{len(self.doc)}")
            page_text = self.get_text_from_page(page_num)
            if page_text:
                text.append(page_text)
        
        combined_text = "\n".join(text)
        logger.info(f"Completed text extraction. Total characters: {len(combined_text)}")
        return combined_text
    
    def get_chunks(self, text):
        """Split text into chunks of 1000 characters."""
        logger.info("Starting text chunking process")
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,   # Each chunk will be 1000 characters
            chunk_overlap=100  # Overlap of 100 characters between chunks
        )
        chunks = text_splitter.split_text(text)
        logger.info(f"Created {len(chunks)} chunks from text")
        return chunks

    def get_page_count(self):
        """Get total number of pages."""
        if not self.doc:
            self.open_pdf()
        count = len(self.doc)
        logger.info(f"PDF has {count} pages")
        return count

    def close(self):
        """Close the PDF document."""
        if self.doc:
            logger.info("Closing PDF document")
            self.doc.close()
            logger.info("PDF document closed successfully")

# Streamlit interface
if __name__ == "__main__":
    st.title("PDF Reader")
    
    # File uploader
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
    
    if uploaded_file is not None:
        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_file_path = tmp_file.name
        
        # Create PDF reader instance
        pdf_reader = PDFReader(tmp_file_path)
        
        # Open the PDF
        if pdf_reader.open_pdf():
            # Get total pages
            total_pages = pdf_reader.get_page_count()
            st.write(f"Total pages: {total_pages}")
            
            # Add a page selector
            page_num = st.number_input("Select page number", min_value=1, max_value=total_pages, value=1) - 1
            
            # Read selected page
            page_text = pdf_reader.get_text_from_page(page_num)
            if page_text:
                st.write("Page content:")
                st.text_area("", page_text, height=300)
            
            # Option to show all pages
            if st.button("Show all pages"):
                all_text = pdf_reader.get_all_text()
                st.write("All pages content:")
                st.text_area("", all_text, height=500)
            if st.button("Show chunks"):
                all_text = pdf_reader.get_all_text()
                chunks = pdf_reader.get_chunks(all_text)
                for i, chunk in enumerate(chunks):
                    st.write(f"Chunk {i+1}:\n{chunk}\n")
                     # Close the PDF
            pdf_reader.close()

            
        # Clean up temporary file
        os.unlink(tmp_file_path)