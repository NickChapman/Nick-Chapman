from hash.linearprobe import LinearProbeHashMap
import argparse, sys, string

def main(argv):
    """ The main program for the spell checker """
    parser = argparse.ArgumentParser(description="Find spelling errors in a text file")
    parser.add_argument('text_file', action="store",
                        help="Text file to check")
    parser.add_argument('dict_file', action="store",
                        help="Dictionary file to check against")
    parser.add_argument('personal_dict', action="store", nargs='?',
                        help="A personal dictionary file")
    files = parser.parse_args(argv)
    
    dictionary = LinearProbeHashMap()
    # Read the first line of the dictionary file to figure out how big our table is
    f = open(files.dict_file, 'r')
    count = f.readline()
    f.close()
    count = count.split("\n")[0]
    try:
        count = int(count)
        dictionary.array = [None] * (count * 2)
    except ValueError:
        # There isn't a number to read so move on
        count = 0

    with open(files.dict_file, 'r') as dict:
        # Skip the first line which we have handled already
        if count != 0:
            next(dict)
        for line in dict:
            word = line.split("/")[0].split("\n")[0]
            dictionary[str(word)] = str(word)

    if files.personal_dict:
        with open(files.personal_dict, 'r') as dict:
            for line in dict:
                word = line.split("/")[0].split("\n")[0]
                dictionary[str(word)] = str(word)

    # Now that everything should be in the dictionary
    # and it's a good size we rehash and keep it at the same size
    # to get the actual collision count
    dictionary.rehash(len(dictionary.array))
    print("Size of hash table: " + str(len(dictionary.array)))
    print("Number of collisions: " + str(dictionary.collisions_found))

    # mispells is a list of tuples that are (word, line number)
    misspells = []
    words_checked = 0
    with open(files.text_file, 'r') as text:
        for line_number, line in enumerate(text):
            # Remove all punctuation 
            punctuation = '!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~\n'
            translation_table = {ord(item) : None for item in punctuation}
            stripped_line = line.translate(translation_table)
            if stripped_line == "":
                continue
            # Split the string apart
            words = stripped_line.split()
            for word in words:
                original = word
                words_checked += 1
                # Check to see if the word exists as it
                try:
                    dictionary[word]
                except KeyError:
                    word = word.lower()
                    try:
                        dictionary[word]
                    except KeyError:
                        # If we still didn't find it then it is a spelling error
                        # Line number + 1 so we get out of computer counting
                        misspells.append((original, line_number + 1))

    print("Number of words checked: " + str(words_checked))
    if len(misspells) > 0:
        print("Misspellings:")
        # Find the longest word and line number
        max_word_len = 0
        max_line_len = 0
        for item in misspells:
            max_word_len = max(len(str(item[0])), max_word_len)
            max_line_len = max(len(str(item[1])), max_line_len)
        # We toss in a bit more room for looks
        max_word_len += 4
        max_line_len += 4
        for item in misspells:
            print("\t" + repr(item[0]).ljust(max_word_len) + " on line " + repr(item[1]).ljust(max_line_len))
        print("Total misspellings: " + str(len(misspells)))
    else:
        print("No misspellings found")
    # Print a couple of blank lines for the looks
    print("\n\n")



if __name__ == "__main__":
    # We make some space between us and the prompt line
    print("\n\n")
    # Split because argv[0] is simply the program name
    main(sys.argv[1:]) 
