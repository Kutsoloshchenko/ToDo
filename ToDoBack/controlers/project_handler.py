
from re import compile
from datetime import date, datetime, timedelta

FOLDER_REGEX = compile(r"[a-zA-Z0-9-_. ]+")

class ProjectHandler:
    def __init__(self, data_base):
        self._db = data_base

    # Handling of user projects

    def create_project(self, dict_attributes):

        check_dict = {"owner": dict_attributes['owner'], "name": dict_attributes['name']}

        response = self._create_item("projects", check_dict, dict_attributes)
        return response

    def change_project(self, dict_attributes):

        check_dict = {"owner": dict_attributes.pop('owner'), "name": dict_attributes['name']}

        id = dict_attributes.pop("id")

        response = self._change_item("projects", check_dict, dict_attributes, {"id": id}, id)
        return response

    def delete_project(self, dict_attributes):

        if self._db.get_entry("tasks",
                              {"project": self._db.get_entry("projects", {"id": dict_attributes['id']}),
                               "state": "In Progress"}):
            response = {"result": 'Fail', "error": 'Project contains task that are in progress and cannot be deleted'}
        else:
            self._db.delete_entry("projects", {"id": dict_attributes['id']})
            response = {"result": "Ok"}

        return response

    def get_projects(self, dict_attributes):
        responce = self._get_multiple_items("projects", dict_attributes)
        if not responce:
            responce = {}

        return responce

    # Handling tasks

    def create_task(self, dict_attributes):
        check_dict = {"project": dict_attributes['project'], "name": dict_attributes['name']}

        response = self._create_item("tasks", check_dict, dict_attributes)
        return response

    def get_tasks_for_today(self, dict_attributes):
        search_dict = {"owner": dict_attributes['owner'],
                       "due_date": date.today()}

        tasks = self._get_multiple_items("tasks", search_dict)

        if tasks:
            return self._sort_tasks_by_state_and_due_date(tasks)
        else:
            return {}

    def get_tasks_for_project(self, dict_attributes):
        search_dict = {"project": dict_attributes['project'],
                       "owner": dict_attributes['owner']}

        tasks = self._get_multiple_items("tasks", search_dict)

        if tasks:
            return self._sort_tasks_by_state_and_due_date(tasks)
        else:
            return [{}]

    def get_tasks_for_7_days(self, dict_attributes):
        search_dict = {"owner": dict_attributes['owner']}

        tasks = self._get_multiple_items("tasks", search_dict)

        tasks = [task for task in tasks if
                 (datetime.strptime(task['due_date'],  "%Y-%m-%d").date() - date.today() <= timedelta(7) and
                  datetime.strptime(task['due_date'], "%Y-%m-%d").date() - date.today() >= timedelta(0))]

        if tasks:
            return self._sort_tasks_by_state_and_due_date(tasks)
        else:
            return {}

    def get_done_tasks(self, dict_attributes):
        search_dict = {"owner": dict_attributes['owner'], "state": "Done"}
        tasks = self._get_multiple_items("tasks", search_dict)

        if tasks:
            return tasks
        else:
            return [{}]

    def delete_task(self, dict_attributes):
        self._db.delete_entry("tasks", {"id": dict_attributes['id']})
        return {"result": "Ok"}

    def change_task(self, dict_attributes):

        check_dict = {"owner": dict_attributes.pop('owner'),
                      "name": dict_attributes['name'],
                      "project": dict_attributes["project"]}

        id = dict_attributes.pop("id")

        response = self._change_item("tasks", check_dict, dict_attributes, {"id": id}, id)
        return response

    def _sort_tasks_by_state_and_due_date(self, tasks):

        tasks = [task for task in tasks if task['state'] != "Done"]

        tasks_upper = sorted([tasks.pop(tasks.index(task)) for
                              task in tasks if
                              ((task["state"] == "In Progress") and
                               (datetime.strptime(task['due_date'],  "%Y-%m-%d").date() < date.today()))],
                             key=lambda x: x['priority'])

        tasks = sorted(tasks, key=lambda x: x['priority'])

        return_list = tasks_upper + tasks

        for task in return_list:
            task['project_name'] = self._db.get_entry("projects", {"id": task["project_id"]}).name

        return return_list

    def _change_item(self, db_alias, validate_dict, dict_attributes, search_dict, id = None):
        validation_responce = self._validate_name(db_alias, validate_dict, dict_attributes['name'], id)

        if validation_responce['result'] == 'Ok':
            self._db.update_entry(db_alias, dict_attributes, search_dict)

        return validation_responce

    def _create_item(self, db_alias, validate_dict, dict_attributes):

        validation_responce = self._validate_name(db_alias, validate_dict, dict_attributes['name'])

        if validation_responce['result'] == 'Ok':
            self._db.add_entry(db_alias, dict_attributes)

        return validation_responce

    def _get_multiple_items(self, db_alias, search_dict):
        return self._db.get_entries(db_alias, search_dict)

    def _validate_name(self, db_alias, validate_dict, name, id= None):
        fullmatch = FOLDER_REGEX.fullmatch(name)

        if not fullmatch:
            return {"result": "Fail", "error": "Name contains invalid characters"}
        elif fullmatch and self._db.contains(db_alias, validate_dict):
            if id:
                if self._db.get_entry(db_alias, {'id': id}).name == name:
                    return {"result": "Ok"}
            return {"result": "Fail", "error": "Item with specified name already exists"}
        else:
            return {"result": "Ok"}