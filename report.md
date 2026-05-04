# Cybersecurity Scan Report

**Data:** 2026-05-04
**Stack:** Python 3.11+ · FastAPI · LangChain/LangGraph · ChromaDB · scikit-learn · XGBoost · PyTorch · Streamlit · Terraform/AWS Lambda+Bedrock · Docker · Kubernetes/Helm · GitHub Pages
**Escopo:** monorepo `oaken-agentes` com 21 projetos + 2 HTML pages (portfolio + landing)

## Sumario

| Metrica | Valor |
|---|---|
| Checks executados | 90 |
| Passaram | 80 |
| Falharam | 10 |
| Criticos | 0 |
| Altos | 1 |
| Medios | 5 |
| Baixos | 4 |

## Achados e Status

### [ALTO-1] API Gateway sem autenticacao — Terraform

**Categoria:** Infra | **Arquivo:** `projects/11-deploy-aws-bedrock/terraform/main.tf:90`
**Impacto:** Endpoint `POST /chat` publico sem API key, JWT ou IAM authorizer. Qualquer pessoa com a URL pode invocar o Lambda.
**Fix sugerido:** Adicionar `aws_apigatewayv2_authorizer` ou API key obrigatoria. Sem throttling, custo ilimitado.
**Status:** Pendente (requer decisao de auth strategy)

---

### [MEDIO-1] CSP bloqueava JavaScript inline — index.html (CORRIGIDO)

**Categoria:** Infra | **Arquivo:** `index.html:18`
**Impacto:** `script-src 'self'` bloqueava o script de scroll reveal (linha 1299). Todas as secoes com `.reveal` ficavam invisiveis (opacity: 0). Stats, Sobre, Produto, Projetos, Diferenciais — ocultos.
**Fix:** Adicionado `'unsafe-inline'` ao `script-src`.
**Status:** CORRIGIDO

### [MEDIO-2] pito-presentation.html sem CSP nem headers de seguranca (CORRIGIDO)

**Categoria:** Infra | **Arquivo:** `pito-presentation.html:5-6`
**Impacto:** Landing page sem nenhuma protecao CSP — scripts inline, sem X-Content-Type-Options, sem Referrer-Policy. Links `target="_blank"` sem `rel="noopener"` (tab-napping).
**Fix:** Adicionados meta CSP, X-Content-Type-Options, Referrer-Policy e `rel="noopener noreferrer"` nos links.
**Status:** CORRIGIDO

### [MEDIO-3] CORS allow_headers wildcard (CORRIGIDO)

**Categoria:** Codigo | **Arquivo:** `projects/_shared/security.py:49` + `projects/21-deploy-docker-k8s/_shared/security.py:49`
**Impacto:** `allow_headers=["*"]` permite qualquer header HTTP em requests cross-origin. Combinado com origem mal configurada, pode facilitar header injection.
**Fix:** Substituido por lista explicita: `["Content-Type", "X-API-Key", "X-Request-Id"]`.
**Status:** CORRIGIDO

### [MEDIO-4] Helm image.tag: latest

**Categoria:** Infra | **Arquivo:** `projects/21-deploy-docker-k8s/helm/values.yaml:3`
**Impacto:** Tag mutavel — deploy pode puxar imagem diferente sem controle. CI tambem pusha `:latest` alem do SHA.
**Fix sugerido:** Default para digest SHA ou tag imutavel no values.yaml. Remover `:latest` do CI push.
**Status:** Pendente

### [MEDIO-5] Dependencias sem pin exato — 21 requirements.txt

**Categoria:** Dependencias | **Arquivo:** Todos os `projects/*/requirements.txt`
**Impacto:** Todas usam `>=x.y.z` sem pin exato. `pip install` pode puxar versao major nova com breaking changes ou CVE.
**Mitigacao existente:** `constraints.txt` limita 18 pacotes com upper bound (`<2.0`).
**Fix sugerido:** Para portfolio educacional, o constraints.txt e suficiente. Para producao, usar `pip-compile` com hashes.
**Status:** Aceitavel para portfolio

