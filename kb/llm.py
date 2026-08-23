from openai import OpenAI

from .config import Config

SYSTEM_PROMPT = (
    "你是一个个人知识库助手。请仅根据下面提供的笔记内容回答用户的问题，"
    "并尽量引用笔记中的原文。如果笔记内容不足以回答，请如实说明，不要编造。"
)


class LLM:
    """OpenAI 兼容的聊天模型抽象层：切换提供方只需改 base_url 与模型名。"""

    def __init__(self, config: Config):
        self._client = OpenAI(api_key=config.api_key, base_url=config.base_url)
        self._model = config.model

    def answer(self, question: str, context: str) -> str:
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": f"笔记内容：\n{context}\n\n问题：{question}",
            },
        ]
        resp = self._client.chat.completions.create(
            model=self._model, messages=messages
        )
        return resp.choices[0].message.content
