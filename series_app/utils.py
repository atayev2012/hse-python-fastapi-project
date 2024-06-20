from fastapi import HTTPException
from typing import Any


def raise_http_exception(
        status_code: int,
        error: Any | None,
        error_data: Any = None
):
    raise HTTPException(
        status_code=status_code,
        detail={
            "status": "fail",
            "message": f"{type(error).__name__}: {error.args}",
            "data": error_data
        }
    )
