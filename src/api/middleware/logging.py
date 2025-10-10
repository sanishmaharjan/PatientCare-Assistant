"""
Custom middleware for the API.
"""

import time
from fastapi import Request
from ..utils import get_logger

logger = get_logger()


async def get_request_body(request: Request) -> str:
    """Safely extract request body for logging purposes."""
    try:
        body = await request.body()
        body_str = body.decode('utf-8')
        # Truncate if too long
        if len(body_str) > 200:
            body_str = body_str[:197] + '...'
        return body_str
    except Exception as e:
        return f"<Error reading body: {str(e)}>"


async def log_requests(request: Request, call_next):
    """Middleware to log all requests and responses."""
    request_id = f"{id(request)}"
    start_time = time.time()
    
    # Log the incoming request with body for debugging
    if request.method in ["POST", "PUT", "PATCH"]:
        body = await get_request_body(request)
        logger.info(f"Request [{request_id}] - {request.method} {request.url.path} - Started - Body: {body}")
        # Reset the request body position for further processing
        await request.body()
    else:
        logger.info(f"Request [{request_id}] - {request.method} {request.url.path} - Started")
    
    # Process the request
    try:
        response = await call_next(request)
        process_time = time.time() - start_time
        
        # Log the response with timing information
        logger.info(f"Request [{request_id}] - {request.method} {request.url.path} - "
                    f"Completed with status {response.status_code} in {process_time:.4f}s")
        
        return response
    except Exception as e:
        process_time = time.time() - start_time
        logger.error(f"Request [{request_id}] - {request.method} {request.url.path} - "
                    f"Failed after {process_time:.4f}s: {str(e)}")
        # Log the stack trace for server errors
        import traceback
        logger.error(f"Exception traceback: {traceback.format_exc()}")
        raise
