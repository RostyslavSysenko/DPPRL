    # Uses code from: # Frequency Finder # http://inventwithpython.com/hacking (BSD Licensed)
    # frequency taken from http://en.wikipedia.org/wiki/Letter_frequency

"""
frequency comparison - count each duplicate occurence of a bloom filter encoding
Try a dictionary attack
compare with various datasets such as city populations, zipcode populations, common first name and common last name
find real data and compare your results (see how accurate your guesses were)

You guys know more about this than I do, maybe there is a way to figure out what a single bit might represent to completely decode them? Try a letter frequency attack.
Add to this code rather than replacing it, I know it's not exactly what you need but it's a good place to start.
"""


class frequencyAttack:
    def __init__(self) -> None:
        self.englishLetterFreq = {'E': 12.70, 'T': 9.06, 'A': 8.17, 'O': 7.51, 'I': 6.97, 'N': 6.75, 'S': 6.33, 'H': 6.09, 'R': 5.99, 'D': 4.25, 'L': 4.03, 'C': 2.78, 'U': 2.76, 'M': 2.41, 'W': 2.36, 'F': 2.23, 'G': 2.02, 'Y': 1.97, 'P': 1.93, 'B': 1.29, 'V': 0.98, 'K': 0.77, 'J': 0.15, 'X': 0.15, 'Q': 0.10, 'Z': 0.07}

        self.commonLetters = 'ETAOINSHRDLCUMWFGYPBVKJXQZ'

        self.LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


    def getFreqCount(self,message,key):
    # Returns a dictionary with key of every letter and value counting their frequency
    # count of how many times they appear in the message parameter.


    # The word letter in this code can be substituted for any string (works for names)
        assert type(key) == list

        freqCount = {}
        for letter in key:
            # Set
            freqCount[letter] = 0
        print(freqCount)



        for letter in message.upper():
            if letter in self.LETTERS:
                freqCount[letter] += 1

        print(freqCount)

        return freqCount

    def getItemAtIndexZero(x):
        return x[0]

    def getFrequencyOrder(self,message):
    # Returns a string of the alphabet letters arranged in order of most
    # frequently occurring in the message parameter.
    # first, get a dictionary of each letter and its frequency count

        letterToFreq = self.getLetterCount(message)

    # second, make a dictionary of each frequency count to each letter(s) with that frequency

        freqToLetter = {}

        for letter in self.LETTERS:

                if letterToFreq[letter] not in freqToLetter:
                    freqToLetter[letterToFreq[letter]] = [letter]

                else:
                    freqToLetter[letterToFreq[letter]].append(letter)

        # third, put each list of letters in reverse "ETAOIN" order, and then convert it to a string

        for freq in freqToLetter:
            freqToLetter[freq].sort(key=self.commonLetters.find, reverse=True)
            freqToLetter[freq] = ''.join(freqToLetter[freq])

    # fourth, convert the freqToLetter dictionary to a list of tuple pairs (key, value), then sort them
        freqPairs = list(freqToLetter.items())
        freqPairs.sort(key=self.getItemAtIndexZero(), reverse=True)



        # fifth, now that the letters are ordered by frequency, extract all

        # the letters for the final string
        freqOrder = []

        for freqPair in freqPairs:
            freqOrder.append(freqPair[1])
        
        return ''.join(freqOrder)





    def englishFreqMatchScore(self,message):

    # Return the number of matches that the string in the message
    # parameter has when its letter frequency is compared to English
    # letter frequency. A "match" is how many of its six most frequent
    # and six least frequent letters is among the six most frequent and
    # six least frequent letters for English.

        freqOrder = self.getFrequencyOrder(message)    
        matchScore = 0

        # Find how many matches for the six most common letters there are.

        for commonLetter in self.commonLetters[:6]:
            if commonLetter in freqOrder[:6]:
                matchScore += 1

        # Find how many matches for the six least common letters there are.

        for uncommonLetter in self.commonLetters[-6:]:
            if uncommonLetter in freqOrder[-6:]:
                matchScore += 1

        return matchScore

def main():
    LETTERS = 'A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W,X,Y,Z'
    letterKey = LETTERS.split(',')

    freq = frequencyAttack()
    freq.getFreqCount(freq.LETTERS,letterKey)



if __name__ == "__main__":
    main()