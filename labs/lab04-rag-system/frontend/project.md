# RAG frontend

Let's create a frontend in Next.js with two routes: one to index files and another to query them.

On the indexing page, we'll create a form where the user can add up to two source code files, and the backend will index the submitted files.

Ideally, the client could manually add the file name and content to a text area or upload a file from their computer. In that case, the system should read the file content and display it in a text area.

On the query page, the user can ask questions about the indexed files in a chat-like format, so the layout should present it in a conversational format, similar to a text chat. Therefore, in the return payload, we will show the content of the "answer" field, and below the answer, we will add small icons so the user can see additional information: one icon for "sources" and one for "context_used".

The API address are 
Index files: https://lab4rag-production.up.railway.app/index/files
Query: https://lab4rag-production.up.railway.app/query

The physical address of the project will be: /mnt/dados/projetos/taller/ai_training/labs/lab04-rag-system/frontend

Color scheme: 
#049DBF
#8C4F04
#D99036
#8C6542
#0D0D0D

**All text on the page must be in American English.**

## Index files 
Post example: 
```json
{
    "files": {
      "auth.py": "def login(user, password):\n    # Validate credentials\n    return token",
      "api.py": "def get_users():\n    return db.query(User).all()"
    }
  }
```

Result example:
```json
{
	"indexed_chunks": 2,
	"files": [
		"auth.py",
		"api.py"
	]
}
```
## Query 
Post example: 
```json
{"question": "How does login work?"}
```

Result example:
```json
{
	"answer": "Based on the provided code context, the `login` function works as follows:\n\nThe `login` function is defined in **auth.py** (Lines 1-3). It takes two parameters, `user` and `password` (Line 1). Inside the function, it is intended to \"Validate credentials\" (Line 2) and then returns a `token` (Line 3). \n\nThe specific implementation details for how the credentials are validated are not provided in the snippet, as Line 2 is a comment.",
	"sources": [
		{
			"file": "api.py",
			"type": "function",
			"name": "get_users",
			"line": 1,
			"relevance": 0.0
		},
		{
			"file": "auth.py",
			"type": "function",
			"name": "login",
			"line": 1,
			"relevance": 0.0
		}
	],
	"context_used": "--- File: api.py | function: get_users | Line: 1 ---\ndef get_users():\n    return db.query(User).all()\n\n--- File: auth.py | function: login | Line: 1 ---\ndef login(user, password):\n    # Validate credentials\n    return token"
}
```




