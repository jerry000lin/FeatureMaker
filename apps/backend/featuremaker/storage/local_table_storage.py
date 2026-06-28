from pathlib import Path
from shutil import copyfileobj
from typing import BinaryIO
from uuid import uuid4


class LocalTableStorage:
    """
    本地受管表文件存储。
    """

    def __init__(self, root_dir: str) -> None:
        self.root_dir = Path(root_dir)

    def save(self, *, file_name: str, file_obj: BinaryIO) -> str:
        suffix = Path(file_name).suffix.lower()
        storage_path = self.root_dir / f"{uuid4().hex}{suffix}"
        storage_path.parent.mkdir(parents=True, exist_ok=True)

        with storage_path.open("wb") as target:
            copyfileobj(file_obj, target)

        return str(storage_path)

    def save_text(self, *, file_name: str, content: str) -> str:
        suffix = Path(file_name).suffix.lower()
        storage_path = self.root_dir / f"{uuid4().hex}{suffix}"
        storage_path.parent.mkdir(parents=True, exist_ok=True)
        storage_path.write_text(content, encoding="utf-8")
        return str(storage_path)

    def delete(self, storage_uri: str) -> None:
        Path(storage_uri).unlink(missing_ok=True)
