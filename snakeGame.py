# Screen resolution - 1920x1080

# Imports
from tkinter import Tk, Canvas, PhotoImage, Entry
import random
from os import path
import re

# Functions


def validateCode(code):
    # Checks for cheat codes - 'DRUNK' or 'BABY'
    regex = "^DRUNK$|^BABY$"
    found = re.search(regex, code)
    if found:
        return True
    else:
        return False


def submitCheatCode(event):
    global cheatCodeEntered, cheatCodeApplied

    # Checks if the user inputted cheat code is valid
    cheatCodeEntered = True
    cheatCode = cheatEntry.get()
    focusOnCanvas(event)  # Escapes input box
    validCode = validateCode(cheatCode)

    if validCode:
        if cheatCode == "DRUNK":
            # Applies 'DRUNK' cheat code
            global snakeSpeed
            snakeSpeed = 180
        elif cheatCode == "BABY":
            # Applies 'BABY' cheat code
            global snake, direction
            for item in snake:
                gameCanvas.delete(item)
            snake = []
            snake.append(
                gameCanvas.create_rectangle(
                    snakeSize,
                    snakeSize,
                    snakeSize * 2,
                    snakeSize * 2,
                    fill=colours[snakeColour]))  # Creates snake head
            direction = "right"

        # Finalises the application of the cheat code (updates variable and
        # response text)
        global cheatCodeApplied, appliedCodeText
        cheatCodeApplied = True
        codeResponseTxt = "Cheat code applied!"

    else:
        # Cheat code not valid
        codeResponseTxt = "Incorrect cheat code, try again!"

    gameCanvas.itemconfigure(
        codeResponseText,
        fill=colours[textColour],
        text=codeResponseTxt)


def focusOnCanvas(event):
    global cheatEntry, cheatEntryBox
    if paused:
        # Escapes cheat input box
        gameCanvas.delete(cheatEntryBox)
        cheatEntry = Entry(gameCanvas)
        cheatEntryBox = gameCanvas.create_window(
            width / 2, (height / 2) + 57,
            window=cheatEntry, height=20, width=100)
        gameCanvas.focus_set()
        bindBossKey()  # Rebinds boss key


def validateName(name):
    # Checks for a space in the name
    found = re.search(" ", name)
    if found:
        return False  # Space found so not a valid name
    else:
        return True  # No space found so it is a valid name


def createLeaderboard():
    # Finds out of leaderboard text file already exists
    leaderboardExists = path.exists("leaderboard.txt")

    if not leaderboardExists:
        # Creates a new leadboard file
        linesList = [
            "Computer 1000\n",
            "Computer 800\n",
            "Computer 600\n",
            "Computer 400\n",
            "Computer 200\n"]
        leaderboard = open("leaderboard.txt", "w")
        leaderboard.writelines(linesList)
        leaderboard.close()


def updateLeaderboard(name):
    newEntry = name + " " + str(score) + "\n"  # Produces new leaderboard entry

    # Finds correct position in leaderboard for new score
    position = 0
    while True:
        if score > leaderboardScores[position]:
            break
        else:
            position += 1

    # Gets old contents of leaderboard
    leaderboard = open("leaderboard.txt", "r")
    linesList = leaderboard.readlines()
    leaderboard.close()

    # Shifts leaderboard entries down a position to make space for the new
    # entry
    for i in range(4, position, -1):
        linesList[i] = linesList[i - 1]

    linesList[position] = newEntry  # Adds new entry to leaderboard list

    # Updates the contents of the leaderboard text file
    leaderboard = open("leaderboard.txt", "w")
    leaderboard.writelines(linesList)
    leaderboard.close()


def bindBossKey():
    window.bind("b", bossKey)


def resetGame():
    global gameStatus, snake, direction, score, snakeSpeed

    # Removes items from game canvas (so canvas is ready for next game)
    gameCanvas.delete(
        gameOverText,
        mainMenuText,
        food,
        leaderboardTitleText,
        leaderboardWorthyText1,
        leaderboardWorthyText2)
    for item in snake:
        gameCanvas.delete(item)
    for item in leaderboardScoreText:
        gameCanvas.delete(item)
    if leaderboardUpdate:
        gameCanvas.delete(nameEntryBox)
        bindBossKey()  # Rebinds boss key

    # Resets various game variables
    gameStatus = "menu"
    snake = []
    direction = "right"
    score = 0
    snakeSpeed = 90

    gameCanvas.pack_forget()  # Hides game canvas


def entryBoxSelected(event):
    window.unbind("b")


