import re
import zipfile


class TextAnalyzer:
    # Class for analyzing a given text
    def __init__(self, text):
        # Initializes the TextAnalyzer with the provided text
        self.text = text

    def count_sentences(self):
        # Counts the number of sentences in the text
        sentences = re.split(r'[.!?]+', self.text)
        num_sentences = 1
        if len(sentences) != 1:
            num_sentences = len(sentences) - 1
        return num_sentences

    def count_narrative_sentences(self):
        # Counts the number of narrative sentences in the text
        narrative_sentences = re.findall(r'[А-ЯA-Z][^.!?]*[.]', self.text)
        num_narrative_sentences = len(narrative_sentences)
        return num_narrative_sentences

    def count_interrogative_sentences(self):
        # Counts the number of interrogative sentences in the text
        interrogative_sentences = re.findall(r'[А-ЯA-Z][^.!?]*[?]', self.text)
        num_interrogative_sentences = len(interrogative_sentences)
        return num_interrogative_sentences

    def count_imperative_sentences(self):
        # Counts the number of imperative sentences in the text
        imperative_sentences = re.findall(r'[А-ЯA-Z][^.!?]*!', self.text)
        num_imperative_sentences = len(imperative_sentences)
        return num_imperative_sentences

    def calculate_average_sentence_length(self):
        # Calculates the average sentence length in the text
        sentences = re.split(r'[.!?]+', self.text)
        num_sentences = len(sentences)
        total_sentences_length = 0
        for sentence in sentences:
            words = re.findall(r'\b\w+\b', sentence)
            total_sentences_length += sum(len(word) for word in words)
        average_sentence_length = total_sentences_length / num_sentences
        return average_sentence_length

    def calculate_average_word_lenght(self):
        # Calculates the average word length in the text
        words = re.findall(r'\b\w+\b', self.text)
        total_word_length = sum(len(word) for word in words)
        average_word_length = total_word_length / len(words)
        return average_word_length

    def count_smileys(self):
        # Counts the number of smileys in the text
        smileys = re.findall(r'[;:]-*[()\[\]]+', self.text)
        num_smileys = len(smileys)
        return num_smileys

    def find_short_words(self):
        # Finds and returns a list of short words in the text
        short_words = re.findall(r'\b\w{1,4}\b', self.text)
        return short_words

    def highlight_text(self):
        # Highlights the text by adding underscores around pairs of consecutive lowercase and uppercase letters
        highlight_pairs_pattern = r'([а-яa-z][А-ЯA-Z])'
        highlighted_text = re.sub(highlight_pairs_pattern, r'_?\1?_', self.text)
        return highlighted_text

    def find_even_words(self):
        # Finds and returns a list of words with an even number of letters in the text
        words = re.findall(r'\b\w+\b', self.text)
        even_words = [word for word in words if len(word) % 2 == 0]
        return even_words

    def find_shorted_word_starting_with_a(self):
        # Finds and returns the shortest word starting with 'a' in the text
        matches = re.findall(r'\b[аa]\w*\b', self.text, re.IGNORECASE)
        shortest_word = min(matches, key=len)
        return shortest_word

    def find_repeated_words(self):
        # Finds and returns a list of repeated words in the text
        words = re.findall(r'\b\w+\b', self.text)
        word_frequency = {}
        for word in words:
            word = word.lower()
            if word in word_frequency:
                word_frequency[word] += 1
            else:
                word_frequency[word] = 1
        repeated_words = [word for word, freq in word_frequency.items() if freq > 1]
        return repeated_words


def write_file(output_file, content):
    # Writes the provided content to the output file
    with open(output_file, "w") as file:
        file.write(content)


def create_zip_archive(output_file, file_to_archive):
    # Creates a zip archive containing the provided file
    with zipfile.ZipFile(output_file, 'w', compression=zipfile.ZIP_DEFLATED) as zip_file:
        zip_file.write(file_to_archive)
        archive_info = zip_file.getinfo(file_to_archive)
        print("Имя файла в архиве: {}".format(archive_info.filename))
        print("Размер сжатого файла: {} байт".format(archive_info.compress_size))
        print("Размер несжатого файла: {} байт".format(archive_info.file_size))
        print("Метод сжатия: {}".format(archive_info.compress_type))


class DataWorker(TextAnalyzer):
    # Class for working with data, inherits from TextAnalyzer
    def __init__(self, input_file, text):
        # Initializes the DataWorker with an input file and text
        super().__init__(text)
        self.input_file = input_file
        self.text = self.read_file()

    def read_file(self):
        # Reads the input file and returns its contents as text
        with open(self.input_file, "r", encoding='utf-8') as file:
            text = file.read()
        return text

    def analyze_text(self):
        # Analyzes the text and returns the analysis results as a string
        num_sentences = self.count_sentences()
        num_narrative_sentences = self.count_narrative_sentences()
        num_interrogative_sentences = self.count_interrogative_sentences()
        num_imperative_sentences = self.count_imperative_sentences()
        average_sentence_length = self.calculate_average_sentence_length()
        average_word_length = self.calculate_average_word_lenght()
        num_smileys = self.count_smileys()
        short_words = self.find_short_words()
        highlighted_text = self.highlight_text()
        even_words = self.find_even_words()
        shortest_word = self.find_shorted_word_starting_with_a()
        repeated_words = self.find_repeated_words()
        output_content = ""
        output_content += "Количество предложений в тексте: {}\n".format(num_sentences)
        output_content += "Количество повествовательных предложений: {}\n".format(num_narrative_sentences)
        output_content += "Количество вопросительных предложений: {}\n".format(num_interrogative_sentences)
        output_content += "Количество побудительных предложений: {}\n".format(num_imperative_sentences)
        output_content += "Средняя длина предложения в символах: {}\n".format(average_sentence_length)
        output_content += "Средняя длина слова в символах: {}\n".format(average_word_length)
        output_content += "Количество смайликов в тексте: {}\n".format(num_smileys)
        output_content += "Список слов длиной менее 5 символов: {}\n".format(short_words)
        output_content += "Выделенный текст: {}\n".format(highlighted_text)
        output_content += "Слова с четным количеством букв: {}\n".format(even_words)
        output_content += "Самое короткое слово, начинающееся на 'a': {}\n".format(shortest_word)
        output_content += "Повторяющиеся слова: {}\n".format(repeated_words)
        return output_content


def task2():
    # Main function for task2
    data_worker = DataWorker("Task2_input.txt", "Task2_output.txt")
    data_worker.analyze_text()
    output_content = data_worker.analyze_text()
    write_file("Task2_output.txt", output_content)

    with open("Task2_output.txt", "r") as file:
        file_content = file.read()
        print(file_content)

    create_zip_archive("Task2_result.zip", "Task2_output.txt")
