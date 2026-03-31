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

graphql_app = GraphQLRouter(schema, context_getter=get_context)

app = FastAPI()

# Allow CORS
origins = [
    "https://customer-app-frontend-5ajwvtv60-boomingwork-9487s-projects.vercel.app/",  # Vite frontend
    # You can add other origins later if needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # GET, POST, PUT, DELETE, etc.
    allow_headers=["*"],
)

app.include_router(graphql_app, prefix="/graphql")