from dataclasses import dataclass

@dataclass
class Symbol:
    resource_path: str
    number: int
    name: str

SYMBOLS = [
    Symbol("res/Bannana-Sprite.png", 0, "Bannana"),
    Symbol("res/Cherry-Sprite.png", 1, "Cherry"),
    Symbol("res/Dollar-Sprite.png", 2, "Dollar"),
    Symbol("res/Watermelon-Sprite.png", 3, "Watermelon"),
    Symbol("res/Seven-Sprite.png", 7, "Seven"),
    Symbol("res/Apple-Sprite.png", 13, "Apple"),
]
