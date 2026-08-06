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
    Symbol("res/Bar-Sprite.png", 4, "Bar"),
    Symbol("res/Lemon-Sprite.png", 5, "Lemon"),
    Symbol("res/Orange-Sprite.png", 6, "Orange"),
    Symbol("res/Seven-Sprite.png", 7, "Seven"),
    Symbol("res/Grapes-Sprite.png", 8, "Grapes"),
    Symbol("res/Rose-Sprite.png", 9, "Rose"),
    Symbol("res/Diamond-Sprite.png", 10, "Diamond"),
    Symbol("res/Emerald-Sprite.png", 11, "Emerald"),
    Symbol("res/Carrot-Sprite.png", 12, "Carrot"),
    Symbol("res/Apple-Sprite.png", 13, "Apple"),
    Symbol("res/Pumpkin-Sprite.png", 14, "Pumpkin"),
    Symbol("res/Cat-Sprite.png", 15, "Cat"),
    Symbol("res/Clover-Sprite.png", 16, "Clover"),
    Symbol("res/Lime-Sprite.png", 17, "Lime"),
    Symbol("res/Plum-Sprite.png", 18, "Plum"),
    Symbol("res/Bell-Sprite.png", 19, "Bell"),
]
