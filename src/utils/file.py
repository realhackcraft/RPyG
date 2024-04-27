class FileUtils:
    @staticmethod
    def parse_colors(text: str):
        color_dict = {}
        with open(text, "r") as color_file:
            for line in color_file:
                key, value = line.strip().split(" ")
                color_dict[key] = f"\033[{value}m"
        return color_dict
