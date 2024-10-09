from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

class PDFExtractor:
    """
    A class to extract text from a PDF file and split it into smaller chunks using the
    RecursiveCharacterTextSplitter. This is useful for processing large PDFs where the content
    needs to be split into smaller pieces for further analysis or processing.
    """
    
    def __init__(self, pdf_path, chunk_size=1000, chunk_overlap=20):
        """
        Initializes the PDFExtractor with the file path of the PDF, the size of each chunk,
        and the overlap between consecutive chunks.
        
        Args:
            pdf_path (str): Path to the PDF file to be processed.
            chunk_size (int): Maximum size of each text chunk. Default is 1000 characters.
            chunk_overlap (int): Number of overlapping characters between consecutive chunks. Default is 20 characters.
        """
        self.pdf_path = pdf_path  # Store the PDF file path
        self.chunk_size = chunk_size  # Set the maximum size for each chunk of text
        self.chunk_overlap = chunk_overlap  # Set the overlap between consecutive text chunks

    def extract_content(self):
        """
        Extracts the text content from the PDF and splits it into smaller chunks using
        RecursiveCharacterTextSplitter.

        Returns:
            list: A list of text chunks extracted from the PDF.
        """
        # Initialize a text splitter with the specified chunk size and overlap
        splitter = RecursiveCharacterTextSplitter(chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap)
        
        # Load the PDF content using PyPDFLoader
        loader = PyPDFLoader(self.pdf_path)
        
        # Extract the text from the PDF and split it into chunks using the splitter
        file_chunks = loader.load_and_split(splitter)
        
        # Return the list of text chunks
        return file_chunks

# Example usage:
# Uncomment the following lines to use the PDFExtractor on a PDF file

# if __name__ == "__main__":
#     pdf_path = "sample.pdf"  # Specify the path to the PDF file
#     extractor = PDFExtractor(pdf_path)  # Create an instance of the PDFExtractor class
#     file_chunks = extractor.extract_content()  # Extract and split the PDF content into chunks
#     print(file_chunks)  # Output the chunks to verify the extracted text
