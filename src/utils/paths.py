from pathlib import Path


class DataPaths:
    @staticmethod
    def get_temp_results_folder():
        temp_results_folder = (
            Path(__file__).resolve().parent.parent.joinpath(".results")
        )
        DataPaths.check_create_path(temp_results_folder)
        return temp_results_folder

    @staticmethod
    def check_create_path(folder):
        if not folder.is_dir():
            folder.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def get_schema_folder():
        return Path(__file__).resolve().parent.parent.joinpath("endpoints", "schemas")

    @staticmethod
    def get_schema_file(schema_name):
        schema_file = f"{schema_name}.json"
        return Path(DataPaths.get_schema_folder()).joinpath(schema_file)
