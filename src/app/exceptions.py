
class StatusCode:
    HTTP_500 = 500
    HTTP_400 = 400
    HTTP_401 = 401
    HTTP_403 = 403
    HTTP_404 = 404
    HTTP_405 = 405


class APIException(Exception):
    status_code: int
    code: str
    msg: str
    detail: str
    ex: Exception

    def __init__(
        self,
        *,
        status_code: int = StatusCode.HTTP_500,
        code: str = "000000",
        msg: str = None,
        detail: str = None,
        ex: Exception = None,
    ):
        self.status_code = status_code
        self.code = code
        self.msg = msg
        self.detail = detail
        self.ex = ex
        super().__init__(ex)


class NotFoundVoteEx(APIException):
    def __init__(self, vote_id: int = None, ex: Exception = None):
        super().__init__(
            status_code=StatusCode.HTTP_404,
            msg=f"해당 투표를 찾을 수 없습니다.",
            detail=f"Not Found Vote ID : {vote_id}",
            code=f"{StatusCode.HTTP_400}{'1'.zfill(4)}",
            ex=ex,
        )