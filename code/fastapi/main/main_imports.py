import json
import redis

from time import gmtime, strftime, sleep, mktime, time
from typing import Optional, Dict, List, Union, Iterable
from fastapi import FastAPI, APIRouter, HTTPException
from fastapi.responses import HTMLResponse, PlainTextResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from main.redis_cache import RedisCache



