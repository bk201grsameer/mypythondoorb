class A:
    def __init__(self) -> None:
        self.a = "a"


class B:
    def __init__(self) -> None:
        self.b = "b"


class s(A, B):
    def __init__(self) -> None:
        super().__init__()
    def 