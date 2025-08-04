from fastapi import FastAPI
from project.routes.heroes import heroes_router


app = FastAPI(title="Master Slave architecture")


@app.get("/healthy")
def healthcheck() -> bool:
    return True


app.include_router(heroes_router)
