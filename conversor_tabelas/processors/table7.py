import re

def process(text):
    
    # 60033533 | Acompanhante de paciente menor de 18 anos e maior de  60 anos | 1020,00
    # Divide o texto em linhas e limpa espaços
    linhas = [l.strip() for l in text.splitlines() if l.strip()]
    registros = []
    
    buffer_nome = []
    codigo_atual = None

    for linha in linhas:
        # 1. Tenta achar o código de 8 dígitos (em qualquer lugar da linha)
        match_codigo = re.search(r'\b(\d{8})\b', linha)
        
        # 2. Tenta achar o valor no final da linha (ex: 1020,00)
        # Procuramos um padrão de número com vírgula que esteja NO FIM da linha
        match_valor = re.search(r'(\d+,\d{2})$', linha)

        # SE ACHOU CÓDIGO: Começa um novo registro
        if match_codigo:
            # Se já tinha um código antes sem fechar, podemos salvar ou limpar
            codigo_atual = match_codigo.group(1)
            # Se houver texto na mesma linha do código, guarda no buffer
            texto_na_linha = linha.replace(codigo_atual, "").strip()
            if texto_na_linha:
                buffer_nome.append(texto_na_linha)
            continue

        # SE ACHOU O VALOR: Fecha o registro atual
        if match_valor and codigo_atual:
            valor_texto = match_valor.group(1)
            # O que sobrar na linha antes do valor também é nome
            parte_nome_final = linha[:linha.rfind(valor_texto)].strip()
            if parte_nome_final:
                buffer_nome.append(parte_nome_final)
            
            # Monta o resultado final
            registros.append({
                "Código": codigo_atual,
                "Descrição": " ".join(buffer_nome).strip(),
                "Valor": f"R$ {valor_texto}" # Adiciona o R$ aqui!
            })
            
            # Reseta para o próximo item
            buffer_nome = []
            codigo_atual = None
            continue

        # SE NÃO É CÓDIGO NEM VALOR: É continuação do nome
        if codigo_atual:
            buffer_nome.append(linha)

    return registros