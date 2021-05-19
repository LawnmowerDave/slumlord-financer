

from transfer import Transfer


class Cost(Transfer):
    
    def __init__(self, name, desc, amount) -> None:
        super().__init__(name, desc, -amount)

