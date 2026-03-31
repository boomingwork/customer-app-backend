from fastapi import FastAPI, Response, Depends
from fastapi.middleware.cors import CORSMiddleware
from strawberry.fastapi import GraphQLRouter
import strawberry
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.graphql.query import Query
from app.graphql.mutation import Mutation

# --- GraphQL schema ---
schema = strawberry.Schema(query=Query, mutation=Mutation)

def get_context(db: Session = Depends(get_db)):
    return {"db": db}

graphql_app = GraphQLRouter(schema, context_getter=get_context)

app = FastAPI()

# ✅ CORS middleware allows your Vercel frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://customer-app-frontend-tau.vercel.app"],  # production frontend
    allow_credentials=True,
    allow_methods=["*"],  # includes OPTIONS, POST, GET
    allow_headers=["*"],
)

# ✅ Include GraphQL router
app.include_router(graphql_app, prefix="/graphql")