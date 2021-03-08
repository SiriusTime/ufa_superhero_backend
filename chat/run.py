from main import Main
from .main import DataChat

import asyncio


if __name__ == "__main__":
    asyncio.Task(DataChat().validate_task())
    Main()._run()