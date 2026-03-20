"""Prompts for code review assistant."""

CODE_REVIEW_SYSTEM = """You are an expert code reviewer. Analyze code for:
1. Bugs and potential errors
2. Security vulnerabilities
3. Performance issues
4. Style and best practices
5. Maintainability concerns

Return only valid JSON that matches the requested schema.
Keep feedback specific, actionable, and concise."""

USER_REVIEW_PROMPT_TEMPLATE = """Review this {language} code:

```{language}
{code}
```

{focus_instruction}

Return JSON matching this schema:
{{
  "summary": "2-3 sentence overview",
  "issues": [
    {{
      "severity": "critical|high|medium|low",
      "category": "bug|security|performance|style|maintainability",
      "line": number or null,
      "description": "clear issue description",
      "suggestion": "specific fix suggestion"
    }}
  ],
  "suggestions": ["general improvement suggestions"],
  "metrics": {{
    "overall_score": 1-10,
    "complexity": "low|medium|high",
    "maintainability": "poor|fair|good|excellent"
  }}
}}"""

SECURITY_FOCUS_PROMPT = """Focus specifically on security vulnerabilities:
- SQL injection
- Command injection
- Path traversal
- Hardcoded secrets
- Input validation issues
- XSS vulnerabilities
- Authentication/authorization flaws
- Insecure cryptography"""

PERFORMANCE_FOCUS_PROMPT = """Focus specifically on performance:
- Algorithm complexity (Big O)
- Memory usage and leaks
- Unnecessary loops or iterations
- Caching opportunities
- Database query optimization
- Async/await patterns
- Resource management"""

def build_focus_instruction(focus: list[str] | None) -> str:
    """Build focus section for review prompts."""
    if not focus:
        return ""

    normalized = [item.strip().lower() for item in focus if item and item.strip()]
    if not normalized:
        return ""

    details: list[str] = [f"Prioritize review focus on: {', '.join(normalized)}."]
    if "security" in normalized:
        details.append(SECURITY_FOCUS_PROMPT)
    if "performance" in normalized:
        details.append(PERFORMANCE_FOCUS_PROMPT)

    return "\n\n".join(details)
