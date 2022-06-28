from dotenv import load_dotenv
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from app.constants import ALLOWED_HOSTS, PROJECT_NAME, API_PREFIX
from app.api.routes.api import router as api_router
from app.api.dependencies.authentication import current_user

load_dotenv()


def get_application() -> FastAPI:
    app = FastAPI(title=PROJECT_NAME, dependencies=[Depends(current_user)], debug=True)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=ALLOWED_HOSTS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(api_router, prefix=API_PREFIX)
    return app


app = get_application()
