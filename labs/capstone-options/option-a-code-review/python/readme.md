# AI Code Review Bot (Capstone Option A)

API FastAPI para revisao automatica de codigo com resposta estruturada, suporte a multiplas linguagens e integracao com webhook do GitHub.

## Endpoints

- `POST /review` - revisao de um snippet
- `POST /review/batch` - revisao de varios arquivos
- `POST /webhook/github` - recepcao de eventos de Pull Request
- `GET /health` - health check

## Variaveis de ambiente

Minimas para funcionar:

- `LLM_PROVIDER=anthropic|openai|google`
- `REVIEW_API_KEY=<sua-chave-para-endpoints-manuais>`
- `WEBHOOK_SECRET_KEY=<secret-do-webhook-github>`

Chaves por provider:

- Anthropic: `ANTHROPIC_API_KEY`
- OpenAI: `OPENAI_API_KEY`
- Google: `GOOGLE_API_KEY`

Opcionais:

- `LLM_TIMEOUT_SECONDS=30`
- `REVIEW_RATE_LIMIT_PER_MINUTE=20`
- `WEBHOOK_RATE_LIMIT_PER_MINUTE=30`
- `MAX_CODE_LENGTH=30000`
- `MAX_BATCH_FILES=20`
- `MAX_BATCH_TOTAL_LENGTH=120000`
- `ALLOWED_ORIGINS=*`

## Executando localmente

```bash
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

## Exemplo: /review

```bash
curl -X POST http://localhost:8000/review \
	-H "Content-Type: application/json" \
	-H "X-API-Key: $REVIEW_API_KEY" \
	-d '{
		"code": "def login(user, password):\n    query = f\"SELECT * FROM users WHERE user={user}\"\n    return db.execute(query)",
		"language": "python",
		"focus": ["security", "performance"]
	}'
```

## Exemplo: /review/batch

```bash
curl -X POST http://localhost:8000/review/batch \
	-H "Content-Type: application/json" \
	-H "X-API-Key: $REVIEW_API_KEY" \
	-d '{
		"focus": ["security"],
		"files": [
			{
				"path": "auth.py",
				"language": "python",
				"code": "def auth(u,p):\n    return True"
			},
			{
				"path": "index.js",
				"language": "javascript",
				"code": "const data = JSON.parse(userInput); eval(data.code);"
			}
		]
	}'
```

## Webhook GitHub

Configure o webhook do repositorio apontando para:

- `POST https://<seu-dominio>/webhook/github`

Eventos recomendados:

- `Pull requests`

A API valida `X-Hub-Signature-256` usando HMAC SHA-256 com `WEBHOOK_SECRET_KEY`.

Documentacao oficial GitHub:

- `https://docs.github.com/pt/webhooks/using-webhooks/validating-webhook-deliveries`

## Health check

```bash
curl http://localhost:8000/health
```