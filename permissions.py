class Permission:

    @staticmethod
    def isAuthorized(permission: str):
        """ Verify user authorization using the database entries or session cookie(s). """
        from main import session

        if 'permissions' in session:
            return str(session['permissions']).split(', ').__contains__(permission)

        return False

    @staticmethod
    def getPermissions():
        """ returns possible permissions """
        return [
            "administator.*"
            "interface.*",
            "*"
        ]


class RoutePermissions:
    """ A class for setting the route authorization variables based on the request method. """

    def __init__(self, post: str = None, get: str = None,
                 put: str = None, delete: str = None):
        self.post = post
        self.get = get
        self.put = put
        self.delete = delete

    def getPermission(self, method: str):
        if method.upper() == "POST":
            return self.post
        elif method.upper() == "GET":
            return self.get
        elif method.upper() == "PUT":
            return self.put
        elif method.upper() == "DELETE":
            return self.delete
        else:
            return None
