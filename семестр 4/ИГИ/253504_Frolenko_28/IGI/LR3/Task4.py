import time

def measure_time(func):
    """
    Decorator function to measure the execution time of a function.

    This decorator wraps the input function and measures the time taken for its execution.
    It then prints the execution time in seconds.

    Args:
    - func (function): The function to be decorated.

    Returns:
    - wrapper (function): The wrapper function.
    """
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print("Execution time:", end_time - start_time, "seconds")
        return result
    return wrapper

@measure_time
def Task4():
    """
    Function to process text and perform various operations.

    This function counts the number of words in a text, identifies words with an odd number
    of letters, finds the shortest word starting with 'i', and identifies repeated words.
    It also measures the execution time of the function.

    Args: None

    Returns: None
    """

    text = ("So she was considering in her own mind, as well as she could, for the hot day made her feel very sleepy "
            "and stupid, whether the pleasure of making a daisy-chain would be worth the trouble of getting up and"
            " picking the daisies, when suddenly a White Rabbit with pink eyes ran close by her.")

    words = text.replace(',', '').split()
    odd_length_words = [word for word in words if len(word) % 2 != 0]
    print("Number of words in the string: ", len(words))
    print("Words with an odd number of letters: ", ", ".join(odd_length_words))

    i_words = [word for word in words if word.startswith('i')]
    shortest_i_word = min(i_words, key=len, default=None)
    print("The shortest word starting with 'i': ", shortest_i_word)

    unique_words = set(words)
    repeated_words = {word for word in unique_words if words.count(word) > 1}
    print("Repeated words:", ", ".join(repeated_words))

    for _ in range(10000000):
        pass
