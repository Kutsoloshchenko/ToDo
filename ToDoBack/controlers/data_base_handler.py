"""Class that incapsulates work with data base and add layer of abstraction """

from rest_api.models import User, Project, Task
from rest_api.serializer import UserSerializer, ProjectSerializer, TaskSerializer

class DataBaseHandler:

    _ALIASES = {"users": User,
                "projects": Project,
                "tasks": Task}

    _SERIALIZERS = {"users": UserSerializer,
                    "projects": ProjectSerializer,
                    "tasks": TaskSerializer}

    def add_entry(self, alias, dict):
        new_entry = self._ALIASES[alias](**dict)
        new_entry.save()

    def delete_entry(self, alias, dict):
        self._ALIASES[alias].objects.filter(**dict).delete()

    def update_entry(self, alias, upd_dict, search_dict):
        entry = self._ALIASES[alias].objects.filter(**search_dict).first()

        print(self._SERIALIZERS[alias](entry).data)

        for key in upd_dict:
            setattr(entry, key, upd_dict[key])
        entry.save()

    def contains(self, alias, dict):
        entry = self._ALIASES[alias].objects.filter(**dict).first()

        if entry:
            return True
        else:
            return False

    def get_entry(self, alias, dict):
        return self._ALIASES[alias].objects.filter(**dict).first()

    def get_entry_attributes(self, alias, dict, attributes):

        entry = self.get_entry(alias, dict)

        if entry:
            return [getattr(entry, attribute) for attribute in attributes]
        else:
            return None, None

    def get_entries(self, alias, dict):
        entries = self._ALIASES[alias].objects.filter(**dict)

        if entries:
            return [self._SERIALIZERS[alias](entry).data for entry in entries]
        else:
            return None