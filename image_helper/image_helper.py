from PIL import Image, ImageTk
from image_helper.symbol import SYMBOLS, Symbol

class ImageHelper:
    code_to_image: dict[int, ImageTk.PhotoImage]

    def _load_symbol(self, symbol: Symbol):
        image_raw = Image.open(symbol.resource_path)
        self.code_to_image[symbol.number] = ImageTk.PhotoImage(image_raw)

    def __init__(self):
        self.code_to_image = {}
        for symbol in SYMBOLS:
            print(f"Loading symbol: {symbol.name}")
            self._load_symbol(symbol)

    def __getitem__(self, key) -> ImageTk.PhotoImage | None:
        return self.code_to_image[key] if key in self.code_to_image.keys() else None
