from contextlib import asynccontextmanager
import asyncio
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from src.api import IdeabotAPI
from src.database import IdeabotDatabase
from src.listeners import ComponentsListener, MentionsListener
import logging
from src.commands import (
    FetchIdeas,
    RememberIdea,
    SearchIdeas,
    DumpIdeas,
    DeleteIdeas,
)
from src.bot import create_bot
from src.util import get_token
from uvicorn import Config, Server

logging.basicConfig(
    format="%(asctime)s,%(msecs)03d %(name)s %(levelname)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)
db = IdeabotDatabase()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Task to run before starting the app and after finishing."""
    bot = create_bot()
    logger.info("DB Created.")
    logger.info("Adding commands...")
    FetchIdeas(db, bot)
    RememberIdea(db, bot)
    SearchIdeas(db, bot)
    DumpIdeas(db, bot)
    DeleteIdeas(db, bot)
    logger.info("Commands imported.")
    logger.info("Creating bot.")
    logger.info("Creating DB.")
    logger.info("Adding listeners...")
    ComponentsListener(bot, db)
    MentionsListener(bot, db)
    logger.info("Listeners added.")
    logger.info("Starting bot")
    task = asyncio.create_task(bot.astart(token=get_token()))
    logger.info("Bot started")
    yield
    await bot.stop()
    task.cancel()


app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

api = IdeabotAPI(app=app, db=db)
api.setup_routers()
loop = asyncio.new_event_loop()
uvicorn_config = Config(
    app=app,
    loop=loop,  # ty:ignore[invalid-argument-type]
    host="0.0.0.0",
    port=12345,
)
logger.info("Starting bot up.")
server = Server(uvicorn_config)

logger.info("Starting server")
loop.run_until_complete(server.serve())
logger.info("Starting bot")
