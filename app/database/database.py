from yaml import safe_dump, safe_load


class DataBase:
    def __init__(self, file_name):
        self.file_name = file_name

    def dump_data(self, dict_to_save):
        with open(self.file_name, 'w') as file:
            safe_dump(dict_to_save, file, default_flow_style=False)

    def load_data(self):
        with open(self.file_name) as file:
            return safe_load(file)

    def update_data(self, dict_to_add):
        with open(self.file_name, 'a') as file:
            safe_dump(dict_to_add, file, default_flow_style=False)
