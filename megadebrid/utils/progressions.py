class Progress:
    @staticmethod
    def convert_bytes(size):
        for x in ["bytes", "kB", "MB", "GB", "TB"]:
            if size < 1024.0:
                return f"{size:5.1f} {x}"
            size /= 1024.0

        return size

    @staticmethod
    def bar(progress: int, total: int, char: str = "█", size: int = 60) -> None:
        x = int(size * progress / total)
        print(
            f"Downloading [{ char * x }{ ( '.' * ( size - x )) }] "
            f"{ progress }/{ total }",
            flush=True,
            end="\r" if size != total else "\n",
        )

    @staticmethod
    def size(progress: int, total: int):
        print(
            f"{ progress }/{ total }",
            flush=True,
            end="\r" if progress != total else "\n",
        )

    def render(
        self, progress: int, total: int, choice: str = "", to_convert: bool = False
    ) -> None:
        if to_convert:
            progress = self.convert_bytes(progress)
            total = self.convert_bytes(total)

        if choice.lower() == "bar":
            self.bar(progress, total)
        else:
            self.size(progress, total)
