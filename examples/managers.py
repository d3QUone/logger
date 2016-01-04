__author__ = 'vladimir'

from logger import Logger

mlog = Logger("com.manager")


class UserManager(object):
    """High-level database interface"""
    SUPER_USER = 0
    OWNER = 1
    PARTNER = 2
    FINANCIER = 3
    USER = 4

    ALL_GROUPS = (SUPER_USER, OWNER, PARTNER, FINANCIER, USER)

    def __init__(self):
        self.storage = {}
        self.amount = 0

    def create_user(self, slug, name, email, group):
        if slug not in self.storage:
            if group not in self.ALL_GROUPS:
                group = self.USER

            self.storage[slug] = {
                "name": name,
                "email": email,
                "group": group
            }
            self.amount += 1
            mlog.info("User {} added to storage".format(mlog.colorize("green", slug)))
            return True
        else:
            mlog.info("User {} already exists".format(mlog.colorize("red", slug)))
            return False

    def update_user(self):
        raise NotImplementedError

    def get_user(self, slug):
        return self.storage.get(slug)

    def list_users(self):
        return self.storage

    def get_amount(self):
        return self.amount
