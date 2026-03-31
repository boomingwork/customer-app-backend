from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
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

# --- GraphQL router ---
graphql_app = GraphQLRouter(
    schema,
    context_getter=get_context
)

# --- FastAPI app ---
app = FastAPI()

# ✅ CORS middleware must be BEFORE router
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or your frontend URL for production
    allow_credentials=True,
    allow_methods=["*"],   # OPTIONS, GET, POST, PUT, DELETE
    allow_headers=["*"],
)

# ✅ Include router
app.include_router(graphql_app, prefix="/graphql")