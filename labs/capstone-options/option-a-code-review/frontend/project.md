Let's create a SPA frontend in Next.js where the user can post source code and the backend will analyze it, displaying the results in blocks of information.

The API address is https://lab02analyzer-production.up.railway.app/analyze

The physical address of the project will be: /mnt/dados/projetos/taller/ai_training/labs/lab02-code-analyzer-agent/frontend

Color scheme: #012340
#025939
#027333
#03A63C
#04D939

All text on the page must be in American English.

Post example: 
```json
{     "code": "def add(a,b):\n    return a+b\n\ndef process(data):\n    result[]\n    for i in range(len(data)):\n        if data[i]>0:\n            result.append(data[i]*2)\n    return result",     "language": "python"   }
```

Result example:
```json
{
	"summary": "The code defines a simple addition utility and a data processing function that filters and transforms a list. However, it contains a critical syntax error in the initialization of a list and uses non-Pythonic iteration patterns.",
	"issues": [
		{
			"severity": "critical",
			"line": 5,
			"category": "bug",
			"description": "The statement 'result[]' is a syntax error. It appears to be an attempt to initialize an empty list without using the assignment operator.",
			"suggestion": "Change 'result[]' to 'result = []'."
		},
		{
			"severity": "low",
			"line": 6,
			"category": "maintainability",
			"description": "Using 'for i in range(len(data))' to iterate over a list is considered un-Pythonic when the index is only used to access the element.",
			"suggestion": "Iterate directly over the data using 'for value in data:' or use a list comprehension."
		},
		{
			"severity": "low",
			"line": 1,
			"category": "style",
			"description": "Missing whitespace around operators and after commas per PEP 8 guidelines.",
			"suggestion": "Change 'add(a,b)' to 'add(a, b)' and 'a+b' to 'a + b'."
		}
	],
	"suggestions": [
		"Use a list comprehension in the 'process' function for better readability and performance: [val * 2 for val in data if val > 0].",
		"Add type hints to function signatures (e.g., 'def add(a: int, b: int) -> int:') to improve IDE support and maintainability.",
		"Include docstrings for functions to explain their purpose and expected input types."
	],
	"metrics": {
		"complexity": "low",
		"readability": "fair",
		"test_coverage_estimate": "none"
	}
}
```