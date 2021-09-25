import random
import string


def uuid():
    """
    영어 대문자+소문자 랜덤 생성
    """
    rand_str = ""
    str_length = 10

    for i in range(str_length):
        rand_str += str(random.choice(string.ascii_letters))

    return rand_str