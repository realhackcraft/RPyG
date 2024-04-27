"""
Manage the display buffer to prevent stuttering
"""
class DisplayManager:
    def __init__(self):
        self.buffer = ""

    def add_to_buffer(self, string: str, end: str="\n"):
        self.buffer += string + end

    def flush_buffer(self):
        print(self.buffer, end="", flush=True)
        self.buffer = ""
