from typing import Callable, Any
from enum import Enum


class NotLoaded(FileNotFoundError):
    '''Not loaded.'''
    pass


class ModeEnum(Enum):
    PAUSE = None
    CONTINUE = 1


class SaveLoad:
    def __init__(self, target: str = None, mode: ModeEnum = ModeEnum.CONTINUE):
        self.MODE = mode

        self.target: str = target

        self._loader_fn = None
        self._saver_fn = None
        self._creator_fn = None
        self._processor_fn = None

    def load(self, load_fn: Callable[[], Any], options={}):
        self._loader_fn = load_fn

    def create(self, create_fn: Callable[[], Any]):
        self._creator_fn = create_fn

    def process(self, process_fn: Callable[[Any], Any]):
        self._processor_fn = process_fn

    def save(self, save_fn: Callable):
        self._saver_fn = save_fn

    def _load(self, *args):
        if not self._loader_fn:
            raise NotImplementedError(
                'Function `load` has not been implemented.')
        try:
            result = self._loader_fn(self.target, *args)
        except NotLoaded:
            result = self._create(*args)

        return result

    def _create(self, *args):
        if not self._creator_fn:
            raise NotImplementedError(
                'Function `create` has not been implemented.')
        result = self._creator_fn(*args)
        return result

    def _process(self, data, *args):
        if not self._processor_fn:
            raise NotImplementedError(
                'Function `process` has not been implemented.')
        result = self._processor_fn(data, *args)
        return result

    def _save(self, data, *args):
        if not self._saver_fn:
            raise NotImplementedError(
                'Function `save` has not been implemented.')
        return self._saver_fn(self.target, data, *args)

    def execute(self, save=True):
        data = self._load()
        result = data

        if self.MODE == ModeEnum.CONTINUE:
            result = self._process(result)

            if save:
                self._save(result)

        return result
