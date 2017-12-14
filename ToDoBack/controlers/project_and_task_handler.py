
from re import compile
from datetime import date, datetime, timedelta

NAME_REGEX = compile(r"[a-zA-Z0-9-_. ]+")


class ProjectAndTaskHandler:
    """ Creates, updates, gets and deletes all projects and tasks

        Important note: Probably would be a better idea to create base abstract Handler class,
        and then inherit it with Project handler and Task Handler class, to separate not common functions
    """
    def __init__(self, data_base):
        """Initializing data base orm class instance """
        self._db = data_base

    # Handling of user projects

    def create_project(self, dict_attributes):
        """Creates project with specified parameters

            Params:
                    dict_attributes - dictionary of parameters received from client

            Returns:
                    response dictionary

        """

        # Values to validate
        check_dict = {"owner": dict_attributes['owner'], "name": dict_attributes['name']}

        response = self._create_item("projects", check_dict, dict_attributes)
        return response

    def change_project(self, dict_attributes):
        """Updates project with specified parameters

                    Params:
                            dict_attributes - dictionary of parameters received from client

                    Returns:
                            response dictionary

        """

        # Values to validate
        check_dict = {"owner": dict_attributes.pop('owner'), "name": dict_attributes['name']}

        id = dict_attributes.pop("id")

        response = self._change_item("projects", check_dict, dict_attributes, {"id": id}, id)
        return response

    def delete_project(self, dict_attributes):
        """Deletes project with specified parameters

            Params:
                    dict_attributes - dictionary of parameters received from client

            Returns:
                    response dictionary

        """

        not_done_task = self._db.get_entry("tasks",
                                            {"project": self._db.get_entry("projects",
                                            {"id": dict_attributes['id']}),
                                            "state": "In Progress"})

        # Check that project does not contain tasks that are not finished
        if not_done_task:
            response = {"result": 'Fail', "error": 'Project contains task that are in progress and cannot be deleted'}
        else:
            self._db.delete_entry("projects", {"id": dict_attributes['id']})
            response = {"result": "Ok"}

        return response

    def get_projects(self, dict_attributes):
        """Get all user projects

            Params:
                    dict_attributes - dictionary of parameters received from client

            Returns:
                    list of projects

        """
        responce = self._get_multiple_items("projects", dict_attributes)
        if not responce:
            responce = {}

        return responce

    # Handling tasks

    def create_task(self, dict_attributes):
        """Creates task with specified parameters

            Params:
                    dict_attributes - dictionary of parameters received from client

            Returns:
                    response dictionary

        """
        # Values to validate before creation
        check_dict = {"project": dict_attributes['project'], "name": dict_attributes['name']}

        response = self._create_item("tasks", check_dict, dict_attributes)
        return response

    def get_tasks_for_today(self, dict_attributes):
        """Gets tasks for today

            Params:
                    dict_attributes - dictionary of parameters received from client

            Returns:
                    list of tasks

        """
        search_dict = {"owner": dict_attributes['owner'],
                       "due_date": date.today()}

        tasks = self._get_multiple_items("tasks", search_dict)

        if tasks:
            return self._sort_tasks_by_state_and_due_date(tasks)
        else:
            return {}

    def get_tasks_for_project(self, dict_attributes):
        """Gets tasks for specified project

            Params:
                    dict_attributes - dictionary of parameters received from client

            Returns:
                    list of sorted tasks

        """

        search_dict = {"project": dict_attributes['project'],
                       "owner": dict_attributes['owner']}

        tasks = self._get_multiple_items("tasks", search_dict)

        if tasks:
            return self._sort_tasks_by_state_and_due_date(tasks)
        else:
            return [{}]

    def get_tasks_for_7_days(self, dict_attributes):
        """Gets tasks for tnext 7 days

            Params:
                    dict_attributes - dictionary of parameters received from client

            Returns:
                    list of tasks

        """
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
        """Gets tasks with status Done

            Params:
                    dict_attributes - dictionary of parameters received from client

            Returns:
                    list of tasks

        """
        search_dict = {"owner": dict_attributes['owner'], "state": "Done"}
        tasks = self._get_multiple_items("tasks", search_dict)

        if tasks:
            return tasks
        else:
            return [{}]

    def delete_task(self, dict_attributes):
        """Deletes task with specified parameters

            Params:
                    dict_attributes - dictionary of parameters received from client

            Returns:
                    result

        """
        self._db.delete_entry("tasks", {"id": dict_attributes['id']})
        return {"result": "Ok"}

    def change_task(self, dict_attributes):
        """Updates task with specified parameters

            Params:
                    dict_attributes - dictionary of parameters received from client

            Returns:
                    result

        """

        check_dict = {"owner": dict_attributes.pop('owner'),
                      "name": dict_attributes['name'],
                      "project": dict_attributes["project"]}

        id = dict_attributes.pop("id")

        response = self._change_item("tasks", check_dict, dict_attributes, {"id": id}, id)
        return response

    def _sort_tasks_by_state_and_due_date(self, tasks):
        """ Sorts task by state and due date. All "In Progress" that are due today are moved to the upped part of list.
            Then all tasks are sorted in priority order

            Params:
                    tasks - list of unsorted tasks

            Returns:
                    list of sorted tasks
        """

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

    # Common functions

    def _change_item(self, db_alias, validate_dict, dict_attributes, search_dict, id=None):
        """ Common function that validates name of item and then make changes to a data base entry

            Params:
                    db_alias - name of table to apply changes to
                    validate_dict - dictionary which values to validate
                    dict_attributes - attributes which should be writen to a data base entry
                    search_dict - attributes by which entries are sorted
                    id - optional parameter, that used to make sure that if name of changed item stays the same,
                         validation function would not return error that current item already exists

            Returns:
                    Dictionary with result and error message if applicable

        """

        # validates name
        validation_responce = self._validate_name(db_alias, validate_dict, dict_attributes['name'], id)

        if validation_responce['result'] == 'Ok':
            self._db.update_entry(db_alias, dict_attributes, search_dict)

        return validation_responce

    def _create_item(self, db_alias, validate_dict, dict_attributes):
        """ Common function that validates name of item and then writes entry to a data base

            Params:
                    db_alias - name of table to add entry to
                    validate_dict - dictionary which values to validate
                    dict_attributes - attributes which should be writen to a data base entry
                    search_dict - attributes by which entries are sorted

            Returns:
                    Dictionary with result and error message if applicable

        """

        validation_responce = self._validate_name(db_alias, validate_dict, dict_attributes['name'])

        if validation_responce['result'] == 'Ok':
            self._db.add_entry(db_alias, dict_attributes)

        return validation_responce

    def _get_multiple_items(self, db_alias, search_dict):
        """ Common function that returns list of data base entries

            Params:
                    db_alias - name of table to apply changes to
                    dict_attributes - attributes which should be writen to a data base entry

            Returns:
                    List of deserialized entries

        """
        return self._db.get_entries(db_alias, search_dict)

    def _validate_name(self, db_alias, validate_dict, name, id= None):
        """ Common function that validates name and that it is unic entry

            Params:
                    db_alias - name of table to apply changes to
                    validate_dict - dictionary which values to validate
                    dict_attributes - attributes which should be writen to a data base entry
                    name - name to validate
                    id - optional parameter, that used to make sure that if name of changed item stays the same,
                         validation function would not return error that current item already exists

            Returns:
                    responce item with result and error message if applicable

        """
        fullmatch = NAME_REGEX.fullmatch(name)

        if not fullmatch:
            return {"result": "Fail", "error": "Name contains invalid characters"}
        elif fullmatch and self._db.contains(db_alias, validate_dict):
            if id:
                if self._db.get_entry(db_alias, {'id': id}).name == name:
                    return {"result": "Ok"}
            return {"result": "Fail", "error": "Item with specified name already exists"}
        else:
            return {"result": "Ok"}