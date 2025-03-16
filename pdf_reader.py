import fitz  # PyMuPDF

class PDFReader:
    def __init__(self, pdf_path):
        """Initialize with path to PDF file."""
        self.pdf_path = pdf_path
        self.doc = None

    def open_pdf(self):
        """Open the PDF file."""
        try:
            self.doc = fitz.open(self.pdf_path)
            return True
        except Exception as e:
            print(f"Error opening PDF: {e}")
            return False

    def get_text_from_page(self, page_num):
        """Extract text from a specific page."""
        try:
            page = self.doc[page_num]
            text = page.get_text("text")  # Explicitly specify text extraction mode
            return text
        except UnicodeDecodeError:
            try:
                # Try alternative encoding
                text = page.get_text("text").encode('latin-1').decode('utf-8', errors='ignore')
                return text
            except Exception as e:
                print(f"Error reading page {page_num} with alternative encoding: {e}")
                return None
        except Exception as e:
            print(f"Error reading page {page_num}: {e}")
            return None

    def get_all_text(self):
        """Extract text from all pages."""
        text = []
        for page_num in range(len(self.doc)):
            page_text = self.get_text_from_page(page_num)
            if page_text:
                text.append(page_text)
        return "\n".join(text)

    def get_page_count(self):
        """Get total number of pages."""
        return len(self.doc)

    def close(self):
        """Close the PDF document."""
        if self.doc:
            self.doc.close()

# Example usage
if __name__ == "__main__":
    # Example PDF path - replace with your PDF file path
    pdf_path = "example.pdf"
    
    # Create PDF reader instance
    pdf_reader = PDFReader(pdf_path)
    
    # Open the PDF
    if pdf_reader.open_pdf():
        try:
            # Get total pages
            total_pages = pdf_reader.get_page_count()
            print(f"Total pages: {total_pages}")
            
            # Read first page
            first_page_text = pdf_reader.get_text_from_page(0)
            if first_page_text:
                print("\nFirst page content:")
                print(first_page_text)
            
            # Read all pages
            all_text = pdf_reader.get_all_text()
            if all_text:
                print("\nAll pages content:")
                print(all_text)
        except Exception as e:
            print(f"Error processing PDF: {e}")
        finally:
            # Close the PDF
            pdf_reader.close() 