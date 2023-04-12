import random
from operator import itemgetter
from termcolor import colored
import time

game = True  # allows the game to run


############################################################################################################################

def authentification():
    print(colored("""Welcome to this music game! 
Guess the name of the song - you are given:
Artist name &
First letter of each word of the song""", "magenta", "on_white"))
    intro = input("Would you like to log in or sign up? (l/s) :")
    while intro != "l" and intro != "s":
        intro = input(colored("Type in l for log in or s for sign up :  ", "red"))

    names_file = open("userspasswords.txt")  # opens file and adds contents to a double list
    no_lines = sum(1 for line in open("userspasswords.txt"))
    users_list = []

    for i in range(0, no_lines):
        line = names_file.readline()
        line = line.rstrip()
        users_list.append(line)

    names_file.close()

    if intro == "l":  # logs in the user
        log_in = input("Username: ")
        while log_in not in users_list:
            log_in = input(colored("Invalid user. Please try again: ", "red"))
        password = input("Password: ")
        userindex = users_list.index(log_in)
        passwordindex = userindex + 1
        realpassword = users_list[passwordindex]
        while password != realpassword:
            password = input(colored("Password incorrect. Please try again: ", "red"))

        print(colored("Logging in...", "white", "on_cyan"))

    elif intro == "s":

        log_in = input("Type in a new username:  ")
        while log_in in users_list:
            log_in = input(colored("This username has already been taken:  ", "red"))
        password = input("Create your new password:  ")
        names_file = open("userspasswords.txt", "a")
        names_file.write(log_in)
        names_file.write("\n")
        names_file.write(password)
        names_file.write("\n")
        names_file.close()

    return log_in


############################################################################################################################

def open_songs():
    songs_file = open("songsartists.txt")
    num_lines = sum(1 for line in open("songsartists.txt"))
    song_artist_list = []

    for i in range(0, int(num_lines / 2)):  # storing file contents as a double list
        song_data = []
        song = songs_file.readline()
        song = song.rstrip()
        song_data.append(song)
        artist = songs_file.readline()
        artist = artist.rstrip()
        song_data.append(artist)
        song_artist_list.append(song_data)
    songs_file.close()

    return song_artist_list


############################################################################################################################

def choosing_song(song_artist_list, beenchosen_songs):
    song_no = random.randint(0, len(song_artist_list) - 1)  # picks a random song
    while song_no in beenchosen_songs:  # checks the song has not already been chosen before
        song_no = random.randint(0, len(song_artist_list) - 1)

    song = song_artist_list[song_no][0]
    artist = song_artist_list[song_no][1]

    print("")
    print(artist)
    titles = song.split()  # splits the song title into a list of separate words
    first_letters = []
    for i in titles:
        letter = i[0].upper()  # the first letter of each word in the title
        first_letters.append(letter)
    print(" ".join(first_letters))

    return [song, song_no]


############################################################################################################################

def playing_game(song):
    user_score = 0
    guess = input("Guess the name of the song for 3 points: ").upper()
    if guess == song.upper():
        user_score += 3

    else:
        guess = input("Try again for 1 point:  ").upper()
        if guess == song.upper():
            user_score += 1
        else:

            print(colored("Correct answer: ", "green"), colored(song, "green"))
            return [False, user_score]  # the game returns as false so game over

    return [True, user_score]


############################################################################################################################

def highscores(log_in, user_score):
    print("")  # once the game has ended prints the highscore
    print(colored("Game Over", "white", "on_red", attrs=["bold"]))
    time.sleep(0.5)
    print("Your Score: ", user_score)
    time.sleep(0.5)

    scores_file = open("scores.txt", "a")

    scores_file.write(log_in)  # writes the current user's name and score to the file
    scores_file.write("\n")
    scores_file.write(str(user_score))
    scores_file.write("\n")
    scores_file.close()

    scores_file = open("scores.txt", "r")  # opens file again and appends data to a double list
    file_lines = sum(1 for line in open("scores.txt"))
    score_list = []

    for i in range(0, int(file_lines / 2)):
        score_data = []
        person = scores_file.readline()
        person = person.rstrip()
        score_data.append(person)
        score = scores_file.readline()
        score = score.rstrip()
        score_data.append(int(score))
        score_list.append(score_data)

    score_list = sorted(score_list, key=itemgetter(1), reverse=True)  # arranges the list using the scores

    print("")  # prints the top 5 high score user and the score
    print(colored("High Scores:", attrs=["underline"]))

    try:
        for i in range(0, 5):
            time.sleep(0.2)
            highscore_user = score_list[i][0]
            highscore = score_list[i][1]
            print("No. %s) %s scored %s" % (i + 1, highscore_user, highscore))

    except:
        pass

    scores_file.close()


############################################################################################################################

score = 0
beenchosen_list = []
username = authentification()
game = True

while game == True:
    songlist = open_songs()

    chosensong = choosing_song(songlist, beenchosen_list)
    song_name = chosensong[0]
    beenchosen_list.append(chosensong[1])  # appends the song no. onto the list

    gameresult = playing_game(song_name)
    game = gameresult[0]  # whether game is True or False
    score += gameresult[1]  # calculates the total score

highscores(username, score)  # once the game is false, loop automativally breaks and runs this function
