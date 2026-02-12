def identify(text):
    # Se tiver ponto e vírgula, grandes chances de ser o Tipo 7
    if ";" in text:
        return 'tipo7'
    
    # Se tiver R$, mas não tiver muitos números de 8 dígitos (códigos)
    if "R$" in text:
        # Se tiver um bloco de texto grande com "Incluso" ou "Exclui"
        if "Incluso" in text or "Exclui" in text:
            return 'tipo2'
        # Se tiver números de 8 dígitos perdidos
        if any(len(w) == 8 and w.isdigit() for w in text.split()):
            return 'tipo2'
        # Se for apenas Nome e R$
        return 'tipo6'

    # Se não tiver R$, mas tiver códigos de 8 dígitos
    if any(len(w) == 8 and w.isdigit() for w in text.split()):
        # Se o código vier no final da linha (Tipo 5) ou começo (Tipo 3)
        # Aqui o detector vai no Tipo 3 por padrão, que é o mais comum
        return 'tipo3'
    
    # Padrão básico (Tipo 1)
    return 'tipo1'  