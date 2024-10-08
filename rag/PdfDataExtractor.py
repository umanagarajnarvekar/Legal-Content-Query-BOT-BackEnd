from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

class PDFExtractor:
    def __init__(self, pdf_path, chunk_size=1000, chunk_overlap=20):
        self.pdf_path = pdf_path
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def extract_content(self):
        splitter = RecursiveCharacterTextSplitter(chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap)
        loader = PyPDFLoader(self.pdf_path)
        file_chunks = loader.load_and_split(splitter)
        return file_chunks

# if __name__ == "__main__":
#     pdf_path = "sample.pdf"
#     extractor = PDFExtractor(pdf_path)
#     file_chunks = extractor.extract_content()
#     print(file_chunks)