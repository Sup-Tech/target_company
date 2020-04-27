class StyleTool:

    @staticmethod
    def readQSS(style_file):
        with open(style_file, 'r') as f:
            return f.read()
