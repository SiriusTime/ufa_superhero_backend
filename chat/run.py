from main import MainMixin
#  import asyncio  TODO for tasks


class Main(MainMixin):
    async def task_checkout(self):
        pass


if __name__ == "__main__":
    Main()._run()