from fastapi import FastAPI
from To_do_app.router.todo_routes import router

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


app.include_router(router, prefix="/api", tags=["To-Do Endpoints"])
