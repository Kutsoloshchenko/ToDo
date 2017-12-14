from controlers.validation import Validator
from controlers.data_base_handler import DataBaseHandler
from controlers.token_controler import TokenController
from controlers.project_and_task_handler import ProjectAndTaskHandler
from datetime import date

class Controler():
    """Level of abstractionsm which functions as a overall controler.
    It will call appropriate functions and models based of view and user input """

    def __init__(self):
            """ Initialize function, creates instances on needed classes"""

            # creates data base orm class
            self._db = DataBaseHandler()

            # creates class that handle user validation
            self._validator = Validator(self._db)

            # imports secret key from config file and creates token controller class instance
            from ToDoBack.settings import SECRET_KEY
            self._jwt_token_creator = TokenController(SECRET_KEY)

            # create Projects and Task handler instance
            self._project_handler = ProjectAndTaskHandler(self._db)

    def _validate_token(self, token, username):
        """ Validates JWR token and returns ID of the user if validation is successful

            Params:
                    token - JWT encoded token
                    username - name of the user

            Returns:
                    ID of the user if validation is successful
                    False if validation is failed

            Important note:
                    This should be realized as a decorator function, so all functions would not have to copy-paste
                    basic function with validation. This will be implemented in future version
        """
        token_dict = self._jwt_token_creator.decode_token(bytes(token, "UTF-8"))
        entry = self._db.get_entry('users', {"username": username})

        if entry["username"] == token_dict["username"] and entry["id"] == token_dict["id"]:
            # is provided user name and user id is same as in decoded token that verification is successful
            return entry["id"]

        else:
            return False

    def sign_up(self, display_name, email, password, repeted_password):
        """Calls validation function of validator class and returns response

            Params:
                    display_name - username entered by user
                    email - email address entered by user
                    password - password entered by user
                    repeted_password - repeat of the password entered by user

            Returns:
                    response item returned by validator sign_up function

        """
        response = self._validator.sign_up(display_name.lower(), email.lower(), password, repeted_password)

        return response

    def sign_in(self, email, password):
        """Calls sign_in function of validator class, and on success adds jwt token to the response object

            Params:
                    email - email address entered by user
                    password - password entered by user
            Returns:
                    response item dict containing status, error, token and username keys

        """

        response = self._validator.sign_in(email.lower(), password)
        if response["result"] == "Ok":
            entry = self._db.get_entry('users', {"email": email})

            if entry:
                response["token"] = self._jwt_token_creator.create_token(entry["username"], entry["id"])
                response["username"] = entry["username"]
            else:
                raise AttributeError

        return response

    # Project handler functions - functions to create, update and get projects

    def create_project(self, data):
        """Creates project with specified parameters

            Params:
                    data - dictionary of parameters received from client

            Returns:
                    response dictionary

            Important Note:
                    This function should be decorated with validation decorator in future,
                    to make code easier and smaller

         """

        owner_id = self._validate_token(data.pop('token'), data.pop('username'))

        if owner_id:
            # if provided user name and user id is same as in decoded token that verification is successful
            data["owner"] = self._db.get_entry("users", {"id": owner_id})
            response = self._project_handler.create_project(data)

        else:
            response = {"result": 'Fail', "error": 'Auth error'}

        return response

    def change_project(self, data):
        """Creates project attributes

            Params:
                    data - dictionary of parameters received from client

            Returns:
                    response dictionary

            Important Note:
                    This function should be decorated with validation decorator in future,
                    to make code easier and smaller

        """
        owner_id = self._validate_token(data.pop('token'), data.pop('username'))

        if owner_id:
            # if provided user name and user id is same as in decoded token that verification is successful
            data["owner"] = self._db.get_entry("users", {"id": owner_id})
            response = self._project_handler.change_project(data)

        else:
            response = {"result": 'Fail', "error": 'Auth error'}

        return response

    def delete_project(self, data):
        """Deletes project with specified parameters

            Params:
                    data - dictionary of parameters received from client

            Returns:
                    response dictionary

            Important Note:
                    This function should be decorated with validation decorator in future,
                    to make code easier and smaller

        """
        owner_id = self._validate_token(data.pop('token'), data.pop('username'))

        if owner_id:
            # if provided user name and user id is same as in decoded token that verification is successful
            data["owner"] = self._db.get_entry("users", {"id": owner_id})
            response = self._project_handler.delete_project(data)

        else:
            response = {"result": 'Fail', "error": 'Auth error'}

        return response

    def get_projects(self, data):
        """Return all users projects

            Params:
                    data - dictionary of parameters received from client

            Returns:
                    response dictionary

            Important Note:
                    This function should be decorated with validation decorator in future,
                    to make code easier and smaller

        """

        owner_id = self._validate_token(data.pop('token'), data.pop('username'))

        if owner_id:
            # is provided user name and user id is same as in decoded token that verification is successful
            data["owner"] = self._db.get_entry("users", {"id": owner_id})
            response = self._project_handler.get_projects(data)

        else:
            response = {"result": 'Fail', "error": 'Auth error'}

        return response

    # Task handler functions - functions to create, update and get tasks

    def create_task(self, data):
        """Creates task with specified parameters

            Params:
                    data - dictionary of parameters received from client

            Returns:
                    response dictionary

            Important Note:
                    This function should be decorated with validation decorator in future,
                    to make code easier and smaller

            """

        owner_id = self._validate_token(data.pop('token'), data.pop('username'))

        if owner_id:
            # if provided user name and user id is same as in decoded token that verification is successful
            data["project"] = self._db.get_entry("projects", {"id": data['project']})
            data["owner"] = self._db.get_entry("users", {"id": owner_id})
            response = self._project_handler.create_task(data)

        else:
            response = {"result": 'Fail', "error": 'Auth error'}

        return response

    def get_tasks_for_today(self, data):
        """Get tasks with Due Date - today

            Params:
                    data - dictionary of parameters received from client

            Returns:
                    response dictionary

            Important Note:
                    This function should be decorated with validation decorator in future,
                    to make code easier and smaller

        """
        owner_id = self._validate_token(data.pop('token'), data.pop('username'))

        if owner_id:
            # if provided user name and user id is same as in decoded token that verification is successful
            data["owner"] = self._db.get_entry("users", {"id": owner_id})
            response = self._project_handler.get_tasks_for_today(data)

        else:
            response = {"result": 'Fail', "error": 'Auth error'}

        return response

    def get_tasks_for_project(self, data):
        """Get tasks for specified project

            Params:
                    data - dictionary of parameters received from client

            Returns:
                    response dictionary

            Important Note:
                    This function should be decorated with validation decorator in future,
                    to make code easier and smaller

        """
        owner_id = self._validate_token(data.pop('token'), data.pop('username'))

        if owner_id:
            # is provided user name and user id is same as in decoded token that verification is successful
            data["owner"] = self._db.get_entry("users", {"id": owner_id})
            response = self._project_handler.get_tasks_for_project(data)

        else:
            response = {"result": 'Fail', "error": 'Auth error'}

        return response

    def get_tasks_for_7_days(self, data):
        """Get tasks with Due Date in next 7 days

            Params:
                    data - dictionary of parameters received from client

            Returns:
                    response dictionary

            Important Note:
                    This function should be decorated with validation decorator in future,
                    to make code easier and smaller

        """
        owner_id = self._validate_token(data.pop('token'), data.pop('username'))

        if owner_id:
            # if provided user name and user id is same as in decoded token that verification is successful
            data["owner"] = self._db.get_entry("users", {"id": owner_id})
            response = self._project_handler.get_tasks_for_7_days(data)

        else:
            response = {"result": 'Fail', "error": 'Auth error'}

        return response

    def get_done_tasks(self, data):
        """Get all tasks with status Done

            Params:
                    data - dictionary of parameters received from client

            Returns:
                    response dictionary

            Important Note:
                    This function should be decorated with validation decorator in future,
                    to make code easier and smaller

        """
        owner_id = self._validate_token(data.pop('token'), data.pop('username'))

        if owner_id:
            # if provided user name and user id is same as in decoded token that verification is successful
            data["owner"] = self._db.get_entry("users", {"id": owner_id})
            response = self._project_handler.get_done_tasks(data)

        else:
            response = {"result": 'Fail', "error": 'Auth error'}

        return response

    def delete_task(self, data):
        """Delete task with specified parameters

            Params:
                    data - dictionary of parameters received from client

            Returns:
                    response dictionary

            Important Note:
                    This function should be decorated with validation decorator in future,
                    to make code easier and smaller

        """
        owner_id = self._validate_token(data.pop('token'), data.pop('username'))

        if owner_id:
            # is provided user name and user id is same as in decoded token that verification is successful
            response = self._project_handler.delete_task(data)

        else:
            response = {"result": 'Fail', "error": 'Auth error'}

        return response

    def change_task(self, data):
        """Update task with specified parameters

            Params:
                    data - dictionary of parameters received from client

            Returns:
                    response dictionary

            Important Note:
                    This function should be decorated with validation decorator in future,
                    to make code easier and smaller

        """

        owner_id = self._validate_token(data.pop('token'), data.pop('username'))

        if owner_id:
            # if provided user name and user id is same as in decoded token that verification is successful
            data["owner"] = self._db.get_entry("users", {"id": owner_id})
            data["project"] = self._db.get_entry("projects", {"id": data['project']})
            response = self._project_handler.change_task(data)

        else:
            response = {"result": 'Fail', "error": 'Auth error'}

        return response