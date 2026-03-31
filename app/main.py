from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from strawberry.fastapi import GraphQLRouter
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.graphql.query import Query
from app.graphql.mutation import Mutation

import strawberry

schema = strawberry.Schema(query=Query, mutation=Mutation)

def get_context(db: Session = Depends(get_db)):
    return {"db": db}

graphql_app = GraphQLRouter(schema, context_getter=get_context, allow_origins=["*"])  # Allow all origins for GraphQL

app = FastAPI()

app.include_router(graphql_app, prefix="/graphql")