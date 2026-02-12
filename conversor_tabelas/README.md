# Conversor de Tabelas Hospitalares
Aplicação local para conversão de textos não estruturados em Excel.


Gemini said
Com certeza, vamos simplificar. Imagine que cada "Tipo" é uma ferramenta diferente na sua caixa de ferramentas para lidar com a bagunça dos textos de hospitais.

Aqui está o resumo bem direto:

🛠️ Suas 7 Ferramentas de Conversão
Ferramenta	O que ela busca?	Quando usar?
Tipo 1	
Número + Nome + Valor	Listas simples e curtas.

Tipo 2	
Nome + Código + [Ignora lixo] + Valor	O melhor para taxas e diárias. Ele joga fora as observações inúteis.

Tipo 3	
Código + Nome	Quando não tem preço, apenas uma lista de códigos e nomes.

Tipo 4	
Número + Nome + R$ Valor	Quando você quer ter certeza que só vai pegar o que tem R$.

Tipo 5	
Nome + Código	Quando o código de 8 dígitos aparece no final da linha.

Tipo 6	
Nome + R$ Valor	Quando o texto não tem código, apenas o nome do serviço e o preço.

Tipo 7	
Dado ; Dado ; Dado	Quando os dados estão separados por ; ou espaços muito grandes.

## Como usar:
1. Instale as dependências: `pip install -r requirements.txt`
2. Inicie a aplicação: `python app.py`
3. Acesse no navegador: `http://localhost:5000`

## Estrutura:
- `processors/`: Lógica de extração (Regex/Texto).
- `services/`: Geração de arquivos Excel.
- `static/`: Interface visual (CSS/JS).
