import json
import redis
import asyncio
import telnetlib

from time import gmtime, strftime, sleep, mktime, time
from typing import Optional, Dict, List, Union, Iterable
from fastapi import FastAPI, APIRouter, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, PlainTextResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from modules.core.classes.core_redis import CoreRedis



