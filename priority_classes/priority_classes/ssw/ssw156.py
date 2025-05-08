
from priority_classes.ssw.ssw import SswRequest
import logging

class Ssw156(SswRequest):
    def __init__(self):
        super().__init__()


if __name__ == '__main__':
    with Ssw156() as ssw:
        ssw.init_browser()
        ssw.login()
        ssw.op156()