def gameEnd():
    global gameStatus, gameOverText, nameEntryBox, mainMenuText
    global leaderboardTitleText, leaderboardScoreText, leaderboardScores
    gameStatus = "finished"

    # Game over text
    gameOverTxt = "Game Over"
    gameOverText = gameCanvas.create_text(
        width / 2,
        (height / 2) - 165,
        fill=colours[textColour],
        font="Times 20 italic bold",
        text=gameOverTxt)

    # Leaderboard display
    leaderboardTitleTxt = "Leaderboard"
    leaderboardTitleText = gameCanvas.create_text(
        width / 2,
        (height / 2) - 105,
        fill=colours[textColour],
        font="Times 15",
        text=leaderboardTitleTxt)

    # Getting contents from the text file
    leaderboard = open("leaderboard.txt", "r")
    position = (height / 2) - 75
    counter = 1
    leaderboardScoreText = []
    leaderboardScores = []
    # Iterates through and displays each item in the leaderboard
    for line in leaderboard:
        leaderboardScoreTxt = str(counter) + ". " + line
        leaderboardScoreText.append(
            gameCanvas.create_text(
                width / 2,
                position,
                fill=colours[textColour],
                font="Times 14",
                text=leaderboardScoreTxt))
        position += 20
        counter += 1

        # Adds scores to list for comparison later
        item = line.split(" ")
        item = item[1].strip("\n")
        leaderboardScores.append(int(item))

    leaderboard.close()

    # Checking if leaderboard needs updating
    global leaderboardUpdate, leaderboardWorthyText1
    global leaderboardWorthyText2, nameEntry
    leaderboardUpdate = False
    if score > leaderboardScores[4]:
        # New leaderboard entry
        leaderboardUpdate = True
        leaderboardWorthyTxt1 = "Your score made it on the leaderboard! Enter a name"
        leaderboardWorthyTxt2 = "below and return to the main menu for your score to be added."
        nameEntry = Entry(gameCanvas)
        # Unbinds boss key whilst typing a name
        nameEntry.bind("<FocusIn>", entryBoxSelected)
        nameEntryBox = gameCanvas.create_window(
            width / 2, height / 2 + 105, window=nameEntry, height=25, width=100)
    else:
        # No new leaderboard entry
        leaderboardWorthyTxt1 = "Sadly, your score did not make it onto the leaderboard."
        leaderboardWorthyTxt2 = "Go to the main menu to try again!"

    # Displays text objects
    leaderboardWorthyText1 = gameCanvas.create_text(
        width / 2,
        (height / 2) + 45,
        fill=colours[textColour],
        font="Times 15",
        text=leaderboardWorthyTxt1)
    leaderboardWorthyText2 = gameCanvas.create_text(
        width / 2,
        (height / 2) + 75,
        fill=colours[textColour],
        font="Times 15",
        text=leaderboardWorthyTxt2)

    # Main menu button
    mainMenuTxt = "Main Menu"
    mainMenuText = gameCanvas.create_text(
        width / 2,
        (height / 2) + 165,
        fill=colours[textColour],
        activefill="steel blue",
        font="Times 20 italic bold",
        text=mainMenuTxt)
    gameCanvas.tag_bind(mainMenuText, "<Button-1>", backToMenu)


def bossKey(event):
    global bossActive

    # Computers screen size
    ws = window.winfo_screenwidth()
    hs = window.winfo_screenheight()

    # Boss key acivation
    if not bossActive:
        bossActive = True

        # Makes appropriate changes to window for the boss screen
        window.title("Graph")
        bossWidth = 690
        bossHeight = 459
        x = (ws / 2) - (bossWidth / 2)
        y = (hs / 2) - (bossHeight / 2)
        window.geometry('%dx%d+%d+%d' % (bossWidth, bossHeight, x, y))

        # Activation if game is in progress - hides appropriate canvases
        if gameStatus == "menu":
            menuCanvas.pack_forget()
            instructionCanvas.pack_forget()
            customiseCanvas.pack_forget()
            cheatCanvas.pack_forget()
        elif gameStatus == "game":
            # Pauses the game if the boss key is pressed when the game is
            # running
            if not paused:
                pauseGame()
            unbindGameKeys()
            gameCanvas.pack_forget()
        else:
            gameCanvas.pack_forget()

        bossCanvas.pack()  # Shows boss screen

    # Boss key deactivation
    else:
        bossActive = False
        # Makes appropriate changes to window for the game screen
        window.title("Snake Game")
        x = (ws / 2) - (width / 2)
        y = (hs / 2) - (height / 2)
        window.geometry('%dx%d+%d+%d' % (width, height, x, y))

        bossCanvas.pack_forget()  # Hides boss screen

        # Returns to appropriate canvases
        if gameStatus == "menu":
            mainMenu()
        elif gameStatus == "game":
            bindGameKeys()
            gameCanvas.pack()
        else:
            gameCanvas.pack()


def changeTextColour(event):
    global textColour
    # Changes text colour according to its current value
    if textColour == 3:
        textColour = 0
    else:
        textColour += 1

    customisePage(event)  # Returns back to the customise page


