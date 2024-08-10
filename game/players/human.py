from game.game import Player


class Human(Player):
    def __init__(
            self,
            name: str = ''
    ):
        self.setName(name)

    def play(
            self,
            playerColor: str
    ):
        step = input(f'Ход {"Белых" if (playerColor == "W") else "Чёрных"}: ')
        setCoords = self.stepConvert(step=step)
        while (setCoords is None):
            print('Неверные координаты')
            step = input(f'Ход {"Белых" if (playerColor == "W") else "Чёрных"}: ')
            setCoords = self.stepConvert(step=step)
        x1, y1, x2, y2 = setCoords[0], setCoords[1], setCoords[2], setCoords[3]
        stepResult = self.GAME.setStep(playerColor=playerColor, x1=x1, y1=y1, x2=x2, y2=y2)
        return stepResult

    def stepConvert(self, step: str):
        xNames = {
            'A': 0,
            'B': 1,
            'C': 2,
            'D': 3,
            'E': 4,
            'F': 5,
            'G': 6,
            'H': 7,
        }

        try:
            stepFrom, stepTo = step.upper().split(' ')
            x1 = xNames[stepFrom[0]]
            y1 = 8 - int(stepFrom[1])
            x2 = xNames[stepTo[0]]
            y2 = 8 - int(stepTo[1])

            if (y1 < 0 or y1 > 7 or y2 < 0 or y2 > 7):
                raise Exception('Out of index', '')

            return (x1, y1, x2, y2)
        except:
            ...

        return None
