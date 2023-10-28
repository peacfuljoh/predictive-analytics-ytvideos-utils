
import tempfile

from src.ytpa_utils.io_utils import save_json, load_json




def test_save_load_json():
    obj = {'a': {'b': [1, 2, 3], 'c': [5, 4, 'a']}, 'd': [1, 2, 3], 'e': '2432'}

    with tempfile.NamedTemporaryFile() as filename:
        save_json(filename.name, obj)
        assert load_json(filename.name) == obj