def changeSnakeColour(event):
    global snakeColour
    # Changes snake colour according to its current value
    if snakeColour == 3:
        snakeColour = 0
    else:
        snakeColour += 1

    customisePage(event)  # Returns back to the customise page


def mainMenu(firstTime=False):
    global playText, instructionsText, controlsText, leaderboardText
    global customiseText, cheatCodesText, quitText
    # Clears main menu canvas (in case there has been a text colour change)
    if firstTime is False:
        menuCanvas.delete(
            playText,
            instructionsText,
            controlsText,
            leaderboardText,
            customiseText,
            cheatCodesText,
            quitText)

    # Play button
    playTxt = "Play"
    playText = menuCanvas.create_text(
        width / 2,
        (height / 2) - 90,
        fill=colours[textColour],
        activefill="steel blue",
        font="Times 20 italic bold",
        text=playTxt)

    # Instructions button
    instructionsTxt = "How to Play"
    instructionsText = menuCanvas.create_text(
        width / 2,
        (height / 2) - 60,
        fill=colours[textColour],
        activefill="steel blue",
        font="Times 20 italic bold",
        text=instructionsTxt)

    # Controls button
    controlsTxt = "Controls"
    controlsText = menuCanvas.create_text(
        width / 2,
        (height / 2) - 30,
        fill=colours[textColour],
        activefill="steel blue",
        font="Times 20 italic bold",
        text=controlsTxt)

    # Leaderboard button
    leaderboardTxt = "Leaderboard"
    leaderboardText = menuCanvas.create_text(
        width / 2,
        (height / 2),
        fill=colours[textColour],
        activefill="steel blue",
        font="Times 20 italic bold",
        text=leaderboardTxt)

    # Customise button
    customiseTxt = "Customise Game"
    customiseText = menuCanvas.create_text(
        width / 2,
        (height / 2) + 30,
        fill=colours[textColour],
        activefill="steel blue",
        font="Times 20 italic bold",
        text=customiseTxt)

    # Cheat codes button
    cheatCodesTxt = "Cheat Codes"
    cheatCodesText = menuCanvas.create_text(
        width / 2,
        (height / 2) + 60,
        fill=colours[textColour],
        activefill="steel blue",
        font="Times 20 italic bold",
        text=cheatCodesTxt)

    # Quit button
    quitTxt = "Quit"
    quitText = menuCanvas.create_text(
        width / 2,
        (height / 2) + 90,
        fill=colours[textColour],
        activefill="steel blue",
        font="Times 20 italic bold",
        text=quitTxt)

    # Binds buttons to the appropriate functions when left clicked
    menuCanvas.tag_bind(playText, "<Button-1>", play)
    menuCanvas.tag_bind(instructionsText, "<Button-1>", instructionPage)
    menuCanvas.tag_bind(controlsText, "<Button-1>", controlsPage)
    menuCanvas.tag_bind(leaderboardText, "<Button-1>", leaderboardPage)
    menuCanvas.tag_bind(customiseText, "<Button-1>", customisePage)
    menuCanvas.tag_bind(cheatCodesText, "<Button-1>", cheatPage)
    menuCanvas.tag_bind(quitText, "<Button-1>", quit)
    menuCanvas.focus_set()

    menuCanvas.pack()  # Packs objects onto the menu canvas


def quit(event):
    window.destroy()


def cheatPage(event):
    menuCanvas.pack_forget()  # Hides main menu canvas

    # Clears cheat canvas (in case there has been a text colour change)
    cheatCanvas.delete("all")

    # Title for cheat canvas
    cheatCodesTitleTxt = "Cheat codes for the game:"
    cheatCodesTitleText = cheatCanvas.create_text(
        width / 2,
        (height / 2) - 75,
        fill=colours[textColour],
        font="Times 20 italic bold",
        text=cheatCodesTitleTxt)

    # Cheat code 1
    cheatCode1Txt = "Slow the snake down: DRUNK"
    cheatCode1Text = cheatCanvas.create_text(
        width / 2,
        (height / 2) - 15,
        fill=colours[textColour],
        font="Times 15",
        text=cheatCode1Txt)

    # Cheat code 2
    cheatCode2Txt = "Reset snake to initial size: BABY"
    cheatCode2Text = cheatCanvas.create_text(
        width / 2,
        (height / 2) + 15,
        fill=colours[textColour],
        font="Times 15",
        text=cheatCode2Txt)

    # Back button
    backTxt = "Back"
    backText = cheatCanvas.create_text(
        width / 2,
        (height / 2) + 75,
        fill=colours[textColour],
        activefill="steel blue",
        font="Times 20 italic bold",
        text=backTxt)
    # Gives action to the back button
    cheatCanvas.tag_bind(backText, "<Button-1>", backToMenu)

    cheatCanvas.pack()  # Packs objects onto the cheat page canvas


