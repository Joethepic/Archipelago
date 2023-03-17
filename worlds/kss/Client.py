import logging
import asyncio
import time

from NetUtils import ClientStatus, color
from worlds.AutoSNIClient import SNIClient

snes_logger = logging.getLogger("SNES")
# Rom data for client

# Client data 
class KSSSNIClient(SNIClient):
    game = "Kirby Super Star"