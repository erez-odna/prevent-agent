from pathlib import Path
from dotenv import load_dotenv, dotenv_values


class AppSettings:
    dotenv_path = str(Path(__file__).parent.parent.joinpath(".env"))
    load_dotenv(dotenv_path=dotenv_path, verbose=True)

    @staticmethod
    def loadenv():
        print("Environment variables:")
        print("--------------------------")
        print(dotenv_values())
        print("--------------------------")
