from fastapi import FastAPI, Depends, Response
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

graphql_app = GraphQLRouter(
    schema,
    context_getter=get_context
)

app = FastAPI()

# ✅ CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Handle OPTIONS preflight synchronously
@app.api_route("/graphql", methods=["OPTIONS"])
def graphql_preflight():
    return Response(status_code=200)

# ✅ Include GraphQL router
app.include_router(graphql_app, prefix="/graphql")