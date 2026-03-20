# AI Code Review Bot (Capstone Option A)

FastAPI API for automated code review with structured responses, multi-language support, request logging, rate limiting, and GitHub webhook validation.

## Features

- Single-file review with structured JSON output
- Batch review for multiple files in one request
- Supported languages: Python, JavaScript, TypeScript, Java, Go, and Rust
- Optional review focus areas: bug, security, performance, style, and maintainability
- Structured issue output with severity, category, optional line number, description, and suggestion
- Request logging with latency and `X-Request-Id`
- In-memory rate limiting for review and webhook endpoints
- GitHub webhook signature validation and pull request event filtering
- Health check endpoint

## Endpoints

- `POST /review` - review a single code snippet
- `POST /review/batch` - review multiple files in one request
- `POST /webhook/github` - receive and validate GitHub Pull Request webhooks
- `GET /health` - health check and provider info

## Response Format

Both review endpoints return structured data in this shape:

```json
{
	"summary": "Short review summary",
	"issues": [
		{
			"severity": "critical",
			"line": 12,
			"category": "security",
			"description": "Unsanitized SQL query",
			"suggestion": "Use parameterized queries instead of string interpolation"
		}
	],
	"suggestions": [
		"Add input validation"
	],
	"metrics": {
		"overall_score": 6,
		"complexity": "medium",
		"maintainability": "fair"
	}
}
```

## Environment Variables

Minimum required configuration:

- `LLM_PROVIDER=anthropic|openai|google`

Provider-specific API keys:

- Anthropic: `ANTHROPIC_API_KEY`
- OpenAI: `OPENAI_API_KEY`
- Google: `GOOGLE_API_KEY`

Required for GitHub webhook signature validation:

- `WEBHOOK_SECRET_KEY=<github-webhook-secret>`

Optional configuration:

- `LLM_TIMEOUT_SECONDS=30`
- `REVIEW_RATE_LIMIT_PER_MINUTE=20`
- `WEBHOOK_RATE_LIMIT_PER_MINUTE=30`
- `MAX_CODE_LENGTH=30000`
- `MAX_BATCH_FILES=20`
- `MAX_BATCH_TOTAL_LENGTH=120000`
- `ALLOWED_ORIGINS=*`

## Running Locally

```bash
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

## Example: POST /review

```bash
curl -X POST http://localhost:8000/review \
	-H "Content-Type: application/json" \
	-d '{
		"code": "def login(user, password):\n    query = f\"SELECT * FROM users WHERE user={user}\"\n    return db.execute(query)",
		"language": "python",
		"focus": ["security", "performance"]
	}'
```

## Example: POST /review/batch

```bash
curl -X POST http://localhost:8000/review/batch \
	-H "Content-Type: application/json" \
	-d '{
		"focus": ["security"],
		"files": [
			{
				"path": "auth.py",
				"language": "python",
				"code": "def auth(u, p):\n    return True"
			},
			{
				"path": "index.js",
				"language": "javascript",
				"code": "const data = JSON.parse(userInput); eval(data.code);"
			}
		]
	}'
```

## Review Validation Rules

- `language` must be one of the supported languages
- `focus` items must be in the supported focus set
- `code` is limited by `MAX_CODE_LENGTH`
- batch requests are limited by `MAX_BATCH_FILES` and `MAX_BATCH_TOTAL_LENGTH`
- invalid model output returns a `502`
- upstream LLM provider failures return a `503`
- rate limit violations return a `429`

## GitHub Webhook

Configure the repository webhook to send requests to:

- `POST https://<your-domain>/webhook/github`

Recommended event:

- `Pull requests`

Current webhook behavior:

- validates `X-Hub-Signature-256` using HMAC SHA-256 and `WEBHOOK_SECRET_KEY`
- rejects duplicate deliveries using `X-GitHub-Delivery`
- rate-limits requests per repository
- accepts only the `pull_request` event
- accepts only these actions: `opened`, `reopened`, `synchronize`, `ready_for_review`, and `edited`
- validates that the payload includes a pull request number
- logs accepted webhook deliveries

Current limitation:

- the webhook does not yet post review comments back to GitHub; it currently validates and acknowledges supported pull request events

GitHub documentation:

- `https://docs.github.com/en/webhooks/using-webhooks/validating-webhook-deliveries`

## Health Check

```bash
curl http://localhost:8000/health
```

The response includes:

- service status
- active LLM provider
- supported languages

## Public Deployment Example

Base URL:

- `https://codereview-production-b0b5.up.railway.app/`

Example:

```bash
curl -X POST https://codereview-production-b0b5.up.railway.app/review \
	-H "Content-Type: application/json" \
	-d '{"code":"print(1)","language":"python"}'
```