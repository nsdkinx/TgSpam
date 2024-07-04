# -*- coding: utf-8 -*-

class UsersContainer:
    """Provides a global users iterator"""

    def __init__(self, users: list[str]):
        self.users = users
        self._users_iterator = iter(users)

    def _update_iterator(self):
        """Needs to be called when the user list is updated
        (i.e. the user is removed)"""
        self._users_iterator = iter(self.users)

    def take_user(self) -> str:
        """Takes a user and removes it from the list.
        Entity getting and StopIteration is handled by the worker"""
        user = next(self._users_iterator)
        self.users.remove(user)
        self._update_iterator()
        return user
