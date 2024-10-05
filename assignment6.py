import string
from typing import Dict, Set, List

# StopWords class
class StopWords:
    def __init__(self, filename: str):
        self.stop_words = set()
        try:
            with open(filename, 'r') as file:
                # Reading stopwords, assuming they are stored in lowercase and include necessary punctuation.
                self.stop_words = set(word.strip() for word in file.read().splitlines())
        except FileNotFoundError:
            print(f"The file {filename} was not found. Please check the file path and try again.")
            raise

    def __contains__(self, word: str) -> bool:
        # The check should consider punctuation stripping if it's not already considered in the stopwords file.
        return word in self.stop_words

    def get_content(self) -> Set[str]:
        return self.stop_words

# FileReader class
class FileReader:
    def __init__(self, filename: str, stopwords: StopWords):
        self.filename = filename
        self.stopwords = stopwords
        self.lines = []
        self.wordlist = {}
        translator = str.maketrans('', '', string.punctuation.replace("'", ""))

        with open(filename, 'r') as file:
            self.lines = file.readlines()
            for line in self.lines:
                line = line.strip().lower()
                line = line.translate(translator)
                words = line.split()

                for word in words:
                    if word and word not in stopwords:
                        self.wordlist[word] = self.wordlist.get(word, 0) + 1

    def get_content(self) -> List[str]:
        return self.lines

    def get_wordlist(self) -> Dict[str, int]:
        return self.wordlist

    def get_info(self, **kwargs) -> str:
        # Ignore any additional keyword arguments
        return f"Filename: {self.filename}"

# FileDecorator base class
class FileDecorator:
    def __init__(self, file_reader: FileReader):
        self.file_reader = file_reader

    def get_content(self) -> List[str]:
        return self.file_reader.get_content()

    def get_wordlist(self) -> Dict[str, int]:
        return self.file_reader.get_wordlist()

    def get_info(self, **kwargs) -> str:
        return self.file_reader.get_info(**kwargs)


class SummaryFileDecorator(FileDecorator):
    def get_info(self, **kwargs) -> str:
        content = self.get_content()
        words = ' '.join(content).split()
        character_count = sum(len(line) for line in content)
        return (f"{self.file_reader.get_info(**kwargs)}\n\n"
                f"-- Summary\n"
                f"{len(content)} line(s)\n"
                f"{len(words)} word(s)\n"
                f"{character_count} character(s)")
        base_info = super().get_info(**kwargs)
        # Append the summary information to the base info
        summary_info = f"-- Summary\n{len(self.get_content())} line(s)\n{len(words)} word(s)\n{character_count} character(s)"
        return f"{base_info}\n{summary_info}"


class HeadLinesDecorator(FileDecorator):
    def get_info(self, head_n=10, **kwargs):
        lines_to_show = self.get_content()[:head_n]
        clean_lines = [line.strip() for line in lines_to_show if line.strip()]
        joined_lines = '\n'.join(clean_lines)
        return (f"{self.file_reader.get_info(**kwargs)}\n\n"
                f"-- First {len(clean_lines)} lines\n"
                f"{joined_lines}\n")
        base_info = super().get_info(**kwargs)
        # Append the first N lines info to the base info
        first_lines_info = f"-- First {head_n} lines\n{joined_lines}"
        return f"{base_info}\n{first_lines_info}"


class CommonWordsDecorator(FileDecorator):
    def get_info(self, common_n=10, **kwargs):
        wordlist = self.get_wordlist()
        sorted_words = sorted(wordlist.items(), key=lambda item: (-item[1], item[0]))[:common_n]
        most_common_words = '\n'.join([f"[{i+1}] {word} : {count} times used" for i, (word, count) in enumerate(sorted_words)])
        return (f"{self.file_reader.get_info(**kwargs)}\n\n"
                f"-- {common_n} most common words\n"
                + most_common_words)
        # Include the base info from previous decorators
        base_info = super().get_info(**kwargs)
        # Append the most common words info to the base info
        common_words_info = f"-- 10 most common words\n{most_common_words}"
        return f"{base_info}\n{common_words_info}"


class SearchWordDecorator(FileDecorator):
    def get_info(self, word=None, **kwargs):
        # Get the accumulated information from the previous layers of decoration
        accumulated_info = super().get_info(**kwargs)

        # Construct the search results information
        search_info = f"-- Search results (keyword = '{word}')"

        if word is None:
            # If no keyword is given, append the missing keyword error
            return f"{accumulated_info}\n\n{search_info}\n-- Search error: keyword missing"

        # Perform the search and construct the results string
        search_results = [line for line in self.get_content() if word and word.lower() in line.lower()]
        formatted_results = "\n".join([f"[{index + 1}] {line.strip()}" for index, line in enumerate(search_results)])

        # Add an extra newline character before the search results header
        # Ensure that two newline characters are there if there are no search results
        if not search_results:
            return f"{accumulated_info}\n\n{search_info}\n"
        else:
            # If search results exist, append them after the header
            return f"{accumulated_info}\n\n{search_info}\n{formatted_results}\n"

        
