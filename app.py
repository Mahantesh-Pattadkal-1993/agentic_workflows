import streamlit as st
import os
import tempfile
import logging
from LLMEngine.ingestion import IngestDocument

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

st.set_page_config(
    page_title="PDF Document Processor",
    page_icon="📄",
    layout="centered"
)

st.title("PDF Document Processor")
st.write("Upload your PDF file to process and store it in the database.")

# Create a placeholder for logs
log_placeholder = st.empty()

# Create an expander for detailed logs
with st.expander("View Processing Logs", expanded=False):
    log_container = st.container()

uploaded_file = st.file_uploader("Choose a PDF file", type=['pdf'])

if uploaded_file is not None:
    logger.info(f"File uploaded: {uploaded_file.name}")
    
    # Create a temporary file to save the uploaded PDF
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        tmp_file_path = tmp_file.name
        logger.info(f"Temporary file created at: {tmp_file_path}")

    try:
        with st.spinner('Processing your PDF...'):
            # Initialize the document processor with the temporary file path
            logger.info("Initializing document processor")
            document_processor = IngestDocument(filepath=tmp_file_path)
            
            # Process the document
            logger.info("Starting document processing")
            document_processor.ingest_document()
            
            st.success("PDF processed successfully!")
            logger.info("Document processing completed successfully")
            
    except Exception as e:
        error_msg = f"An error occurred while processing the PDF: {str(e)}"
        logger.error(error_msg, exc_info=True)
        st.error(error_msg)
    
    # finally:
    #     # Clean up the temporary file
    #     if os.path.exists(tmp_file_path):
    #         logger.info(f"Cleaning up temporary file: {tmp_file_path}")
    #         os.remove(tmp_file_path)
    #         logger.info("Temporary file removed")

st.markdown("---")
st.markdown("""
### Instructions:
1. Click on 'Browse files' to select a PDF document
2. Wait for the processing to complete
3. The document will be chunked and stored in the database
4. View detailed processing logs by expanding the 'View Processing Logs' section
""")