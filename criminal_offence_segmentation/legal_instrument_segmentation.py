import re


class InstrumentSegmentation(object):
    def __init__(self):
        self.instrument_content = None

    @staticmethod
    def extract_judgement(instrument_path):
        for line in open(instrument_path):
            line = re.sub(r'\s+', '', line)
            if line.startswith("本院认为"):
                return line
        return None
