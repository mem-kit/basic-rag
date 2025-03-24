import os, datetime, logging

from langchain_community.embeddings import QianfanEmbeddingsEndpoint
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import Docx2txtLoader
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.document_loaders import OutlookMessageLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from dotenv import load_dotenv


load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

FAQ_BASE = os.getenv("FAQ_BASE_PATH")
FAQ_BASE_DOCS_PATH = os.getenv("FAQ_BASE_DOCS_PATH")
FAQ_BASE_INDEX_PATH = os.getenv("FAQ_BASE_INDEX_PATH")
FAQ_BASE_EMAIL_PATH = os.getenv("FAQ_BASE_EMAIL_PATH")

#
lock = FAQ_BASE + "index.lock"
#

class RAGBuildIndex:

    @staticmethod
    def build():

        # Check file lock
        if os.path.exists(lock):
            logger.error("Index Build In Progress, return!")
            return
        logger.info("RAG_Build_Index:: init")
        # Create file lock
        f = open(lock, "a")
        f.write("\n\nBuilding index: " + datetime.datetime.now().strftime("%d-%b-%Y (%H:%M:%S.%f)"))
        f.close()

        logger.info("RAG_Build_Index:: start")

        embeddings = QianfanEmbeddingsEndpoint(model="bge-large-zh")


        logger.info('Loading documents...')
        # Load Documents
        logger.info("RAG_Build_Index:: load document")
        documents = []
        for file in os.listdir(FAQ_BASE_DOCS_PATH):
            # conjunct the full file path
            file_path = os.path.join(FAQ_BASE_DOCS_PATH, file)
            logger.info('      Loading file_path: %s', file_path)
            if file.endswith('.pdf'):
                loader = PyPDFLoader(file_path)
                documents.extend(loader.load())
            elif file.endswith('.docx') or file.endswith('.doc'):
                loader = Docx2txtLoader(file_path)
                documents.extend(loader.load())
            elif file.endswith('.txt'):
                loader = TextLoader(file_path)
                documents.extend(loader.load())

        # Load Emails
        logger.info('Loading Emails...')
        email_loader = DirectoryLoader(path=FAQ_BASE_EMAIL_PATH, glob='**/*.msg',
                                      show_progress=True, loader_cls=OutlookMessageLoader)
        documents.extend(email_loader.load())
        logger.info('Documents Load Completed ')
        # Split doc to chunks
        logger.info('Splitting...')
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=10)
        chunked_documents = text_splitter.split_documents(documents)
        logger.info('Indexing')
        # Use Langchain to create the default embeddings using text-embedding-ada-002
        db = FAISS.from_documents(documents=chunked_documents, embedding=embeddings)
        logger.info('Embedding pages')
        # save the embeddings into FAISS vector store
        db.save_local(FAQ_BASE_INDEX_PATH)
        logger.info('Saved Index data')

        #
        # Remove file lock
        f = open(lock, "a")
        complete_time = datetime.datetime.now().strftime("%Y_%d_%b_%H_%M_%S_%f")
        f.write("\n\nComplete index build: " + datetime.datetime.now().strftime("%d-%b-%Y (%H:%M:%S.%f)"))
        f.close()
        os.rename(lock, "index_" + complete_time + ".lock")
        logger.info('Rename index lock')
        logger.info('Build Index All Set')
        logger.info(' ')
        logger.info(' ')

