import random
from collections import defaultdict


"""this is going to be the genetic algo"""
#indxit cannot be in target_word

mutation_percent = 0.05
population_size = 100
keep_how_many = 11 #10 gives us 10^2 - 1 names. We need 11
#target_word = "Hello I hope the length of this is not a matter"
target_word = "school is very hard" #word cuttof after solve??? sometimes the word is cut short?
#fixed the problems, the indxit splits the words at that to avoid conflict with something

indxit = ".$*"
#no numbers,caps,or spaces.. since it splits using spaces
#forgot to add space as a word
#97-122
#32 is space
alphabet = [chr(x) for x in range(97, 123)]
alphabet.append(" ")
#spaces have to be underscores

population = {'sponge': 0}
#quick example
#pop = {"Martin" : 0, "Marcus" : 0, "will" : 0}

def similarity(str1, str2):
    sim = 0
    char_compare = [1 for x in range(0,len(str1)) if str1[x] == str2[x]]
    sim = sum(char_compare)
    return sim

def generate_similarity_scores():
    #don't forget to clear stuff first
    for key, value in population.items():
        population[key] = similarity(target_word, key)

def random_word():
    word = ""
    while len(word) < len(target_word):
        word = word + alphabet[random.randint(0,len(alphabet)-1)]
    return word

#I MADE THIS FOR NOTHING, JUST USE IF IN

def compare_string_list(str1,list_strings):
   return str1 in list_strings

def generate_highest_scores(sum_population):
    takeone = sum_population.popitem()
    random_highest = takeone[0]
    sum_population[random_highest] = takeone[1]
    for key,value in sum_population.items():
        if value > sum_population[random_highest]:
            random_highest = key
    return random_highest

def generate_population(pop_size,pop):
    allkey = pop.keys()
    inner_pop = pop
    while len(pop) < pop_size:
        the_word = random_word()

        if not(compare_string_list(the_word,allkey)):
            inner_pop[the_word] = 0
    return inner_pop

def populate_population(inpu_population):
    new_pop = generate_population(population_size,inpu_population)


    return new_pop





#can't run before population is initialized
#geez this boi is riddled with errors
def generate_top_many(inpupop):
    the_top = []
    priv_population = inpupop.copy()

    while len(the_top) < keep_how_many:

        sco = generate_highest_scores(priv_population)
        the_top.append(sco)
        priv_population.pop(sco)

    return the_top

def mutate_string(str1):
   # char_compare = [alphabet[random.randint(0,len(alphabet) - 1)] for x in range(0, len(str1)) if str1[x] == str2[x]]
    word = ""
    for x in range(0,len(str1)):
        if(random.randint(0,101)/ 100)<=mutation_percent:
            word = word + (alphabet[random.randint(0,len(alphabet) - 1)])
        else:
            word = word + str1[x]
    return word


def mutate_two_strings(str1,str2):
    first_half = str1[0:int(len(str1)/2)]
    second_half = str2[int(len(str2)/2):len(str2)]
    return first_half + second_half

#this takes the best and creates the next generation
#this probably isnt friendly to words with spaces
#this is not freindly with spaces!!!
def make_from_potluck(fittest):
    new_population = {}
    potluck = []
    for x,y in zip(fittest, [x ** 3 for x in range(len(fittest),0,-1)]):
        new_string = x + indxit
        new_string = new_string * y
        new_string = new_string.split(indxit)
        potluck.extend(new_string)

    #print(len(potluck))
    while len(new_population) < population_size:
        #print(len(new_population))
        indx1 = random.randint(0,len(potluck) - 1)
        indx2 = random.randint(0,len(potluck) - 1)
        new_name = mutate_two_strings(potluck[indx1],potluck[indx2])
        new_name = mutate_string(new_name)
        new_population[new_name] = similarity(new_name,target_word)

    #new_population = populate_population(new_population)
    return new_population

# new_population = {name: similarity(name,target_word) for v,name in enumerate(potluck)}

class Evolve:
    mypop = {'sponge': 0}

    def go(self):
        while(not(target_word == generate_highest_scores(self.mypop))):
            #print("here")
            self.mypop = generate_population(population_size,self.mypop)
            #print("there")

            #print(len(generate_top_many(self.mypop)))
            #print(len(make_from_potluck(generate_top_many(self.mypop))))
            newpop = make_from_potluck(generate_top_many(self.mypop))
            #print("again")

            self.mypop = newpop


            current_highest = generate_highest_scores(self.mypop)
            print(current_highest)


my_class = Evolve()


print(mutate_two_strings("hello","suppt"))
#after generating from potluck i want to insert 10 random strings back into the equation
#now i need a create next population and a mutater

my_class.go()
#print(generate_top_many(population))
#print(len(make_from_potluck(generate_top_many(population)))) #this isnt ending
#print(len(populate_population(make_from_potluck(generate_top_many(population)))))
print("yay")