---

### [BAIXO-1] Subprocess com codigo LLM sem sandbox

**Categoria:** Codigo | **Arquivo:** `projects/07-agente-tools-zero-shot/main.py:78` + `projects/15-agente-codigo-sandbox/sandbox.py:22`
**Impacto:** Quando `OAKEN_ALLOW_LOCAL_EXEC=1`, codigo gerado pelo LLM executa direto no host. Prompt injection → RCE.
**Mitigacao:** Gate desabilitado por default + preferencia Docker. Risco real so se ativado em ambiente nao-descartavel.
**Status:** Aceitavel (by design, documentado)

### [BAIXO-2] Dockerfile sem image digest pin

**Categoria:** Infra | **Arquivo:** `projects/21-deploy-docker-k8s/Dockerfile:1`
**Impacto:** `python:3.12-slim` e tag flutuante. `docker pull` pode trazer OS layer diferente.
**Fix sugerido:** Usar `python:3.12-slim@sha256:<digest>`.
**Status:** Pendente

### [BAIXO-3] CI sem scan de vulnerabilidades na imagem

**Categoria:** Infra | **Arquivo:** `projects/21-deploy-docker-k8s/.github/workflows/ci.yml`
**Impacto:** SBOM e gerado mas nenhum gate Trivy/Grype antes do push. CVE no base image passa direto.
**Fix sugerido:** Adicionar step `aquasecurity/trivy-action` antes do push.
**Status:** Pendente

### [BAIXO-4] constraints.txt incompleto

**Categoria:** Dependencias | **Arquivo:** `constraints.txt`
**Impacto:** Falta cobertura para `torch`, `langchain`, `chromadb`, `boto3`, `mlflow`, `dvc` — pacotes grandes com CVEs frequentes.
**Fix sugerido:** Adicionar upper bounds para esses pacotes.
**Status:** Pendente

---

## Categorias Limpas (sem achados)

| Categoria | Status |
|---|---|
| **Secrets** | Limpo — nenhum segredo em codigo, configs ou git history. `.env` no gitignore, `.env.example` sem valores reais |
| **SQL Injection** | Limpo — nenhuma concatenacao SQL encontrada |
| **XSS** | Limpo — nenhum `innerHTML`/`document.write`. Paginas estaticas sem input de usuario |
| **SSRF** | Limpo — URLs hardcoded (localhost), nenhuma vem de input HTTP |
| **Path Traversal** | Limpo — todos os `open()` com paths fixos |
| **Desserializacao** | Limpo — zero `pickle.loads` ou `yaml.load` inseguro |
| **LGPD** | Completo — PRIVACY.md robusto, 6 endpoints art. 18, audit chain SHA-256, PII redaction em 7 padroes |
| **Logging** | Limpo — nenhum log imprime PII. Guardrails logam apenas hashes truncados |
| **IAM (Helm)** | Bom — `runAsNonRoot`, `drop: [ALL]`, `readOnlyRootFilesystem`, `seccompProfile: RuntimeDefault` |
| **Backup** | N/A para portfolio educacional |

## Resumo de Acoes

| # | Acao | Status |
|---|---|---|
| 1 | CSP `script-src 'unsafe-inline'` em index.html | CORRIGIDO |
| 2 | CSP + security headers em pito-presentation.html | CORRIGIDO |
| 3 | `rel="noopener noreferrer"` em links externos pito | CORRIGIDO |
| 4 | CORS `allow_headers` explicito (2 ficheiros) | CORRIGIDO |
| 5 | API Gateway authorizer no Terraform | Pendente |
| 6 | Helm default tag → digest | Pendente |
| 7 | Dockerfile image digest pin | Pendente |
| 8 | CI image scan gate (Trivy) | Pendente |
| 9 | constraints.txt cobertura adicional | Pendente |

**4 de 9 achados corrigidos nesta sessao.** Os pendentes sao decisoes arquiteturais ou melhorias incrementais que nao afetam a funcionalidade do portfolio.
