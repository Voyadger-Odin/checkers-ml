import random
import time

from game.game import Player


class Balvan(Player):
    def __init__(
            self,
            name: str = '',
            sleep: float = 0,
            isRequiredSteps: bool = True
    ):
        self.SLEEP = sleep
        self.IS_REQUIRED_STEPS = isRequiredSteps
        self.setName(name)

    def play(self, playerColor: str):
        time.sleep(self.SLEEP)

        requiredSteps = []
        if (self.IS_REQUIRED_STEPS):
            if not(self.GAME.isRequiredStepItem is None):
                requiredSteps = self.GAME.requiredStepsForItem(
                    playerColor=playerColor,
                    x=self.GAME.isRequiredStepItem[0],
                    y=self.GAME.isRequiredStepItem[1]
                )
            else:
                requiredSteps = self.GAME.requiredStepsForPlayer(playerColor=playerColor)

        if (len(requiredSteps) > 0):
            stepAble = requiredSteps[random.randint(0, len(requiredSteps) - 1)]
            stepResult = self.GAME.setStep(playerColor=playerColor, x1=stepAble[0], y1=stepAble[1], x2=stepAble[2], y2=stepAble[3])
        else:
            x1 = 0
            y1 = 0
            stepsAble  = []

            while len(stepsAble) == 0:
                x1 = random.randint(0, 7)
                y1 = random.randint(0, 7)
                while (self.GAME.checkPlayerItem(self.GAME.place[y1][x1]) != playerColor):
                    x1 = random.randint(0, 7)
                    y1 = random.randint(0, 7)

                stepsAble = self.GAME.checkStepAble(playerColor=playerColor, x=x1, y=y1)

            stepAble = stepsAble[random.randint(0, len(stepsAble) - 1)]
            stepResult = self.GAME.setStep(playerColor=playerColor, x1=x1, y1=y1, x2=stepAble[0], y2=stepAble[1])

        return stepResult
