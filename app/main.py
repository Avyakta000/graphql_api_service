from fastapi import FastAPI, Request
from strawberry.fastapi import GraphQLRouter
from app.graphql.schema import schema

# function to add the request to the context
async def get_context(request: Request):
    return {"request": request}

# graphQL route with the custom context getter
graphql_app = GraphQLRouter(schema, context_getter=get_context)

app = FastAPI()

# graphQL route
app.include_router(graphql_app, prefix="/graphql")

@app.get("/")
async def root():
    return {"message": "GraphQL server is running"}