def customisePage(event):
    menuCanvas.pack_forget()  # Hides main menu canvas

    # Clears customise canvas (in case there has been a text colour change)
    customiseCanvas.delete("all")

    # Title for the customise canvas
    customiseTitleTxt = "Customise the game:"
    customiseTitleText = customiseCanvas.create_text(
        width / 2,
        (height / 2) - 105,
        fill=colours[textColour],
        font="Times 20 italic bold",
        text=customiseTitleTxt)

    # Changing text colour button
    textColourTxt = "Click to change the text colour"
    textColourText = customiseCanvas.create_text(
        width / 2,
        (height / 2) - 45,
        fill=colours[textColour],
        activefill="steel blue",
        font="Times 15",
        text=textColourTxt)
    customiseCanvas.tag_bind(
        textColourText,
        "<Button-1>",
        changeTextColour)  # Changes text colour on click

    # Changing snake colour text and button
    currentSnakeColourTxt = "The current snake colour is: " + \
        colours[snakeColour]
    currentSnakeColourText = customiseCanvas.create_text(
        width / 2,
        (height / 2),
        fill=colours[textColour],
        font="Times 15",
        text=currentSnakeColourTxt)
    snakeColourChangeTxt = "Click to change the snake colour"
    snakeColourChangeText = customiseCanvas.create_text(
        width / 2,
        (height / 2) + 30,
        fill=colours[textColour],
        activefill="steel blue",
        font="Times 15",
        text=snakeColourChangeTxt)
    customiseCanvas.tag_bind(
        snakeColourChangeText,
        "<Button-1>",
        changeSnakeColour)  # Changes snake colour on click

    # Back button
    backTxt = "Back"
    backText = customiseCanvas.create_text(
        width / 2,
        (height / 2) + 105,
        fill=colours[textColour],
        activefill="steel blue",
        font="Times 20 italic bold",
        text=backTxt)
    # Gives action to the back button
    customiseCanvas.tag_bind(backText, "<Button-1>", backToMenu)

    customiseCanvas.pack()  # Packs objects onto the customise page canvas


def leaderboardPage(event):
    menuCanvas.pack_forget()  # Hides main menu canvas

    global leaderboardScoreText

    # Leaderboard display heading
    leaderboardTitleTxt = "Leaderboard"
    leaderboardTitleText = leaderboardCanvas.create_text(
        width / 2,
        (height / 2) - 105,
        fill=colours[textColour],
        font="Times 20 italic bold",
        text=leaderboardTitleTxt)

    # Getting contents from the text file
    leaderboard = open("leaderboard.txt", "r")
    position = (height / 2) - 45
    counter = 1
    # Iterates through and displays each item in the leaderboard
    for line in leaderboard:
        leaderboardScoreTxt = str(counter) + ". " + line
        leaderboardScoreText.append(
            leaderboardCanvas.create_text(
                width / 2,
                position,
                fill=colours[textColour],
                font="Times 15",
                text=leaderboardScoreTxt))
        position += 30
        counter += 1

    leaderboard.close()

    # Back button
    backTxt = "Back"
    backText = leaderboardCanvas.create_text(
        width / 2,
        (height / 2) + 105,
        fill=colours[textColour],
        activefill="steel blue",
        font="Times 20 italic bold",
        text=backTxt)
    # Gives action to the back button
    leaderboardCanvas.tag_bind(backText, "<Button-1>", backToMenu)

    leaderboardCanvas.pack()  # Packs objects onto the leaderboard page canvas


