import re

def process(text):
    """
    Processador Simplificado:
    - Ignora códigos numéricos no início.
    - Captura apenas Descrição e Valor.
    - Funciona com textos em linha única ou com quebras.
    """
    if not text:
        return []

    # Limpeza inicial de espaços e prefixos "tab"
    text = re.sub(r'^tab\s*', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\s+', ' ', text.strip())
    
    results = []
    
    # Regex para capturar: (Texto da Descrição) + (Valor com vírgula)
    # O lookahead (?=\s*\d+\s|$) ajuda a separar itens grudados em linha única
    pattern = re.compile(r'(.*?)\s*(?:R\$\s*)?(\d{1,3}(?:\.\d{3})*,\d{2})(?=\s+\d+\s+|$)')
    
    matches = pattern.findall(text)
    if not matches:
        # Busca simples caso o texto não tenha delimitadores claros entre itens
        pattern_simple = re.compile(r'(.*?)\s*(?:R\$\s*)?(\d{1,3}(?:\.\d{3})*,\d{2})')
        matches = pattern_simple.findall(text)

    for match in matches:
        raw_desc = match[0].strip()
        valor = match[1].strip()
        
        # REMOVE O NÚMERO DA FRENTE:
        # Se a descrição começar com números seguidos de espaço, nós os descartamos
        descricao_limpa = re.sub(r'^\d{1,10}\s+', '', raw_desc).strip()
            
        if descricao_limpa or valor:
            results.append({
                "Descrição": descricao_limpa,
                "Valor R$": valor
            })

    return results