import asyncio
from functools import partial
from typing import Any, Callable


async def create_awaitable(func: Callable, *args, **kwargs) -> Any:
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, partial(func, *args, **kwargs))
