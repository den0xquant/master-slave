from fastapi import FastAPI
from project.routes.heroes import heroes_router


app = FastAPI(title="Master Slave architecture")
app.include_router(heroes_router)
