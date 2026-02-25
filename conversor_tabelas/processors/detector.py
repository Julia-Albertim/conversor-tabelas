import re

def identify(text):
    """
    Tenta identificar o padrão da tabela com base no conteúdo.
    Prioriza o novo padrão universal se encontrar preços no fim das linhas.
    """
    lines = text.strip().split('\n')
    if not lines:
        return 'auto'
        
    # Padrão universal: Descrição longa terminando em Valor R$ (com ou sem ponto de milhar)
    universal_pattern = re.compile(r'.*?\s*(?:R\$\s*)?(\d{1,3}(?:\.\d{3})*,\d{2})$')
    
    match_count = 0
    for line in lines[:5]:  # Verifica as primeiras 5 linhas
        if universal_pattern.match(line.strip()):
            match_count += 1
            
    if match_count >= 1:
        return 'tipo8'

    # Se tiver ponto e vírgula, grandes chances de ser o Tipo 7
    if ";" in text:
        return 'tipo7'
    
    # Se tiver R$, mas não tiver muitos números de 8 dígitos (códigos)
    if "R$" in text:
        if "Incluso" in text or "Exclui" in text:
            return 'tipo2'
        if any(len(w) == 8 and w.isdigit() for w in text.split()):
            return 'tipo2'
        return 'tipo6'

    # Se não tiver R$, mas tiver códigos de 8 dígitos
    if any(len(w) == 8 and w.isdigit() for w in text.split()):
        return 'tipo3'
    
    # Padrão básico (Tipo 1)
    return 'tipo1'  
