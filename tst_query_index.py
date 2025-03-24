from rag.rag_index_holder import RagIndexHolder
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    question = "什么是皮卡鱼?"
    logger.info("The question is: %s", question)
    answer = RagIndexHolder.ask_question(question)
    logger.info("The answer is: %s", answer)