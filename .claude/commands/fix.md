---
description: Patch cirúrgico de bug específico, sem refator extra. Uso: /fix <bug-id ou descrição>
---

# /fix — Correção Cirúrgica

Corrija **apenas** o bug informado em `$ARGUMENTS`. Patch mínimo e seguro.

## Regras inegociáveis

1. **Não refatore nada fora do escopo.** Se ver outro problema, anote no fim — não corrija agora.
2. **Mostre diff exato** (antes / depois) com `file:line` clicável.
3. **Explique o risco eliminado** em 1 linha (qual regra R1–R20 viola).
4. **Forneça 1 comando de teste** que valida o fix (curl, pytest, grep).
5. **Aguarde confirmação** antes de avançar ao próximo bug.

## Avisos automáticos

- Se o fix impactar `_shared/`, avise: "⚠️  Afeta TODOS os projetos do portfólio. Confirme antes de aplicar."
- Se o fix exigir migração de schema/dados, avise: "⚠️  Migração necessária. Rollback plan?"
- Se o fix mudar comportamento público (API/contrato), avise: "⚠️  Breaking change. Versionar."

## Formato de Saída

```
🎯 Bug: <descrição em 1 linha>
📍 Localização: <file>:<line>
⚠️  Regra violada: R<N> — <nome curto>

--- ANTES ---
<código original — só as linhas que mudam, ±2 de contexto>

--- DEPOIS ---
<código corrigido>

🛡️  Risco eliminado: <1 frase>
🧪 Teste: <comando único>
📋 Próximo: <próximo bug ou "aguardando aprovação">
```

## Anti-padrões proibidos no fix

- ❌ Adicionar testes que ainda não existem (sugira `/smoke` separado)
- ❌ Mudar formatação (linha em branco, indentação) fora do bug
- ❌ Renomear variáveis "para clareza"
- ❌ Atualizar dependências (sugira PR separado)
- ❌ Mudar comentários ou docstrings não-relacionados

**Se o bug não puder ser corrigido cirurgicamente** (precisa refactor amplo), diga isso e proponha um plano em vez de aplicar patch ruim.
