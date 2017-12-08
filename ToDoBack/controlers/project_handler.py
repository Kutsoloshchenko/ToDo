
from re import compile

FOLDER_REGEX = compile(r"[a-zA-Z0-9-_. ]+")

class ProjectHandler:
    def __init__(self, data_base):
        self._db = data_base

    def create_project(self, dict_attributes):

        check_dict = {"owner": dict_attributes['owner'], "name": dict_attributes['name']}

        response = self._create_item("projects", check_dict, dict_attributes)
        return response

    def create_task(self, dict_attributes):

        check_dict = {"project": dict_attributes['project'], "name": dict_attributes['name']}

        response = self._create_item("tasks", check_dict, dict_attributes)
        return response

    def _create_item(self, db_alias, validate_dict, dict_attributes):

        validation_responce = self._validate_name(db_alias, validate_dict, dict_attributes['name'])

        if validation_responce['result'] == 'Ok':
            self._db.add_entry(db_alias, dict_attributes)

        return validation_responce

    def _validate_name(self, db_alias, validate_dict, name):
        fullmatch = FOLDER_REGEX.fullmatch(name)

        if not fullmatch:
            return {"result": "Fail", "error": "Name contains invalid characters"}
        elif fullmatch and self._db.contains(db_alias, validate_dict):
            return {"result": "Fail", "error": "Album with specified name already exists"}
        else:
            return {"result": "Ok"}