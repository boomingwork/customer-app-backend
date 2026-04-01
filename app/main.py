from fastapi import FastAPI, Depends, Response
from fastapi.middleware.cors import CORSMiddleware
from strawberry.fastapi import GraphQLRouter
from sqlalchemy.orm import Session
import strawberry

from app.db.session import get_db
from app.graphql.query import Query
from app.graphql.mutation import Mutation


schema = strawberry.Schema(query=Query, mutation=Mutation)


def get_context(db: Session = Depends(get_db)):
    return {"db": db}


graphql_app = GraphQLRouter(schema, context_getter=get_context)

app = FastAPI()

# Allow CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://customer-app-frontend-tau.vercel.app",
        "https://customer-app-frontend-boomingwork-9487s-projects.vercel.app",
        "https://customer-app-frontend-git-master-boomingwork-9487s-projects.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global preflight handler
@app.options("/{full_path:path}")
def preflight_handler(full_path: str):
    return Response(status_code=200)


app.include_router(graphql_app, prefix="/graphql")