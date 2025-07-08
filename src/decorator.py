from functools import wraps
import asyncio
from typing import TypeVar, Callable, Any, Optional
from loguru import logger
from .config import get_config

T = TypeVar("T")



def retry_async(
    attempts: int = None,
    delay: float = 1.0,
    backoff: float = 2.0,
    return_on_fail: Any = None
):
    """
    Async retry decorator with exponential backoff.
    If attempts are not provided, please use SETTINGS.ATTEMPTS from config.
    """
    def decorator(func: Callable[..., T]) ->  Callable[..., Optional[T]]:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Get attempts from config if not provided
            retry_attempts = attempts if attempts is not None else get_config()['SETTINGS']['ATTEMPTS']
            current_delay = delay
            proxy_identifier = kwargs.get('proxy', '')

            for attempt in range(0, retry_attempts+1):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    if attempt < retry_attempts :  # Don't sleep on the last attempt
                        logger.warning(
                            f"Proxy: {proxy_identifier}\n"
                            f"Attempt {attempt+1}/{retry_attempts} failed for {func.__name__}: {str(e)}. "
                            f"Retrying in {current_delay:.1f} seconds..."
                        )
                        await asyncio.sleep(current_delay)
                        current_delay *= backoff
                    else:
                        raise e


            return return_on_fail

        return wrapper

    return decorator


