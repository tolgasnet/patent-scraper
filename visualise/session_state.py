from collections.abc import MutableMapping
from typing import Any


class SessionManager:
    """Handle session state bookkeeping with a simple mapping backend."""

    PAGE_KEY = "page"
    DATASET_KEY = "_selected_dataset"
    SEARCH_KEY = "_search_query"

    def __init__(self, storage: MutableMapping[str, Any]):
        self._storage = storage

    @property
    def page(self) -> int:
        return int(self._storage.get(self.PAGE_KEY, 1))

    @page.setter
    def page(self, value: int) -> None:
        self._storage[self.PAGE_KEY] = max(1, int(value))

    @property
    def search_query(self) -> str:
        return str(self._storage.get(self.SEARCH_KEY, ""))

    def update_search_query(self, query: str) -> None:
        if self.search_query != query:
            self._storage[self.SEARCH_KEY] = query
            self.reset_page()

    def record_dataset(self, dataset_identifier: str) -> None:
        if self._storage.get(self.DATASET_KEY) != dataset_identifier:
            self._storage[self.DATASET_KEY] = dataset_identifier
            self.reset_page()

    def reset_page(self) -> None:
        self._storage[self.PAGE_KEY] = 1