def instructionPage(event):
    menuCanvas.pack_forget()  # Hides main menu canvas

    # Clears instruction canvas (in case there has been a text colour change)
    instructionCanvas.delete("all")

    # Title for the instruction canvas
    instructionsTitleTxt = "Insutructions:"
    instructionsTitleText = instructionCanvas.create_text(
        width / 2,
        (height / 2) - 165,
        fill=colours[textColour],
        font="Times 20 italic bold",
        text=instructionsTitleTxt)

    # Instruction text
    instructionLine1Txt = "The player controls a square (the snake's head). The snake is"
    instructionLine2Txt = "moving at a constant rate, so use the arrow keys to change the"
    instructionLine3Txt = "direction of the head of the snake. Navigate the head of the snake"
    instructionLine4Txt = "to a 'food' item (a blue square) to eat the food and score some"
    instructionLine5Txt = "points. Eating food results in the snake growing in size. The aim"
    instructionLine6Txt = "of the game is to avoid collision with the body of the snake - this"
    instructionLine7Txt = "becomes progressively more difficult as the snake grows in size."
    instructionLine8Txt = "Good Luck!"

    # Instruction objects
    instructionLine1Text = instructionCanvas.create_text(
        width / 2,
        (height / 2) - 105,
        fill=colours[textColour],
        font="Times 15",
        text=instructionLine1Txt)
    instructionLine2Text = instructionCanvas.create_text(
        width / 2,
        (height / 2) - 75,
        fill=colours[textColour],
        font="Times 15",
        text=instructionLine2Txt)
    instructionLine3Text = instructionCanvas.create_text(
        width / 2,
        (height / 2) - 45,
        fill=colours[textColour],
        font="Times 15",
        text=instructionLine3Txt)
    instructionLine4Text = instructionCanvas.create_text(
        width / 2,
        (height / 2) - 15,
        fill=colours[textColour],
        font="Times 15",
        text=instructionLine4Txt)
    instructionLine5Text = instructionCanvas.create_text(
        width / 2,
        (height / 2) + 15,
        fill=colours[textColour],
        font="Times 15",
        text=instructionLine5Txt)
    instructionLine6Text = instructionCanvas.create_text(
        width / 2,
        (height / 2) + 45,
        fill=colours[textColour],
        font="Times 15",
        text=instructionLine6Txt)
    instructionLine7Text = instructionCanvas.create_text(
        width / 2,
        (height / 2) + 75,
        fill=colours[textColour],
        font="Times 15",
        text=instructionLine7Txt)
    instructionLine8Text = instructionCanvas.create_text(
        width / 2,
        (height / 2) + 105,
        fill=colours[textColour],
        font="Times 15",
        text=instructionLine8Txt)

    # Back button
    backTxt = "Back"
    backText = instructionCanvas.create_text(
        width / 2,
        (height / 2) + 165,
        fill=colours[textColour],
        activefill="steel blue",
        font="Times 20 italic bold",
        text=backTxt)
    # Gives action to the back button
    instructionCanvas.tag_bind(backText, "<Button-1>", backToMenu)

    instructionCanvas.pack()  # Packs objects onto the instruction page canvas


def controlsPage(event):
    menuCanvas.pack_forget()  # Hides main menu canvas

    # Clears customise canvas (in case there has been a text colour change)
    controlsCanvas.delete("all")

    # Title for cheat canvas
    controlsTitleTxt = "Controls"
    controlsTitleText = controlsCanvas.create_text(
        width / 2,
        (height / 2) - 135,
        fill=colours[textColour],
        font="Times 20 italic bold",
        text=controlsTitleTxt)

    # Control 1
    control1Txt = "Move snake head up: Up arrow"
    control1Text = controlsCanvas.create_text(
        width / 2,
        (height / 2) - 75,
        fill=colours[textColour],
        font="Times 15",
        text=control1Txt)

    # Control 2
    control2Txt = "Move snake head left: Left arrow"
    control2Text = controlsCanvas.create_text(
        width / 2,
        (height / 2) - 45,
        fill=colours[textColour],
        font="Times 15",
        text=control2Txt)

    # Control 3
    control3Txt = "Move snake head down: Down arrow"
    control3Text = controlsCanvas.create_text(
        width / 2,
        (height / 2) - 15,
        fill=colours[textColour],
        font="Times 15",
        text=control3Txt)

    # Control 4
    control4Txt = "Move snake head right: Right arrow"
    control4Text = controlsCanvas.create_text(
        width / 2,
        (height / 2) + 15,
        fill=colours[textColour],
        font="Times 15",
        text=control4Txt)

    # Control 5
    control5Txt = "Pause: P"
    control5Text = controlsCanvas.create_text(
        width / 2,
        (height / 2) + 45,
        fill=colours[textColour],
        font="Times 15",
        text=control5Txt)

    # Control 6
    control6Txt = "Boss key: B"
    control6Text = controlsCanvas.create_text(
        width / 2,
        (height / 2) + 75,
        fill=colours[textColour],
        font="Times 15",
        text=control6Txt)

    # Back button
    backTxt = "Back"
    backText = controlsCanvas.create_text(
        width / 2,
        (height / 2) + 135,
        fill=colours[textColour],
        activefill="steel blue",
        font="Times 20 italic bold",
        text=backTxt)
    # Gives action to the back button
    controlsCanvas.tag_bind(backText, "<Button-1>", backToMenu)

    controlsCanvas.pack()  # Packs objects onto the customise page canvas


def play(event):
    menuCanvas.pack_forget()  # Hides the main menu canvas

    gameCanvas.itemconfigure(
        scoreText,
        fill=colours[textColour],
        text="Score: " +
        str(score))  # Updates the colour of the score display text

    snake.append(
        gameCanvas.create_rectangle(
            snakeSize,
            snakeSize,
            snakeSize * 2,
            snakeSize * 2,
            fill=colours[snakeColour]))  # Creates snake head

    # Changes the game status
    global gameStatus
    gameStatus = "game"

    bindGameKeys()  # Calls function to bind the snake movement keys
    placeFood()  # Calls function to generate food
    moveSnake()  # Calls function to move the snake


