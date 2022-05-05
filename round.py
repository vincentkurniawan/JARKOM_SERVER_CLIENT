class Round():
    #constructor
    def __init__(self, question, key, a, b, c, d):
        self.question = question
        self.key = key
        self.a = a
        self.b = b
        self.c = c
        self.d = d


#examples, pls remove afterwards
def main(): 
    #Example of array of rounds
    rounds = [Round("Siapa penemu gravitasi ?", 2, "Albert Einstein", "Isaac Newton", "Duncan Lord", "Kingsman"), 
            Round("Apa nama makanan khas Italia ?", 1, "Pizza", "Burger", "Kentang goreng", "Sushi"),
            Round("question 3 ?", 2, "Albert Einstein", "Isaac Newton", "Duncan Lord", "Kingsman"),
            Round("question 4?", 2, "Albert Einstein", "Isaac Newton", "Duncan Lord", "Kingsman")
            ]
            
    #example on how to get the values
    for i in rounds:
        print( i.question, i.key, sep =' ')


if __name__ == '__main__':
    main()