
import tempfile

from src.ytpa_utils.io_utils import save_json, load_json, save_pickle, load_pickle




def test_save_load_json():
    obj = {'a': {'b': [1, 2, 3], 'c': [5, 4, 'a']}, 'd': [1, 2, 3], 'e': '2432'}

    with tempfile.NamedTemporaryFile() as file:
        save_json(file.name, obj)
        assert load_json(file.name) == obj

def test_save_load_pickle():
    obj = {'a': {'b': [1, 2, 3], 'c': [5, 4, 'a']}, 'd': [1, 2, 3], 'e': '2432'}

    with tempfile.NamedTemporaryFile() as file:
        save_pickle(file.name, obj)
        assert load_pickle(file.name) == obj

