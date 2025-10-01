print("Bot or Human? Let's figure this out!")
#ask the user for the time at which he received the message
response_hour = float(input("When did you receive your response (type a float between 0 and 24)? "))
#The sender is a bot unless one of the conditions being true changes that
sender_is_bot = True
#check if the hour of response is between 2 and 5 am
if response_hour<2 or response_hour>5:
    #If not in between, ask the user for response time
    response_time = float(input("How long did it take to get your response (in min)? "))
    #convert response time to seconds and check if it is over 9 seconds
    if response_time*60 >=9:
        #if it is, ask user for number of words in response than compute the WPM
        number_of_words = float(input("How many words in your response? "))
        wpm = number_of_words/response_time
        #cehck if wpm is higher than 66
        if wpm >= 66:
            #if it is, ask user for number of typos in answer
            number_of_typos = int(input("How many typos in the response (grammatical errors, misspelled words, etc.)? "))
            #check if number of typos is equal to 0
            if number_of_typos == 0:
                #if it is, ask user to ask the responder how many 't' there are in 'eeooeotetto'
                number_of_t = int(input("Ask the responder how many 't' there are in 'eeooeotetto' and type their answer? "))
                #chekc if answer for number of t is equal to 3
                if number_of_t ==3:
                    #if yes, send is a human if not he is a bot
                    sender_is_bot=False
            #if number of tupos higher than 0, then sender is a human
            else:
                sender_is_bot = False
        #if wpm is less than 66, then sender is a human
        else:
            sender_is_bot = False    
if sender_is_bot == True:
    print("You just talked to a bot")
else:
    print("You just talked to a fellow human")