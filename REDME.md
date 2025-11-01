# God Level Coder Challenge – Solução de Gabriela Moura

## Resumo do Projeto
Este projeto consiste em uma plataforma de analytics para donos de restaurantes, permitindo explorar dados operacionais de forma intuitiva. A ideia é fornecer insights que não são facilmente acessíveis pelos canais tradicionais, como iFood, Rappi ou vendas presenciais. A solução permite visualizar métricas, criar dashboards personalizados, comparar períodos e identificar tendências.
A aplicação foi desenvolvida em **Python**, utilizando **Streamlit** como interface web interativa, e o banco de dados é **SQLite** para facilitar execução local. A solução já foi hospedada no **Streamlit Cloud** e pode ser acessada pelo link: [https://nola-god-level-tv2ntguxhb9hql2gk9cnnr.streamlit.app/](https://nola-god-level-tv2ntguxhb9hql2gk9cnnr.streamlit.app/)

## Tecnologias e Bibliotecas
- Python 3.11
- Streamlit
- Pandas
- Plotly
- Faker (para geração de dados fictícios)
- SQLite (banco local)

## Estrutura do Projeto
nola-god-level/
├─ app.py              # Interface Streamlit
├─ desafio.py          # Lógica do desafio
├─ reports.py          # Funções de geração de relatórios
├─ db.py               # Conexão e manipulação do banco de dados
├─ generate_data.py    # Script para gerar dados de teste
├─ analyze_data.py     # Funções de análise de dados
├─ README.md           # Documentação
└─ requirements.txt    # Dependências do projeto

## Funcionalidades
- Dashboard interativo para explorar dados de vendas, restaurantes e clientes.
- Filtragem por período, canal de venda e restaurante.
- Visualização de métricas como:
  - Produtos mais vendidos
  - Total de vendas por restaurante
  - Tendências de vendas ao longo do tempo
- Comparação de períodos e detecção de padrões de consumo.
- Exportação de relatórios gerados (opcional).

## Hospedagem
O dashboard está hospedado no **Streamlit Cloud** e pode ser acessado diretamente sem precisar rodar localmente:

[https://nola-god-level-tv2ntguxhb9hql2gk9cnnr.streamlit.app/](https://nola-god-level-tv2ntguxhb9hql2gk9cnnr.streamlit.app/)


## Decisões Arquiteturais
- **Streamlit** foi escolhido por permitir dashboards interativos de forma rápida, sem necessidade de front-end complexo.
- **SQLite** foi usado para simplificar a execução local e evitar configuração de servidores.
- **Plotly** foi usado para gráficos interativos.
- O projeto é modularizado para separar a lógica de dados (`analyze_data.py`, `reports.py`), a interface (`app.py`) e a geração de dados (`generate_data.py`).

