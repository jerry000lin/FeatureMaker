from io import BytesIO
from pathlib import Path

from featuremaker.storage.local_table_storage import LocalTableStorage


def test_local_table_storage_saves_and_deletes_file(tmp_path):
    storage = LocalTableStorage(str(tmp_path))

    storage_uri = storage.save(
        file_name="customers.csv",
        file_obj=BytesIO(b"customer_id,name\n1,Alice\n"),
    )

    saved_file = Path(storage_uri)
    assert saved_file.exists()
    assert saved_file.suffix == ".csv"
    assert saved_file.read_bytes() == b"customer_id,name\n1,Alice\n"

    storage.delete(storage_uri)
    assert not saved_file.exists()


def test_local_table_storage_saves_text_file(tmp_path):
    storage = LocalTableStorage(str(tmp_path))

    storage_uri = storage.save_text(
        file_name="customers.csv",
        content="customer_id,name\n1,Alice\n",
    )

    saved_file = Path(storage_uri)
    assert saved_file.exists()
    assert saved_file.suffix == ".csv"
    assert saved_file.read_text(encoding="utf-8") == "customer_id,name\n1,Alice\n"
