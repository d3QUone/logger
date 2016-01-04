__author__ = 'vladimir'

import json

import falcon
from logger import Logger

from managers import UserManager


log = Logger("com.api")
api = falcon.API()
user_manager = UserManager()


class UserHandlerResource(object):

    def on_get(self, request, response):
        """List all registered users"""
        log.info("Asked list of users")
        response.body = json.dumps(user_manager.list_users())

    def on_post(self, request, response):
        """Create a new user o throw error"""
        slug = request.get_param("slug", required=True)
        name = request.get_param("name", required=True)
        email = request.get_param("email", required=True)
        group = request.get_param("group", required=True)

        res = user_manager.create_user(slug, name, email, group)
        log.info("{}".format("User created - OK" if res else "User was already created"))

        response.body = json.dumps({
            "success": res
        })


user_handler = UserHandlerResource()
api.add_route("/user", user_handler)
