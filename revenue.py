

from transfer import Transfer


class Revenue(Transfer):

    def __init__(self, name, desc, amount) -> None:
        super().__init__(name, desc, amount)
