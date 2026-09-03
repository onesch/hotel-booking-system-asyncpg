from fastapi import HTTPException


class ConflictException(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=409, detail=detail)


class NotFoundException(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=404, detail=detail)


class InvalidTypeException(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=400,detail=detail)