def backToMenu(event):
    if gameStatus == "menu":
        # Hides other menu canvases
        instructionCanvas.pack_forget()
        controlsCanvas.pack_forget()
        customiseCanvas.pack_forget()
        cheatCanvas.pack_forget()
        leaderboardCanvas.pack_forget()
        for item in leaderboardScoreText:
            # Clears items from leaderboard if they exist
            leaderboardCanvas.delete(item)

    elif gameStatus == "finished":
        # Resets game and hides game canvas
        if leaderboardUpdate:
            # Updating leaderboard
            playerName = nameEntry.get()
            validName = validateName(playerName)
            if validName:
                # Name is valid so leaderboard is updated
                updateLeaderboard(playerName)
                resetGame()
                gameCanvas.pack_forget()
            else:
                # Stays on game over screen and updates text if name invalid
                leaderboardWorthyTxt1 = "Invalid name, try again!"
                leaderboardWorthyTxt2 = "Please input a name without any spaces."
                gameCanvas.itemconfigure(
                    leaderboardWorthyText1,
                    text=leaderboardWorthyTxt1)
                gameCanvas.itemconfigure(
                    leaderboardWorthyText2,
                    text=leaderboardWorthyTxt2)
        else:
            resetGame()
            gameCanvas.pack_forget()

    mainMenu()  # Calls function for main menu canvas


def unbindGameKeys():
    gameCanvas.unbind("<Left>")
    gameCanvas.unbind("<Right>")
    gameCanvas.unbind("<Up>")
    gameCanvas.unbind("<Down>")
    gameCanvas.unbind("p")


def bindGameKeys():
    gameCanvas.bind("<Left>", leftKey)
    gameCanvas.bind("<Right>", rightKey)
    gameCanvas.bind("<Up>", upKey)
    gameCanvas.bind("<Down>", downKey)
    gameCanvas.bind("p", pauseKey)
    gameCanvas.focus_set()  # Keyboard input is directed to the gameCanvas widget


def growSnake():
    lastElement = len(snake) - 1  # Gets last snake element
    # Gets coords of last snake element
    lastElementPos = gameCanvas.coords(snake[lastElement])
    snake.append(
        gameCanvas.create_rectangle(
            0,
            0,
            snakeSize,
            snakeSize,
            fill=colours[snakeColour]))  # Adds new rectangle to snake data structure
    if (direction == "left"):
        gameCanvas.coords(snake[lastElement + 1],
                          lastElementPos[0] + snakeSize,
                          lastElementPos[1],
                          lastElementPos[2] + snakeSize,
                          lastElementPos[3])  # Moves new element to the right of the last element
    elif (direction == "right"):
        gameCanvas.coords(snake[lastElement + 1],
                          lastElementPos[0] - snakeSize,
                          lastElementPos[1],
                          lastElementPos[2] - snakeSize,
                          lastElementPos[3])  # Moves new element to the left of the last element
    elif (direction == "up"):
        gameCanvas.coords(snake[lastElement +
                                1], lastElementPos[0], lastElementPos[1] +
                          snakeSize, lastElementPos[2], lastElementPos[3] +
                          snakeSize)  # Moves new element below the last element
    else:
        # Direction == down
        gameCanvas.coords(snake[lastElement +
                                1], lastElementPos[0], lastElementPos[1] -
                          snakeSize, lastElementPos[2], lastElementPos[3] -
                          snakeSize)  # Moves new element above the last element

    # Increments the score by 10
    global score
    score += 10
    scoreTxt = "Score: " + str(score)  # Creates new text to display
    # Updates the score that is displayed
    gameCanvas.itemconfigure(scoreText, text=scoreTxt)


def moveFood():
    global food, foodX, foodY
    # Moves food back to its original starting point
    gameCanvas.move(food, (foodX * (-1)), (foodY * (-1)))

    # New position of food
    foodX = random.randint(0, width - snakeSize)
    foodY = random.randint(0, height - snakeSize)

    # Moves the food to the generated coordinates
    gameCanvas.move(food, foodX, foodY)


def overlapping(a, b):
    if a[0] < b[2] and a[2] > b[0] and a[1] < b[3] and a[3] > b[1]:  # Checks for collision
        return True  # Collision occurs
    return False  # No collision


