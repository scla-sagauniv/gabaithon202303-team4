class ExecTime:
    def __init__(self) -> None:
        self.m_range = ['εε', 'εεΎ']
        self.hour = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11']
        self.minute = ['00', '30']

    def merge_list(self):
        return [*self.m_range, *self.hour, *self.minute]
