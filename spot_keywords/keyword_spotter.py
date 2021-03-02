from flashtext import KeywordProcessor

class AddMultiKeywords:
    def __init__(self, text, keyword_dict):
        self.text = text
        self.keyword_dict = keyword_dict

    def addkey(self):
        keyword_processor = KeywordProcessor()
        keyword_processor.add_keywords_from_dict(self.keyword_dict)
        extracted_keyword = keyword_processor.extract_keywords(self.text)
        return extracted_keyword