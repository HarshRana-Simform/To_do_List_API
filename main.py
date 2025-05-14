from fastapi import FastAPI
from To_do_app.router import todo_routes, user_routes, authentication_routes

# Endpoint	        Method	Description
# /todos	        Get	    Read all todo
# /create_todo      POST	Create a todo
# /todo/{todo_id}	GET	    Get a todo by id
# /todo/{todo_id}	PATCH	Update a todo by id
# /todo/{todo_id}	DELETE	Delete a todo by id


app = FastAPI(
    title='TO-DO List',
    description='A set of RESTful APIs for a To-Do list web service',
)

app.include_router(authentication_routes.router,
                   prefix="/auth", tags=["Authentication"])

app.include_router(user_routes.router, prefix="/api", tags=["User Endpoints"])

app.include_router(todo_routes.router, prefix="/api", tags=["To-Do Endpoints"])
