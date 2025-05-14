import os

def load_documents_from_folder(folder_path):
    """
    Lê todos os arquivos .txt dentro da pasta e subpastas.
    Retorna uma lista de strings (conteúdo dos documentos).
    """
    docs = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".txt"):
                file_path = os.path.join(root, file)
                with open(file_path, "r", encoding="utf-8") as f:
                    docs.append(f.read())
    return docs
