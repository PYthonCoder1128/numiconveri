from string import ascii_lowercase, ascii_uppercase, digits, punctuation
from pyperclip import copy
from icecream import ic

from error import *


def decimal_to_binary(number):
    binary_digits = []

    while number > 0:
        remainder = number % 2
        binary_digits.append(remainder)
        number //= 2

    # Reverse the binary_digits list to get the correct binary representation
    binary_digits.reverse()

    # Convert binary digits to a string representation
    binary_string = "".join(map(str, binary_digits))

    return binary_string


_TextType = str
_BinaryType = str


numbers = [
    "10000",
    "10001",
    "10010",
    "10011",
    "10100",
    "10101",
    "10110",
    "10111",
    "11000",
    "11001",
]


class Text:
    def __init__(self, __text: _TextType | None = None) -> None:
        self.str = str(__text)

    def get(self) -> _TextType:
        return self.str

    def __str__(self) -> _TextType:
        return self.str

    def __repr__(self) -> _TextType:
        return self.str

    def to_binary(self) -> _BinaryType:
        space = " "
        resstr = ""
        zeros = ""

        for char in self.str:
            if char in ascii_lowercase:
                zeros += "0" * (
                    5 - len(decimal_to_binary(ascii_lowercase.index(char) + 1))
                )
                resstr += f"011{zeros}{decimal_to_binary(ascii_lowercase.index(char) + 1)}{space}"
                zeros = ""
            elif char in ascii_uppercase:
                zeros += "0" * (
                    5 - len(decimal_to_binary(ascii_uppercase.index(char) + 1))
                )
                resstr += f"010{zeros}{decimal_to_binary(ascii_uppercase.index(char) + 1)}{space}"
                zeros = ""
            elif char in digits:
                if char == "0":
                    zeros += "0" * (4 - len(decimal_to_binary(digits.index(char) - 1)))
                    resstr += (
                        f"0011{zeros}{decimal_to_binary(digits.index(char) - 1)}{space}"
                    )
                    zeros = ""
                else:
                    zeros += "0" * (4 - len(decimal_to_binary(digits.index(char))))
                    resstr += (
                        f"0011{zeros}{decimal_to_binary(digits.index(char))}{space}"
                    )
                    zeros = ""
            elif char in punctuation:
                zeros += "0" * (5 - len(decimal_to_binary(punctuation.index(char) + 1)))
                resstr += (
                    f"001{zeros}{decimal_to_binary(punctuation.index(char) + 1)}{space}"
                )
                zeros = ""
            elif char == " ":
                zeros = ""
                resstr += f"00100000{space}"

        return resstr[:-1]

    def set_as_binary(self):
        self.str = self.to_binary()


class Binary:
    def __init__(self, __binary: _BinaryType | None = None) -> None:
        self.str = str(__binary)

    def get(self) -> _BinaryType:
        return self.str

    def __str__(self) -> _BinaryType:
        return self.str

    def __repr__(self) -> _BinaryType:
        return self.str

    def to_text(self) -> _TextType:
        for char in self.str:
            if char not in ["0", "1", " "]:

                error(
                    "invalid character '%s' in %s" % (char, self.str),
                    name="TranslateCharactersError",
                ).Raise()

        if self.str[-1] != " ":
            self.str += " "

        resstr = ""
        current = ""  # 8-bit only; if it is 7 bytes long then raise error.
        for byte in self.str:
            if byte != " ":
                current += str(byte)
            else:
                ic(current)
                if current[:3] == "011":
                    holder = ""
                    binletter = current[3:]
                    oned = False
                    xzeros = ""
                    for byte in binletter:
                        if byte == "1":
                            if oned == False:
                                oned = True
                            holder += byte
                        elif byte == "0":
                            if oned == True:
                                holder += byte
                            else:
                                xzeros += byte
                    ic(holder, oned)

                    ic(len(holder))
                    holder1 = 0
                    for idx, power in enumerate(reversed(range(len(holder)))):
                        holder1 += int(holder[idx]) * (2 ** int(power))

                    ic(holder1)

                    try:
                        letter = ascii_lowercase[holder1 - 1]
                        ic(letter)
                    except IndexError:
                        pass
                    else:
                        resstr += letter
                        ic(resstr)

                        holder = ""
                        oned = False
                        xzeros = ""

                elif current[:3] == "010":
                    holder = ""
                    binletter = current[3:]
                    oned = False
                    xzeros = ""
                    for byte in binletter:
                        if byte == "1":
                            if oned == False:
                                oned = True
                            holder += byte
                        elif byte == "0":
                            if oned == True:
                                holder += byte
                            else:
                                xzeros += byte
                    ic(holder, oned)

                    ic(len(holder))
                    holder1 = 0
                    for idx, power in enumerate(reversed(range(len(holder)))):
                        holder1 += int(holder[idx]) * (2 ** int(power))

                    ic(holder1)

                    try:
                        letter = ascii_uppercase[holder1 - 1]
                        ic(letter)
                    except IndexError:
                        pass
                    else:
                        resstr += letter
                        ic(resstr)

                        holder = ""
                        oned = False
                        xzeros = ""

                elif current[:3] == "001":
                    binletter = current[3:]
                    if binletter in numbers:
                        resstr += str(numbers.index(binletter))
                        ic(resstr)
                    elif binletter == "00000":
                        resstr += " "
                    else:
                        holder = ""
                        oned = False
                        xzeros = ""
                        for byte in binletter:
                            if byte == "1":
                                if oned == False:
                                    oned = True
                                holder += byte
                            elif byte == "0":
                                if oned == True:
                                    holder += byte
                                else:
                                    xzeros += byte
                        ic(holder, oned)

                        ic(len(holder))
                        holder1 = 0
                        for idx, power in enumerate(reversed(range(len(holder)))):
                            holder1 += int(holder[idx]) * (2 ** int(power))

                        ic(holder1)

                        try:
                            punc = punctuation[holder1 - 1]
                            ic(digits)
                        except IndexError:
                            pass
                        else:
                            resstr += punc
                            ic(resstr)

                            holder = ""
                            oned = False
                            xzeros = ""

                current = ""

        if self.str[-1] == " ":
            self.str = self.str[:-1]

        return resstr

    def set_as_text(self):
        self.str = self.to_text()


t = Text("null").to_binary()
ic(t)
ic(Binary("00100000").to_text())
