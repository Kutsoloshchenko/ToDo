from controlers.validation import Validator
from controlers.data_base_handler import DataBaseHandler
from controlers.token_controler import TokenController
from controlers.project_handler import ProjectHandler
from datetime import date

class Model():

    def __init__(self):
            """ Initialize function, creates instances on needed classes"""

            # creates data base orm class
            self._db = DataBaseHandler()

            # creates class that handle user validation
            self._validator = Validator(self._db)

            # imports secret key from config file and creates token controller class instance
            from ToDoBack.settings import SECRET_KEY
            self._jwt_token_creator = TokenController(SECRET_KEY)

            # create osHandler instance
            self._project_handler = ProjectHandler(self._db)

    def _validate_token(self, token, username):
        token_dict = self._jwt_token_creator.decode_token(bytes(token, "UTF-8"))
        username, id_bd = self._db.get_entry_attributes('users', {"username": username}, ("username", "id"))

        if username == token_dict["username"] and id_bd == token_dict["id"]:
            # is provided user name and user id is same as in decoded token that verification is successful
            return id_bd

        else:
            return False

    def sign_up(self, display_name, email, password, repeted_password):
        """Calls validation function of validator class and returns response

            inputs:
                    display_name - username entered by user
                    email - email address entered by user
                    password - password entered by user
                    repeted_password - repeat of the password entered by user

            return:
                    response item returned by validator sign_up function

        """
        response = self._validator.sign_up(display_name.lower(), email.lower(), password, repeted_password)

        return response

    def sign_in(self, email, password):
        """Calls sign_in function of validator class, and on success adds jwt token to the response object

            inputs:
                    email - email address entered by user
                    password - password entered by user
            return:
                    response item dict containing status, error, token and username keys

        """

        response = self._validator.sign_in(email.lower(), password)
        if response["result"] == "Ok":
            username, id = self._db.get_entry_attributes('users', {"email": email}, ("username", "id"))

            if username and id:
                response["token"] = self._jwt_token_creator.create_token(username, id)
                response["username"] = username
            else:
                raise AttributeError

        return response

    # Project handler functions

    def create_project(self, data):

        owner_id = self._validate_token(data.pop('token'), data.pop('username'))

        if owner_id:
            # is provided user name and user id is same as in decoded token that verification is successful
            data["owner"] = self._db.get_entry("users", {"id": owner_id})
            response = self._project_handler.create_project(data)

        else:
            response = {"result": 'Fail', "error": 'Auth error'}

        return response

    def change_project(self, data):
        owner_id = self._validate_token(data.pop('token'), data.pop('username'))

        if owner_id:
            # is provided user name and user id is same as in decoded token that verification is successful
            data["owner"] = self._db.get_entry("users", {"id": owner_id})
            response = self._project_handler.change_project(data)

        else:
            response = {"result": 'Fail', "error": 'Auth error'}

        return response

    def delete_project(self, data):
        owner_id = self._validate_token(data.pop('token'), data.pop('username'))

        if owner_id:
            # is provided user name and user id is same as in decoded token that verification is successful
            data["owner"] = self._db.get_entry("users", {"id": owner_id})
            response = self._project_handler.delete_project(data)

        else:
            response = {"result": 'Fail', "error": 'Auth error'}

        return response

    def get_projects(self, data):
        owner_id = self._validate_token(data.pop('token'), data.pop('username'))

        if owner_id:
            # is provided user name and user id is same as in decoded token that verification is successful
            data["owner"] = self._db.get_entry("users", {"id": owner_id})
            response = self._project_handler.get_projects(data)

        else:
            response = {"result": 'Fail', "error": 'Auth error'}

        return response

    # Task handler functions

    def create_task(self, data):

        owner_id = self._validate_token(data.pop('token'), data.pop('username'))

        if owner_id:
            # is provided user name and user id is same as in decoded token that verification is successful
            data["project"] = self._db.get_entry("projects", {"id": data['project']})
            data["owner"] = self._db.get_entry("users", {"id": owner_id})
            response = self._project_handler.create_task(data)

        else:
            response = {"result": 'Fail', "error": 'Auth error'}

        return response

    def get_tasks_for_today(self, data):
        owner_id = self._validate_token(data.pop('token'), data.pop('username'))

        if owner_id:
            # is provided user name and user id is same as in decoded token that verification is successful
            data["owner"] = self._db.get_entry("users", {"id": owner_id})
            response = self._project_handler.get_tasks_for_today(data)

        else:
            response = {"result": 'Fail', "error": 'Auth error'}

        return response

    def get_tasks_for_project(self, data):
        owner_id = self._validate_token(data.pop('token'), data.pop('username'))

        if owner_id:
            # is provided user name and user id is same as in decoded token that verification is successful
            data["owner"] = self._db.get_entry("users", {"id": owner_id})
            response = self._project_handler.get_tasks_for_project(data)

        else:
            response = {"result": 'Fail', "error": 'Auth error'}

        return response

    def get_tasks_for_7_days(self, data):
        owner_id = self._validate_token(data.pop('token'), data.pop('username'))

        if owner_id:
            # is provided user name and user id is same as in decoded token that verification is successful
            data["owner"] = self._db.get_entry("users", {"id": owner_id})
            response = self._project_handler.get_tasks_for_7_days(data)

        else:
            response = {"result": 'Fail', "error": 'Auth error'}

        return response

    def get_done_tasks(self, data):
        owner_id = self._validate_token(data.pop('token'), data.pop('username'))

        if owner_id:
            # is provided user name and user id is same as in decoded token that verification is successful
            data["owner"] = self._db.get_entry("users", {"id": owner_id})
            response = self._project_handler.get_done_tasks(data)

        else:
            response = {"result": 'Fail', "error": 'Auth error'}

        return response

    def delete_task(self, data):
        owner_id = self._validate_token(data.pop('token'), data.pop('username'))

        if owner_id:
            # is provided user name and user id is same as in decoded token that verification is successful
            response = self._project_handler.delete_task(data)

        else:
            response = {"result": 'Fail', "error": 'Auth error'}

        return response

    def change_task(self, data):

        owner_id = self._validate_token(data.pop('token'), data.pop('username'))

        if owner_id:
            # is provided user name and user id is same as in decoded token that verification is successful
            data["owner"] = self._db.get_entry("users", {"id": owner_id})
            data["project"] = self._db.get_entry("projects", {"id": data['project']})
            response = self._project_handler.change_task(data)

        else:
            response = {"result": 'Fail', "error": 'Auth error'}

        return response