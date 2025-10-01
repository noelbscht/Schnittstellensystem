import datetime

from permissions import *
from http import HTTPStatus

"""
    HTTP Methods:
   | POST   ->  create data  |
   | GET    ->  request data |
   | PUT    ->  update data  |
   | DELETE ->  delete data  | 
"""


class Header:

    def __init__(self, key: str, required: bool):
        self.key = key
        self.required = required

    def is_needed_feedback(self):
        """ returns json object that requests missing header """
        from main import jsonify
        return jsonify({
            "message": "Missing required parameter.",
            "header": self.key

        }), HTTPStatus.UNPROCESSABLE_ENTITY


class Interface:

    def __init__(self):
        self.routes = [
            RouteInformation("request general interface information."),
            RouteGreeting("returns a personalized greeting based on the passed name."),
            RouteUserInformation("request basic user information."),
            RouteServerStatus("request basic server information. (cookie-authentication)"),
            RouteAuthentication("Handles user authentication keys: create, validate, renew and delete.")
        ]

    def handle_request(self, request, path):
        from main import jsonify, session

        interface = self.get_route(path)
        if interface:
            if request.method not in interface.methods:
                if request.method == "OPTIONS":
                    # CORS response
                    return interface.options_response()

                return jsonify({
                    'message': "Method not allowed"
                }), HTTPStatus.METHOD_NOT_ALLOWED

            # check headers
            if interface.headers:
                for header in interface.headers:
                    if not header.required:
                        continue
                    if header.key not in request.headers:
                        return header.is_needed_feedback()

            # check permission
            if interface.permissions:
                method_perm = interface.permissions.getPermission(request.method)
                if method_perm:
                    if 'group' not in session or not Permission.isAuthorized(method_perm):
                        return jsonify({'message': 'Unauthorized request.'}), HTTPStatus.UNAUTHORIZED

            # return interface
            try:
                return interface.on_request(request)
            except Exception as ex:
                return jsonify({'error': ex.args}), HTTPStatus.INTERNAL_SERVER_ERROR

    def get_route(self, path):
        for r in self.routes:
            if r.path == path:
                return r
        return None

    def get_routes(self):
        return self.routes


class APIRoute:
    def __init__(self, path: str, description: str,
                 methods: list, headers: list[Header], permissions: RoutePermissions):
        self.path = path
        self.description = description
        self.methods = methods
        self.headers = headers
        self.permissions = permissions

    def on_request(self, request):
        raise NotImplementedError("Please Implement this method")

    def options_response(self):
        # allow methods + OPTIONS method
        allowed_methods = set(self.methods)
        allowed_methods.add("OPTIONS")

        # allow headers
        headers = [h.key for h in self.headers]
        allowed_headers = ", ".join(headers)

        from main import make_response
        response = make_response("", 200)
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = ", ".join(sorted(allowed_methods))
        response.headers["Access-Control-Allow-Headers"] = allowed_headers or "*"
        response.headers["Access-Control-Max-Age"] = "3600"
        return response


class RouteInformation(APIRoute):

    def __init__(self, description: str):
        super().__init__("information", description, ["GET"], [], RoutePermissions())

    def on_request(self, request):
        from main import jsonify

        routes = []
        for r in interface.get_routes():
            routes.append({r.__class__.__name__: {
                "path": "/api/" + r.path,
                "description": r.description,
                "permissions": r.permissions.__dict__,
                "headers": [h.key for h in r.headers],
                "methods": r.methods
            }})

        return jsonify({
            "routes": routes
        })


class RouteGreeting(APIRoute):

    def __init__(self, description):
        super().__init__("greeting", description, ["GET"], [Header("X-GREET-Name", True)], RoutePermissions())

    def on_request(self, request):
        from main import jsonify

        name = request.headers['X-GREET-Name']

        message = f"Hello {name}!"

        return jsonify({
            "message": message
        })


class RouteUserInformation(APIRoute):

    def __init__(self, description):
        super().__init__("user/information", description, ["GET"], [], RoutePermissions())

    def on_request(self, request):
        from main import jsonify, session

        if 'group' not in session:
            return jsonify({
                "error": "user group not set."
            }), HTTPStatus.BAD_REQUEST

        group = session['group']
        perms = session['permissions']

        return jsonify({
            "user_group": group,
            "permissions": perms
        })


class RouteServerStatus(APIRoute):

    def __init__(self, description):
        super().__init__("status", description, ["GET"], [], RoutePermissions(get="server.status"))

    def on_request(self, request):
        from main import jsonify

        return jsonify({
            "status": "OK",
            "datetime": datetime.datetime.now()
        })


class RouteAuthentication(APIRoute):

    def __init__(self, description):
        super().__init__("authentication", description,
                         ["GET", "POST", "PUT", "DELETE"],
                         [Header("X-AUTH-User", True), Header("X-AUTH-Key", False)],
                         RoutePermissions())

    def on_request(self, request):
        from main import jsonify
        from utils import sql

        user = request.headers.get("X-AUTH-User", None)
        key = request.headers.get("X-AUTH-Key", None)

        if user:
            if request.method == "POST":
                # create auth key
                if sql("SELECT COUNT(*) FROM authentication WHERE LOWER(user) = %s;", (user.lower(),), fetch_one=True)[0] > 0:
                    return jsonify({
                        "error": "user already exists",
                        "user": user
                    })

                row_id = sql("INSERT IGNORE INTO authentication (user) VALUES (%s);", (user,), return_insert_id=True)
                new_key = sql("SELECT auth_key FROM authentication WHERE id = %s;", (row_id,), fetch_one=True)[0]
                return jsonify({
                    "status": "auth_key created",
                    "user": user,
                    "key": new_key
                })
            elif not key:
                # require X-AUTH-KEY header
                return self.headers[1].is_needed_feedback()

            if request.method == "GET":
                # return specific auth key
                result = sql("SELECT * FROM authentication WHERE user = %s AND auth_key = %s;", (user, key),
                             fetch_one=True)

                if result:
                    return jsonify({
                        "status": "successfully validated",
                    })
                return jsonify({
                    "status": "validation failed",
                })
            elif request.method == "PUT":
                # prevent if validation failed
                if sql("SELECT COUNT(*) FROM authentication WHERE LOWER(user) = %s AND auth_key = %s;", (user.lower(), key), fetch_one=True)[0] == 0:
                    return jsonify({
                        "status": "failed"
                    })

                # update auth key
                sql("UPDATE authentication SET auth_key = (UUID()) WHERE user = %s AND auth_key = %s;",
                             (user, key))
                return jsonify({
                    "status": "auth_key updated"
                })
            elif request.method == "DELETE":
                # prevent if validation failed
                if sql("SELECT COUNT(*) FROM authentication WHERE LOWER(user) = %s AND auth_key = %s;", (user.lower(), key), fetch_one=True)[0] == 0:
                    return jsonify({
                        "status": "failed"
                    })

                # delete auth key
                sql("DELETE FROM authentication WHERE user = %s AND auth_key = %s;", (user, key))
                return jsonify({
                    "status": "auth_key deleted"
                })

        # require X-AUTH-USER header
        return self.headers[0].is_needed_feedback()


interface = Interface()
