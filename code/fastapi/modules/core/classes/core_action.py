from main.main_imports import *

class CoreAction:

  # core actions
  async def DelayMs(self, data):
    await asyncio.sleep(int(data['time_ms'])/1000)
    return { 'slept' : data['time_ms'] }



