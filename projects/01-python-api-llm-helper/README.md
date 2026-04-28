# 01 — Python API LLM Helper

> **Carreira Alura:** Base — *Python: Inteligência Artificial Aplicada*

CLI em Python que recebe uma tarefa textual (resumir, traduzir, gerar código) e roteia para o provedor LLM configurado (OpenAI, Gemini, Anthropic ou mock offline).

## Stack
| Camada | Tecnologia |
|--------|------------|
| CLI | `typer` |
| LLM | `openai` / `google-generativeai` / `anthropic` (auto-detect) |
| Utils | `projects/_shared` |

## Como rodar

```bash
pip install -r requirements.txt
python main.py resumir "texto longo aqui ..."
python main.py traduzir "Hello world" --idioma "português"
python main.py codigo "função fibonacci em python recursiva"
```

Sem API key, cai automaticamente no `MockLLMClient` (resposta determinística para smoke test).

## Entregáveis para portfólio
- CLI funcional com 3 comandos
- Auto-detecção de provedor (resiliente a falta de chaves)
- Padrão de wrapping multi-provider que se repete nos demais projetos

## Próximos passos
- Adicionar comando `chat` interativo
- Salvar histórico em SQLite
- Modo streaming (`--stream`)
