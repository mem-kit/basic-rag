from langchain_community.embeddings import QianfanEmbeddingsEndpoint
from langchain_community.llms.baidu_qianfan_endpoint import QianfanLLMEndpoint

from dotenv import load_dotenv


load_dotenv()

embeddings = QianfanEmbeddingsEndpoint(model="bge-large-zh")
result = embeddings.embed_documents(["test"])
print("ok", result)

llm = QianfanLLMEndpoint(model="ERNIE-4.0-8K")
input_text = "用50个字左右阐述，生命的意义在于什么, 谢谢"
llm.invoke(input_text)

for chunk in llm.stream(input_text):
    print(chunk)