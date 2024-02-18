__all__ = ["Error", "error", "Raiser"]


from typing import Any


ErrorType = str


class Raiser:
    def __init__(cls, msg: ErrorType):
        cls.msg = msg

    def Raise(cls):
        print(cls.msg)

    def __str__(cls) -> ErrorType:
        return cls.msg

    def __repr__(cls) -> ErrorType:
        return cls.msg


class Error:
    __sep__ = " "

    def __init__(self, *args: Any, **kwds: Any):
        self.__args = args
        self.__kwargs = kwds
        if self.__kwargs.get("name", None) is not None:
            if type(self.__kwargs["name"]) == str:
                self.name = self.__kwargs["name"]
            else:
                raise ValueError(
                    "setting 'name' should be a string, not {}".format(
                        type(self.__kwargs["name"])
                    )
                )

        if self.__kwargs.get("sep", None) is not None:
            if type(self.__kwargs["sep"]) == str:
                self.__sep__ = self.__kwargs["sep"]
            else:
                raise ValueError(
                    "setting 'sep' should be a string, not {}".format(
                        type(self.__kwargs["sep"])
                    )
                )

    @property
    def name(self):
        return self.__class__.__name__

    @name.setter
    def name(self, name: str):
        self.__class__.__name__ = name

    @property
    def sep(self):
        return self.__sep__

    @sep.setter
    def sep(self, sep: str):
        self.__sep__ = sep

    def __str__(self) -> ErrorType:
        resval = ""
        for val in self.__args:
            resval += self.sep + str(val)
        return f"{self.name}:{resval}"

    def __repr__(self) -> ErrorType:
        resval = ""
        for val in self.__args:
            resval += self.sep + str(val)
        return f"{self.name}:{resval}"


def error(*args: Any, **kwds: Any) -> Raiser:
    return Raiser(str(Error(*args, kwds=kwds)))
