import os

from langchain_core.embeddings import Embeddings
import requests
import json
import logging
from typing import Any, Dict, List, Optional
from dotenv import load_dotenv


logger = logging.getLogger(__name__)
load_dotenv()

API_KEY = os.getenv("QIANFAN_AK")
SECRET_KEY = os.getenv("QIANFAN_SK")

class BaiduEmbeddings(Embeddings):
    """
    Please check this document
    https://console.bce.baidu.com/support/?u=qfdc&timestamp=1742133605390#/api?product=QIANFAN&project=%E5%8D%83%E5%B8%86ModelBuilder&parent=%E5%90%91%E9%87%8FEmbeddings&api=rpc%2F2.0%2Fai_custom%2Fv1%2Fwenxinworkshop%2Fembeddings%2Fbge_large_zh&method=post
    """
    def _get_access_token(self):
        """
        使用 AK，SK 生成鉴权签名（Access Token）
        :return: access_token，或是None(如果错误)
        """
        url = "https://aip.baidubce.com/oauth/2.0/token"
        params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
        return str(requests.post(url, params=params).json().get("access_token"))

    def embed_query(self, text: str) -> list[float]:
        return None

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/embeddings/bge_large_zh?access_token=" + self._get_access_token()

        payload = json.dumps({
            "input": texts
        }, ensure_ascii=False)
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload.encode("utf-8"))

        print("All set: ", response)
        return response.json()['data'][0]['embedding']


embeddings = BaiduEmbeddings()
result = embeddings.embed_documents(["test"])
print("ok", result)
