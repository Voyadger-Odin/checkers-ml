from game.game import Player

import torch
print('torch')

# STATUS_CODES = {
#     -1: '',
#     0: 'Успешный ход',
#     1: 'Побита фигура противника',
#     2: 'Пустая клетка',
#     3: 'Чужая фигура',
#     4: 'Ход назад',
#     5: 'Невозможный ход',
#     6: 'Клетка занята',
#     7: 'Необходимо побить фигуру соперника',
#     8: 'Необходимо добить все фигуры',
# }

class Megamozg(Player):
    def __init__(
            self,
            name: str = ''
    ):
        self.setName(name)

    def play(
            self,
            playerColor: str
    ):
        x1, y1, x2, y2 = 0, 0, 0, 0

        # CODE HERE
        place = []
        for row in self.GAME.place:
            place += row
        print(place)
        # place = torch.tensor(place) + 0.
        print(place)
        # exit()

        stepResult = self.GAME.setStep(playerColor=playerColor, x1=x1, y1=y1, x2=x2, y2=y2)
        return stepResult
