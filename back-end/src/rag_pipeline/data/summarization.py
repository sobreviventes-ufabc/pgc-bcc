import json
import uuid
from concurrent.futures import ThreadPoolExecutor, as_completed
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage
from langchain.schema.document import Document
from .retry import retry_with_backoff
from ..core.models import get_llama_model, get_llava_model

def summarize_elements(elements, is_table=False):
    prompt_template = """
    Você é um assistente encarregado de resumir textos institucionais da UFABC.
    Resuma o conteúdo sem perder nenhuma informação importante, incluindo números, fórmulas ou regras específicas como "C = 16 + 5CR".
    Evite reescrever as ideias com outras palavras. Mantenha expressões-chave sempre que forem relevantes.
    Responda apenas com o resumo, sem comentários adicionais: {element}
    """
    model = get_llama_model()
    prompt = ChatPromptTemplate.from_template(prompt_template)
    chain = {"element": lambda x: x} | prompt | model | StrOutputParser()

    summaries = []
    def summarize_single(element):
        return retry_with_backoff(lambda: chain.invoke({"element": element}))
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(summarize_single, el) for el in elements]
        for future in as_completed(futures):
            try:
                summaries.append(future.result())
            except Exception:
                summaries.append("Erro ao resumir.")
    return summaries

def summarize_images(images):
    prompt_text = (
    "Resuma objetivamente o conteúdo da imagem. "
    "A imagem pertence a um documento acadêmico da Universidade Federal do ABC (UFABC). "
    "Foque em identificar informações relevantes como logotipos, textos institucionais, títulos, ou elementos gráficos com significado acadêmico, e seja bem específico. "
    "Resuma apenas o conteúdo informativo.")
    model = get_llava_model()
    summaries = []

    def summarize_image(img_b64):
        prompt = ChatPromptTemplate.from_messages([HumanMessage(content=[
            {"type": "text", "text": prompt_text},
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_b64}"}}
        ])])
        chain = prompt | model | StrOutputParser()
        return retry_with_backoff(lambda: chain.invoke({}))

    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(summarize_image, img) for img in images]
        for future in as_completed(futures):
            try:
                summaries.append(future.result())
            except Exception:
                summaries.append("Erro ao resumir imagem.")
    return summaries

def add_documents(originals, summaries, retriever):
    if not originals or not summaries or len(originals) != len(summaries):
        return
    ids = [str(uuid.uuid4()) for _ in originals]
    retriever.vectorstore.add_documents([
        Document(page_content=s, metadata={"doc_id": ids[i]})
        for i, s in enumerate(summaries)
    ])
    pairs = []
    for i, orig in enumerate(originals):
        if isinstance(orig, str):
            pairs.append((ids[i], orig.encode("utf-8")))   # <- transforma em bytes
        else:
            # já é bytes (ex.: base64 de imagem), mantém
            pairs.append((ids[i], orig))
    retriever.docstore.mset(pairs)