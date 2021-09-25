from fastapi import HTTPException


class DuplicatedEntryError(HTTPException):
    def __init__(self, message: str):
        super().__init__(status_code=422, detail=message)


class CommonException(Exception):
    ...


class CommonNotFoundError(CommonException):
    def __init__(self):
        self.status_code = 404
        self.detail = "Not Found"


class CommonExistError(CommonException):
    def __init__(self):
        self.status_code = 409
        self.detail = "Already Exists"