from core.retriever_pipeline import get_rag_pipeline
from utils.display_utils import display_base64_image

def main():
    regenerate = input("🔄 Deseja gerar os chunks novamente? (s/n): ").strip().lower() == "s"
    chain_with_sources = get_rag_pipeline(force_regenerate=regenerate)
    
    if not chain_with_sources:
        print("Não foi possível inicializar a pipeline.")
        return
        
    while True:
        user_input = input("\nPergunta (ou 'sair'): ")
        if user_input.strip().lower() == "sair":
            break
        print("\nBuscando resposta...")
        response = chain_with_sources.invoke(user_input)
        print("\nResposta:", response["response"])

        print("\nContexto:")
        for t in response["context"]["texts"]:
            print(t)
            print("\n" + "-" * 50 + "\n")
        for img in response["context"]["images"]:
            display_base64_image(img)

if __name__ == "__main__":
    main()