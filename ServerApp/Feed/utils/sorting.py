class Sorting:
    @staticmethod
    def sort_by_date(data):
        return sorted(data, key=lambda x: x['created_at'], reverse=True)