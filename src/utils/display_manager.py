"""DisplayManager helps with the management of the output buffer"""

class DisplayManager:
    """Manages the output of the program to decrease redraw time"""
    def __init__(self):
        self.buffer = ""

    def add_to_buffer(self, string: str, end: str = "\n"):
        """Adds a string to the buffer"""
        self.buffer += string + end

    def flush_buffer(self):
        """Flushes everything in the buffer to the terminal"""
        print(self.buffer, end="", flush=True)
        self.buffer = ""

    def clear_display(self):
        """Adds a \"clear display\" ANSI escape sequence to the buffer"""
        self.add_to_buffer("\033[H\033[J")
