from fastapi import HTTPException, Request
from starlette.responses import RedirectResponse

async def not_found_error(request: Request, exc: HTTPException):
    return RedirectResponse('/404', status_code=303)

exception_handlers = {
    404: not_found_error
}