def moveSnake():
    gameCanvas.pack()  # Shows game canvas and packs any updates of our objects to the canvas

    # Records the position of the snake's head in a list (so the body can
    # follow)
    positions = []
    positions.append(gameCanvas.coords(snake[0]))

    # What to do if the head reaches a wall
    # Left wall
    if positions[0][0] < 0:
        gameCanvas.coords(
            snake[0],
            width,
            positions[0][1],
            width - snakeSize,
            positions[0][3])
    # Right wall
    elif positions[0][2] > width:
        gameCanvas.coords(
            snake[0],
            0 - snakeSize,
            positions[0][1],
            0,
            positions[0][3])
    # Bottom wall
    elif positions[0][3] > height:
        gameCanvas.coords(
            snake[0],
            positions[0][0],
            0 - snakeSize,
            positions[0][2],
            0)
    # Top wall
    elif positions[0][1] < 0:
        gameCanvas.coords(
            snake[0],
            positions[0][0],
            height,
            positions[0][2],
            height - snakeSize)

    # Reupdates positions of the snake's head
    positions.clear()
    positions.append(gameCanvas.coords(snake[0]))

    # Movement of snake
    if direction == "left":
        gameCanvas.move(snake[0], -snakeSize, 0)
    elif direction == "right":
        gameCanvas.move(snake[0], snakeSize, 0)
    elif direction == "up":
        gameCanvas.move(snake[0], 0, -snakeSize)
    elif direction == "down":
        gameCanvas.move(snake[0], 0, snakeSize)

    # Gets positions of the snake head and the food
    sHeadPos = gameCanvas.coords(snake[0])

    # Checks if the head is on the food
    foodPos = gameCanvas.coords(food)
    if overlapping(sHeadPos, foodPos):
        moveFood()  # Puts the food in a new position
        growSnake()  # Snake gets bigger when it eats the food

    # Checks if the head is on any part of the body
    for i in range(1, len(snake)):
        if overlapping(sHeadPos, gameCanvas.coords(snake[i])):
            gameEnd()

    if (gameStatus == "game") and (
            paused is False):  # Checks if game is complete or paused
        # Repeats the movement function (carries on the game)
        window.after(snakeSpeed, moveSnake)

    # Iterates through remaining elements of snake and adds the positions to
    # the positions list
    for i in range(1, len(snake)):
        positions.append(gameCanvas.coords(snake[i]))

    # Updates the position of each element of snake
    for i in range(len(snake) - 1):
        gameCanvas.coords(snake[i + 1],
                          positions[i][0],
                          positions[i][1],
                          positions[i][2],
                          positions[i][3])


def placeFood():
    global food, foodX, foodY
    food = gameCanvas.create_rectangle(
        0, 0, snakeSize, snakeSize, fill="steel blue")  # Creates food

    # Position of food
    foodX = random.randint(0, width - snakeSize)
    foodY = random.randint(0, height - snakeSize)

    gameCanvas.move(food, foodX, foodY)  # Moves the food to the coordinates


def leftKey(event):
    global direction
    direction = "left"


def rightKey(event):
    global direction
    direction = "right"


def upKey(event):
    global direction
    direction = "up"


def downKey(event):
    global direction
    direction = "down"


def pauseKey(event):
    pauseGame()


def pauseGame():
    global paused, cheatEntry, cheatEntryBox, cheatCodeEntered, cheatCodeApplied
    if gameStatus == "game":
        if not paused:
            # Pauses the game - shows paused text
            paused = True
            gameCanvas.itemconfigure(pauseText1, fill=colours[textColour])
            gameCanvas.itemconfigure(pauseText2, fill=colours[textColour])
            gameCanvas.itemconfigure(cheatCodesText, fill=colours[textColour])
            gameCanvas.itemconfigure(
                cheatSubmitText,
                fill=colours[textColour],
                activefill="steel blue")
            gameCanvas.tag_raise(pauseText1)
            gameCanvas.tag_raise(pauseText2)
            gameCanvas.tag_raise(cheatCodesText)
            gameCanvas.tag_raise(cheatSubmitText)

            gameCanvas.tag_bind(
                cheatSubmitText,
                "<Button-1>",
                submitCheatCode)  # Submits the cheat code on click

            # Creates input box for cheat code
            cheatEntry = Entry(gameCanvas)
            # Unbinds boss key whilst typing a name
            cheatEntry.bind("<FocusIn>", entryBoxSelected)
            cheatEntryBox = gameCanvas.create_window(
                width / 2, (height / 2) + 57, window=cheatEntry, height=20, width=100)
        else:
            # Resumes the game - hides the paused text
            paused = False
            gameCanvas.itemconfigure(pauseText1, fill="black")
            gameCanvas.itemconfigure(pauseText2, fill="black")
            gameCanvas.itemconfigure(cheatCodesText, fill="black")
            gameCanvas.itemconfigure(
                cheatSubmitText, fill="black", activefill="black")
            gameCanvas.tag_lower(pauseText1)
            gameCanvas.tag_lower(pauseText2)
            gameCanvas.tag_lower(cheatCodesText)
            gameCanvas.tag_lower(cheatSubmitText)
            # Deletes entry box for cheat code
            gameCanvas.delete(cheatEntryBox)

            # Removes bind for cheat code submit button
            gameCanvas.tag_unbind(cheatSubmitText, "<Button-1>")

            # Resets cheatCodeEntered and cheatCodeApplied variables
            if cheatCodeEntered:
                if cheatCodeApplied:
                    cheatCodeApplied = False
                cheatCodeEntered = False
                # Hides respective text when a cheat code is enterred
                gameCanvas.itemconfigure(codeResponseText, fill="black")

            moveSnake()  # Calls the move function to resume


