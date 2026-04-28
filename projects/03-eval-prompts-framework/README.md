# 03 — Eval Prompts Framework

> **Carreira Alura:** Base / Especialista em IA — *Engenharia de Prompts e avaliação*

Framework minimalista para A/B testing de prompts: você define variantes + casos de teste + critérios, ele roda no provedor configurado e gera um relatório comparativo (acurácia, custo, latência).

## Stack
| Camada | Tecnologia |
|--------|------------|
| Schema | `pydantic` |
| Execução | `_shared` LLM clients |
| Testes | `pytest` |
| Relatório | Markdown |

## Como rodar

```bash
pip install -r requirements.txt
python main.py suites/sentimento.yaml
pytest -q                      # roda os testes do framework
```

## Estrutura de uma suíte (`suites/sentimento.yaml`)

```yaml
name: sentimento_pt
prompts:
  - id: v1
    system: "Classifique como POSITIVO ou NEGATIVO."
  - id: v2
    system: "Você é um classificador. Devolva apenas POSITIVO ou NEGATIVO. Sem texto extra."
cases:
  - input: "Adorei o atendimento!"
    expected: "POSITIVO"
  - input: "Produto horrível, não recomendo."
    expected: "NEGATIVO"
```

## Entregáveis para portfólio
- Datamodel limpo com Pydantic
- Métricas: acerto exato, latência (ms), tokens (custo)
- Relatório Markdown comparativo
