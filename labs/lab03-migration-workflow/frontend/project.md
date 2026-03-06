Let's create a frontend SPA in Next.js where the user can add up to 2 source code files, and the backend will perform the migration, displaying the results in information blocks.

- Ideally, the client would be able to manually add the file name and content to a text area or upload a file from their local machine. In that case, the system should read the file content and display it in a text area.

The API address is https://migration-workflow-production.up.railway.app/migrate

The physical address of the project will be: /mnt/dados/projetos/taller/ai_training/labs/lab03-migration-workflow/frontend

Color scheme: #012340
#3C36D9
#343BBF
#142273
#011140
#43D9CA

All text on the page must be in American English.

Post example: 
```json
{   
	"source_framework": "express",     
	"target_framework": "fastapi",     
	"files": {       
		"routes/users.js": "const express  require('express');\nconst router = express.Router();\n\nrouter.get('/users', async (req, res) => {\n    const users = await db.getUsers();\n    res.json(users);\n});\n\nmodule.exports = router;"     
		}   
}
```

Result example:
```json
{
	"success": true,
	"migrated_files": {
		"routers/users.py": "from fastapi import APIRouter, Depends\nfrom typing import List\nfrom pydantic import BaseModel\n\n# --- Step 1: Pydantic Model (Schema) ---\nclass UserSchema(BaseModel):\n    id: int\n    username: str\n    email: str\n\n    class Config:\n        from_attributes = True\n\n# --- Step 2: Mock Database Layer (Logic from Step 2) ---\n# In a real app, this would be in a separate db.py file using SQLAlchemy/Motor\nasync def get_db_users():\n    # Simulated DB call\n    return [{\"id\": 1, \"username\": \"jdoe\", \"email\": \"jdoe@example.com\"}]\n\n# --- Step 3: Initialize FastAPI Router ---\nrouter = APIRouter(\n    prefix=\"/users\",\n    tags=[\"users\"]\n)\n\n# --- Step 4: Migrate GET /users Route ---\n@router.get(\"/\", response_model=List[UserSchema])\nasync def read_users():\n    \"\"\"\n    Fetch all users from the database.\n    FastAPI automatically handles JSON serialization via the response_model.\n    \"\"\"\n    users = await get_db_users()\n    return users"
	},
	"plan_executed": [
		{
			"id": 1,
			"description": "Define Pydantic Schemas: Create a 'User' model in Python using Pydantic to replace the loose JSON structure in Express. This handles the 'Data Validation and Typing' challenge and ensures automatic documentation.",
			"status": "completed"
		},
		{
			"id": 2,
			"description": "Implement Database Access Layer: Rewrite the 'db.getUsers' logic using a Python ORM or driver (e.g., SQLAlchemy, Tortoise, or Motor). This addresses the 'Database Layer Compatibility' challenge by providing an asynchronous function to fetch data.",
			"status": "completed"
		},
		{
			"id": 3,
			"description": "Initialize FastAPI Router: Create a new Python file (e.g., 'app/routers/users.py') and initialize a FastAPI 'APIRouter' instance. This replaces the 'express.Router()' modularity pattern.",
			"status": "completed"
		},
		{
			"id": 4,
			"description": "Migrate GET /users Route: Implement the GET endpoint within the new APIRouter. Use 'async def', call the new database function from Step 2, and return the Pydantic models from Step 1. This removes the need for 'res.json()' as FastAPI handles serialization automatically.",
			"status": "completed"
		},
		{
			"id": 5,
			"description": "Configure Main Application: Create the main FastAPI entry point (e.g., 'main.py'), include the users router using 'app.include_router()', and implement global exception handlers to replace the manual error catching logic used in the Express version.",
			"status": "completed"
		}
	],
	"verification": {
		"files_migrated": 1,
		"steps_completed": 5,
		"issues": [],
		"validations": [
			{
				"file": "routers/users.py",
				"valid": true,
				"issues": [
					{
						"line": 1,
						"issue": "The 'Depends' class is imported from 'fastapi' but is never used in the provided code.",
						"suggestion": "Remove 'Depends' from the import statement to keep the code clean if it is not intended for future use in this snippet."
					}
				]
			}
		]
	},
	"errors": []
}
```