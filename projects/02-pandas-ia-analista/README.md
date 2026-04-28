# 02 — Pandas IA Analista

> **Carreira Alura:** Base — *Pensamento computacional + Python IA Aplicada*

Faz EDA (análise exploratória) automática num CSV e usa LLM para gerar **insights narrativos** sobre os dados.

## Stack
| Camada | Tecnologia |
|--------|------------|
| Dados | `pandas` |
| Visualização | `matplotlib` |
| Insights | LLM via `_shared` |

## Como rodar

```bash
pip install -r requirements.txt
python main.py samples/vendas.csv --target receita
# ou rode com seu próprio CSV
python main.py /caminho/para/dados.csv
```

Saída: estatísticas (`describe`), gráficos em `out/`, e um relatório textual gerado pelo LLM com 5 insights e próximos passos.

## Entregáveis para portfólio
- Pipeline reutilizável de EDA → LLM
- Relatório textual em Markdown salvo em `out/relatorio.md`
- Geração de gráficos (histograma, correlação) automática

## Próximos passos
- Versão Streamlit interativa
- Sugerir feature engineering automático
