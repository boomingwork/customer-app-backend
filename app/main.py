from fastapi import FastAPI, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from strawberry.fastapi import GraphQLRouter
import strawberry
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.graphql.query import Query
from app.graphql.mutation import Mutation

schema = strawberry.Schema(query=Query, mutation=Mutation)

def get_context(db: Session = Depends(get_db)):
    return {"db": db}

graphql_app = GraphQLRouter(schema, context_getter=get_context)

ALLOWED_ORIGIN = "https://customer-app-frontend-tau.vercel.app"

# ✅ Add OPTIONS directly onto the GraphQL router itself, before mounting
@graphql_app.options("/")
async def graphql_preflight(request: Request):
    return JSONResponse(
        content="OK",
        status_code=200,
        headers={
            "Access-Control-Allow-Origin": ALLOWED_ORIGIN,
            "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Credentials": "true",
            "Access-Control-Max-Age": "3600",
        },
    )

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[ALLOWED_ORIGIN],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Include AFTER the OPTIONS route is registered on graphql_app
app.include_router(graphql_app, prefix="/graphql")