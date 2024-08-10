from game.game import Game
from game.players.balvan import Balvan
from game.players.human import Human
from game.players.megamozg import Megamozg


if __name__ == '__main__':
    IS_REQUIRED_STEPS = True
    IS_PRINT_PLACE = False

    timeSleep = 1 / 2
    timeSleep = 0

    playerBalvan = Balvan(name='Balvan', sleep=timeSleep, isRequiredSteps=IS_REQUIRED_STEPS)
    playerHuman = Human(name='Human')
    playerMegamozg = Megamozg(name='Megamozg')


    for i in range(100):
        print(f'Игра {i + 1}')
        game = Game(
            playerWhite=playerMegamozg,
            playerBlack=playerBalvan,
            isRequiredSteps=IS_REQUIRED_STEPS,
            isPrintPlace=IS_PRINT_PLACE
        )

        game.play()