def createPauseText():
    global pauseText1, pauseText2, cheatCodesText, cheatSubmitText
    # Text for pause screen which always appears
    pauseTxt1 = "Paused"
    pauseText1 = gameCanvas.create_text(
        width / 2,
        (height / 2) - 30,
        fill="black",
        font="Times 20 italic bold",
        text=pauseTxt1)
    pauseTxt2 = "press 'p' to resume"
    pauseText2 = gameCanvas.create_text(
        width / 2,
        (height / 2),
        fill="black",
        font="Times 20 italic bold",
        text=pauseTxt2)
    cheatCodesTxt = "Enter a cheat code: "
    cheatCodesText = gameCanvas.create_text(
        (width / 2) - 150,
        (height / 2) + 60,
        fill="black",
        font="Times 15 italic bold",
        text=cheatCodesTxt)
    cheatSubmitTxt = "Submit code"
    cheatSubmitText = gameCanvas.create_text(
        (width / 2) + 125,
        (height / 2) + 60,
        fill="black",
        font="Times 15 italic bold",
        text=cheatSubmitTxt)


def setWindowDimensions(w, h):
    window = Tk()  # Create window
    window.title("Snake Game")  # Title of window

    # Computers screen size
    ws = window.winfo_screenwidth()
    hs = window.winfo_screenheight()

    # Calculates centre of screen
    x = (ws / 2) - (w / 2)
    y = (hs / 2) - (h / 2)

    window.geometry('%dx%d+%d+%d' % (w, h, x, y))  # Window size

    return window


# Dimensions of world
width = 550
height = 550

createLeaderboard()  # Creates leaderboard text file if it doesn't already exist

# Creates window and stores to variable 'window'
window = setWindowDimensions(width, height)

# Creates global canvases
menuCanvas = Canvas(window, bg="black", width=width, height=height)
instructionCanvas = Canvas(window, bg="black", width=width, height=height)
controlsCanvas = Canvas(window, bg="black", width=width, height=height)
customiseCanvas = Canvas(window, bg="black", width=width, height=height)
cheatCanvas = Canvas(window, bg="black", width=width, height=height)
gameCanvas = Canvas(window, bg="black", width=width, height=height)
bossCanvas = Canvas(window, bg="black", width=690, height=459)
leaderboardCanvas = Canvas(window, bg="black", width=width, height=height)
blankCanvas = Canvas(window, bg="black", width=width, height=height)

# Creates list of colours for text and snake
colours = ["white", "red", "blue", "green"]
snakeColour = 0
textColour = 0

# Main menu snake images
# Image source: https://pixy.org/4668928/
snakeImg = PhotoImage(file="snake.png")
snakeImg = snakeImg.subsample(30)  # Resizes image
snakeImage1 = menuCanvas.create_image(
    width / 2, 75, image=snakeImg)  # Top snake
snakeImage2 = menuCanvas.create_image(
    width / 2, height - 75, image=snakeImg)  # Bottom snake

# Boss key - status, image and binds key
bossActive = False
# Image source:
# https://commons.wikimedia.org/wiki/File:Bush_approval_ratings_line_graph.png
# (no attribtion is actually required for this image)
bossImg = PhotoImage(file="boss.png")
bossImg = bossImg.subsample(2)
bossImage = bossCanvas.create_image(345, 230, image=bossImg)
bindBossKey()

createPauseText()  # Creates paused text and objects

# Creates snake
snake = []
snakeSize = 15
snakeSpeed = 90

# Initialising variables
score = 0
paused = False
# Used to determine when the game is in progress (3 possibilities -
# "menu", "game" & "finished")
gameStatus = "menu"
leaderboardScoreText = []

# Cheat code variables
cheatCodeEntered = False
cheatCodeApplied = False
codeResponseTxt = ""
codeResponseText = gameCanvas.create_text(
    (width / 2),
    (height / 2) + 90,
    fill="white",
    font="Times 15 italic bold",
    text=codeResponseTxt)

# Creates score text and object
scoreTxt = "Score: " + str(score)
scoreText = gameCanvas.create_text(
    width / 2,
    20,
    fill=colours[textColour],
    font="Times 20 italic bold",
    text=scoreTxt)

direction = "right"  # Initial direction of snake

mainMenu(True)  # First time to main menu so passes true

window.mainloop()  # Displays window
