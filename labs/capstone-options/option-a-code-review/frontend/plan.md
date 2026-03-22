Let's modify this site with the following features

1) Light colors, white background and light green.
2) The API address is https://codereview-production-b0b5.up.railway.app/
3) Let's implement a screen with 2 tabs,
    3.1) Tab1 for simple review where the user can post code or upload a file and we show the content in the textarea
    3.2) Tab2 Batch Review where the client can select up to 2 files
    3.3) The system should show the structured information in "Example result" blocks
4) Let's create a multi-select list for the `focus` field
    4.1)  {"bug", "security", "performance", "style", "maintainability"}



Projeto atual que deve ser alterado
`labs/capstone-options/option-a-code-review/frontend/src`



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

Example result
```json
{"summary":"The code contains a critical SQL injection vulnerability and a major logical flaw where the password is completely ignored during the authentication process. It also lacks basic input sanitization and secure database interaction patterns.","issues":[{"severity":"critical","line":2,"category":"security","description":"SQL Injection vulnerability: User input is directly interpolated into the SQL string using f-strings.","suggestion":"Use parameterized queries (e.g., db.execute('SELECT * FROM users WHERE user=?', (user,))) to safely handle user input."},{"severity":"critical","line":1,"category":"security","description":"The 'password' parameter is accepted but never used in the query or validated, allowing any user to log in with any password.","suggestion":"Retrieve the hashed password from the database and use a secure comparison library like bcrypt or argon2 to verify the provided password."},{"severity":"high","line":2,"category":"bug","description":"SQL Syntax Error: The {user} variable in the f-string is not wrapped in quotes, which will cause a syntax error for string-based usernames.","suggestion":"Fix by using parameterized queries which handle quoting automatically."},{"severity":"medium","line":2,"category":"performance","description":"Use of 'SELECT *' is inefficient and can leak sensitive data (like password hashes) to the application layer if not needed.","suggestion":"Explicitly select only the columns required for the login logic (e.g., id, password_hash)."}],"suggestions":["Implement password hashing using a library like passlib or bcrypt; never store or compare passwords in plain text.","Add a 'LIMIT 1' to the SQL query to optimize database performance once the user is found.","Ensure the 'db' object and its connection are managed using a context manager or dependency injection to prevent resource leaks."],"metrics":{"overall_score":1,"complexity":"low","maintainability":"poor"}} 
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
