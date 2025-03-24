from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_community.embeddings import QianfanEmbeddingsEndpoint
from langchain_community.llms.baidu_qianfan_endpoint import QianfanLLMEndpoint
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.vectorstores import FAISS


from dotenv import load_dotenv
import os, threading, logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
load_dotenv()

FAQ_BASE_INDEX_PATH = os.getenv("FAQ_BASE_INDEX_PATH")
logger.info(f"FAQ_BASE_INDEX_PATH path is: {FAQ_BASE_INDEX_PATH}")

# system_prompt = (
#     "Use the given context to answer the question. "
#     "Provide the answer from the context only.  "
#     "If you can't get information from the contxt, just say 'I don't know'. "
#     "At the end, provide the support site: 'http://github.com/mem-kit' Thank you!"
#     "Context: {context}"
# )

system_prompt = (
    "使用上下午context来回答问题. "
    "你只能从提供的上下午context中来获取答案. "
    "如果你无法从上下文context中获取信息, 你只需要回答 '不好意思,我不知道'. "
    "最后: 请在文末提供支持网站: 'http://github.com/mem-kit' 谢谢!"
    "Context: {context}"
)

system_prompt = """请严格按以下步骤处理：
1. 仅使用提供的Context内容回答
2. 若Context无相关信息，直接回答'不知道'
3. 禁止添加任何外部知识
4. 回答结构尽量可能详细

Context: {context}"""


class RagIndexHolder:
    _lock = threading.Lock()
    embeddings = None
    vector_store = None
    retriever = None
    llm = None


    @staticmethod
    def init_vector_database():
        if RagIndexHolder.embeddings is None:
            with RagIndexHolder._lock:
                if RagIndexHolder.embeddings is None:
                    RagIndexHolder.embeddings = QianfanEmbeddingsEndpoint(model="bge-large-zh")
                    RagIndexHolder.vector_store = FAISS.load_local(FAQ_BASE_INDEX_PATH, RagIndexHolder.embeddings, allow_dangerous_deserialization=True)
                    RagIndexHolder.retriever = RagIndexHolder.vector_store.as_retriever()
                    RagIndexHolder.llm = QianfanLLMEndpoint(model="ERNIE-4.0-8K")
            ##
            logger.info("Init the static data with lock")
        else:
            logger.info("Get static data in class/application level")
        ##

    @staticmethod
    def ask_question(question:str):
        logger.info(f"****ask_question****: {question}")
        RagIndexHolder.init_vector_database()
        messages = [("system", system_prompt), ("human", "{input}")]
        # for m in messages:
        #     logger.info(f'***__ask_question***__message is: {m}')
        prompt = ChatPromptTemplate.from_messages(messages)
        question_answer_chain = create_stuff_documents_chain(RagIndexHolder.llm, prompt)
        chain = create_retrieval_chain(RagIndexHolder.retriever, question_answer_chain)
        response = chain.invoke({"input": question})
        return response

    @staticmethod
    def conversation(history: [], question: str):
        logger.info(f"****conversation****: {question}")
        RagIndexHolder.init_vector_database()
        messages = []
        ## make sure append it
        messages.append(("system", system_prompt))
        if history and len(history) > 0:
            for his in history:
                messages.append(his)
        ## make sure append it
        messages.append(("human", "{input}"))
        # logger.info('message list: ')
        # for m in messages:
        #     logger.info(f'  ****conversation****  message is: {m}')
        prompt = ChatPromptTemplate.from_messages(messages)
        question_answer_chain = create_stuff_documents_chain(RagIndexHolder.llm, prompt)
        chain = create_retrieval_chain(RagIndexHolder.retriever, question_answer_chain)
        response = chain.invoke({"input": question})
        return response

