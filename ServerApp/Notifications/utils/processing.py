import re
from dataclasses import field


class Processing:
    def __init__(self, data, params):
        self.filter_params = []
        self.sort_params = []
        self.data = data
        self.params = params
        self.warnings = []

        # Call the separate_params method
        self._separate_params()


    def _separate_params(self):
        for key, value in self.params.items():
            if match := re.match(r'sort\[(.+?)\]', key):
                field = match.group(1)
                self.sort_params.append({field: value})
            elif match := re.match(r'filter\[(.+?)\]\[(.+?)\]', key):
                field, operation = match.groups()
                self.filter_params.append({f"{field}_{operation}": value})

    def apply_sort(self, data):
        sorted_data = data
        for sort_param in self.sort_params:
            for field, value in sort_param.items():
                if value == "asc":
                    sorted_data = sorted(data, key=lambda x: x[field])
                elif value == "desc":
                    sorted_data = sorted(data, key=lambda x: x[field], reverse=True)
        return sorted_data

    def apply_filter(self, item):
        if not isinstance(item, dict):
            return False
        for filter_item in self.filter_params:
            if not self._match_filter(filter_item, item):
                return False
        return True

    def _match_filter(self, filter_item, item):
        for key, value in filter_item.items():
            field, operation = key.split("_", 1)
            if operation == "$in":
                if value in item[field]:
                    return True
                else:
                    return False
            elif operation == "$eq":
                if item[field] == value:
                    return True
                return False
            else:
                print(f"Operation {operation} is not supported")
                warning = {
                    "message": f"Operation {operation} is not supported",
                    "field": field
                }
                if warning not in self.warnings:
                    self.warnings.append(warning)
                return True
        return True

    def process_data(self):
        filtered_data = [item for item in self.data if self.apply_filter(item)]
        return {
            "data": self.apply_sort(filtered_data),
            "warnings": self.warnings
        }


