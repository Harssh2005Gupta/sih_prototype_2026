import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from satquery.config import API_TITLE, API_VERSION, SAMPLES_DIR, API_HOST, API_PORT
from satquery.data.sample_generator import generate_sample_tiles
from satquery.backend.routes import router

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("satquery.api")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting SatQuery AI Backend...")
    # Pre-generate sample tiles if absent
    if not SAMPLES_DIR.exists() or len(list(SAMPLES_DIR.glob("*.npy"))) == 0:
        logger.info("Initializing sample multispectral satellite tiles...")
        generate_sample_tiles(SAMPLES_DIR)
    yield
    logger.info("Shutting down SatQuery AI Backend...")


app = FastAPI(
    title=API_TITLE,
    version=API_VERSION,
    description="Earth Observation Multimodal VLM & AI Agent Framework for Multispectral Sentinel-2 Querying",
    lifespan=lifespan,
)

# Enable CORS for frontend clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("satquery.backend.main:app", host=API_HOST, port=API_PORT, reload=True)
