from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from strawberry.fastapi import GraphQLRouter
import strawberry

from app.db.session import get_db
from app.graphql.query import Query
from app.graphql.mutation import Mutation

# --- GraphQL schema ---
schema = strawberry.Schema(query=Query, mutation=Mutation)

def get_context(db: Session = Depends(get_db)):
    return {"db": db}

# --- GraphQL router with CORS handled ---
graphql_app = GraphQLRouter(
    schema,
    context_getter=get_context,
    allow_origin=[
        "https://customer-app-frontend-5ajwvtv60-boomingwork-9487s-projects.vercel.app"
    ],
)

# --- FastAPI app ---
app = FastAPI()
app.include_router(graphql_app, prefix="/graphql")