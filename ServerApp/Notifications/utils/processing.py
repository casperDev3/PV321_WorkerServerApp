class Processing:
    def __init__(self, data, params):
        self.filter_params = None
        self.sort_params = None
        self.data = data
        self.params = params

        # Call the separate_params method
        self.separate_params()

    def separate_params(self):
        self.sort_params = [{"title": self.params.get("sort[title]", None)}]
        self.filter_params = [{"content_$in": self.params.get("filter[content][$in]", None)}]
        pass

    def apply_sort(self, data):
        if self.sort_params:
            sort_key = self.sort_params[0].get("title", None)
            if sort_key == "asc":
                data = sorted(data, key=lambda x: x["title"])
            elif sort_key == "desc":
                data = sorted(data, key=lambda x: x["title"], reverse=True)
        return data

    def apply_filter(self, item):
        if self.filter_params:
            for filter_item in self.filter_params:
                for key, value in filter_item.items():
                    if value:
                        if key == "content_$in":
                            if value in item["content"]:
                                return True
                            else:
                                return False

    def process_data(self):
        filtered_data = [item for item in self.data if self.apply_filter(item)]
        return self.apply_sort(filtered_data)

