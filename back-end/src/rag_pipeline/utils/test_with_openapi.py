from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI

from core.prompt_utils import parse_docs

def test_response_with_openai(retriever):
    def get_openai_model():
        model = ChatOpenAI(model="gpt-4o")
        print("🔄 Testando resposta com OpenAI GPT-4o")
        return model

    def build_prompt_openai(kwargs):
        docs = kwargs["context"]
        question = kwargs["question"]
        context_text = "".join(docs["texts"])
        prompt_content = [
            {"type": "text", "text": f"""
            Responda com base apenas no contexto fornecido...
            Contexto: {context_text}
            Pergunta: {question}
            """}
        ]
        for image in docs["images"]:
            prompt_content.append({"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image}"}})
        return ChatPromptTemplate.from_messages([HumanMessage(content=prompt_content)])

    return {
        "context": retriever | RunnableLambda(parse_docs),
        "question": RunnablePassthrough(),
    } | RunnablePassthrough().assign(
        response=(RunnableLambda(build_prompt_openai) | get_openai_model() | StrOutputParser())
    )