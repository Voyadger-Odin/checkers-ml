import os

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    LASTSTEP = '\33[44m'
    POWER = '\033[33m'

class Player():
    def play(
            self,
            playerColor: str
    ):
        ...

    def setGame(
            self,
            game
    ):
        self.GAME = game

    def setName(self, name):
        self.NAME = name


class Game():
    def __init__(
            self,
            playerWhite: Player,
            playerBlack: Player,
            isRequiredSteps: bool = True,
            isPrintPlace: bool = True
    ):
        self.PLAYER_WHITE = playerWhite
        self.PLAYER_WHITE.setGame(self)

        self.PLAYER_BLACK = playerBlack
        self.PLAYER_BLACK.setGame(self)

        self.currentPlayer = 'W'
        self.place = [
            [0, 2, 0, 2, 0, 2, 0, 2],
            [2, 0, 2, 0, 2, 0, 2, 0],
            [0, 2, 0, 2, 0, 2, 0, 2],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 1, 0, 1, 0, 1, 0],
            [0, 1, 0, 1, 0, 1, 0, 1],
            [1, 0, 1, 0, 1, 0, 1, 0],
        ]
        # self.place = [
        #     [0, 0, 0, 0, 0, 0, 0, 0],
        #     [0, 0, 0, 0, 0, 0, 0, 0],
        #     [0, 0, 0, 0, 0, 0, 0, 0],
        #     [0, 0, 0, 0, 0, 0, 0, 0],
        #     [0, 0, 0, 0, 0, 0, 0, 0],
        #     [0, 0, 0, 0, 0, 0, 0, 0],
        #     [0, 0, 0, 0, 0, 0, 0, 2],
        #     [0, 0, 0, 0, 0, 0, 1, 0],
        # ]
        self.WHITE_COUNT = 0
        self.BLACK_COUNT = 0
        self.lastStep = None
        self.STATUS_CODES = {
            -1: '',
            0: 'Успешный ход',
            1: 'Побита фигура противника',
            2: 'Пустая клетка',
            3: 'Чужая фигура',
            4: 'Ход назад',
            5: 'Невозможный ход',
            6: 'Клетка занята',
            7: 'Необходимо побить фигуру соперника',
            8: 'Необходимо добить все фигуры',
        }
        self.IS_REQUIRED_STEPS = isRequiredSteps
        self.IS_PRINT_PLACE = isPrintPlace
        self.isRequiredStepItem = None
        self.RESULT_PATH = '\\results.txt'

    def play(self):
        # Подсчёт фигур на доске
        for y in range(8):
            for x in range(8):
                item = self.place[y][x]
                itemColor = self.checkPlayerItem(item)
                if (itemColor == 'W'):
                    self.WHITE_COUNT += 1
                elif (itemColor == 'B'):
                    self.BLACK_COUNT += 1

        if (self.IS_PRINT_PLACE):
            self.printPlace()

        while True:
            # Проверка на ничью
            personFigurs = []
            for y in range(8):
                for x in range(8):
                    if (self.checkPlayerItem(self.place[y][x]) == self.currentPlayer):
                        personFigurs.append((x, y))

            for figureCoords in personFigurs:
                requiredStepsForItem = self.requiredStepsForItem(
                    playerColor=self.currentPlayer,
                    x=figureCoords[0],
                    y=figureCoords[1]
                )
                if (len(requiredStepsForItem) > 0):
                    break

                checkStepAble = self.checkStepAble(
                    playerColor=self.currentPlayer,
                    x=figureCoords[0],
                    y=figureCoords[1]
                )
                if (len(checkStepAble) > 0):
                    break
            else:
                self.setPat()
                break

            if (self.currentPlayer == 'W'):
                stepResult = self.PLAYER_WHITE.play('W')
            else:
                stepResult = self.PLAYER_BLACK.play('B')

            if (self.IS_PRINT_PLACE):
                self.printPlace()

            if (self.BLACK_COUNT == 0 or self.WHITE_COUNT == 0):
                if (self.BLACK_COUNT == 0):
                    self.saveResults(player=self.PLAYER_WHITE, playerColor='W')
                if (self.WHITE_COUNT == 0):
                    self.saveResults(player=self.PLAYER_BLACK, playerColor='B')

                break

            if not (stepResult['status'] in (0, 1)):
                print(f'Ошибка ({stepResult["status"]}): {self.STATUS_CODES[stepResult["status"]]}')

    def checkPlayerItem(self, item: int):
        if (item in (1, 3)):
            return 'W'
        if (item in (2, 4)):
            return 'B'
        return None

    def setStep(self, playerColor: str, x1: int, y1: int, x2: int, y2: int):
        result = {
            'status': 5,
        }

        item = self.place[y1][x1]

        # Чужая фигура
        if (self.checkPlayerItem(item) != playerColor):
            result['status'] = 3
            return result

        if (self.IS_REQUIRED_STEPS):
            if not (self.isRequiredStepItem is None):
                if (x1 != self.isRequiredStepItem[0] or y1 != self.isRequiredStepItem[1]):
                    result['status'] = 8
                    return result

            # Необходимо побить фигуру соперника
            requiredSteps = self.requiredStepsForPlayer(playerColor=playerColor)
            if (len(requiredSteps) > 0 and not ((x1, y1, x2, y2) in requiredSteps)):
                result['status'] = 7
                return result

        item_next = self.place[y2][x2]
        if (item_next == 0):
            # Обычная фигура
            if (self.place[y1][x1] in (1, 2)):
                if (abs(x1 - x2) == 1 and abs(y1 - y2) == 1):
                    # Успешный ход
                    self.place[y1][x1] = 0
                    self.place[y2][x2] = item
                    self.lastStep = (x2, y2)
                    result['status'] = 0
                elif (
                        abs(x1 - x2) == 2 and
                        abs(y1 - y2) == 2 and
                        not (self.checkPlayerItem(
                            self.place[y1 + int((y2 - y1) / 2)][x1 + int((x2 - x1) / 2)]) is None) and
                        (self.checkPlayerItem(
                            self.place[y1 + int((y2 - y1) / 2)][x1 + int((x2 - x1) / 2)]) != playerColor)
                ):
                    self.place[y1][x1] = 0
                    self.place[y1 + int((y2 - y1) / 2)][x1 + int((x2 - x1) / 2)] = 0
                    self.place[y2][x2] = item

                    if (playerColor == 'W'):
                        self.BLACK_COUNT -= 1
                    else:
                        self.WHITE_COUNT -= 1

                    self.lastStep = (x2, y2)

                    # Побита фигура противника
                    result['status'] = 1

            # Дамка
            elif (self.place[y1][x1] in (3, 4)):
                if (abs(x1 - x2) != abs(y1 - y2)):
                    result['status'] = 5
                    return result

                # Направление дамки
                xv = int((x2 - x1) / abs(x2 - x1))
                yv = int((y2 - y1) / abs(y2 - y1))

                # Проверка диагонали хода
                xi = x1 + xv
                yi = y1 + yv
                for i in range(abs(x1 - x2) - 1):
                    itemI = self.place[yi][xi]
                    if (itemI != 0):
                        # Если фигура соперника находится за одну клетку до места установки
                        if ((xi + xv == x2) and (yi + yv == y2) and self.checkPlayerItem(itemI) != self.currentPlayer):
                            # Побита фигура противника
                            result['status'] = 1
                        else:
                            result['status'] = 5
                            return result

                    xi += xv
                    yi += yv

                if (result['status'] == 1):
                    self.place[y2][x2] = self.place[y1][x1]
                    self.place[y1][x1] = 0
                    self.place[y2 - yv][x2 - xv] = 0

                    if (playerColor == 'W'):
                        self.BLACK_COUNT -= 1
                    else:
                        self.WHITE_COUNT -= 1

                    self.lastStep = (x2, y2)
                else:
                    self.place[y2][x2] = self.place[y1][x1]
                    self.place[y1][x1] = 0
                    self.lastStep = (x2, y2)
                    result['status'] = 0

        if (self.lastStep[1] == 0 and self.place[self.lastStep[1]][self.lastStep[0]] == 1):
            self.place[self.lastStep[1]][self.lastStep[0]] = 3

        if (self.lastStep[1] == 7 and self.place[self.lastStep[1]][self.lastStep[0]] == 2):
            self.place[self.lastStep[1]][self.lastStep[0]] = 4

        if (result['status'] in (0, 1)):
            requiredStepsForItem = []
            if (self.IS_REQUIRED_STEPS and result['status'] == 1):
                requiredStepsForItem = self.requiredStepsForItem(playerColor=self.currentPlayer, x=self.lastStep[0],
                                                                 y=self.lastStep[1])
            if (self.IS_REQUIRED_STEPS and len(requiredStepsForItem) > 0):
                self.isRequiredStepItem = self.lastStep
            else:
                self.isRequiredStepItem = None
                if (self.currentPlayer == 'W'):
                    self.currentPlayer = 'B'
                else:
                    self.currentPlayer = 'W'

        return result

    def requiredStepsForItem(self, playerColor: str, x: int, y: int):
        result = []

        item = self.place[y][x]

        # Left Forword
        if (item in (1, 2)):
            if (
                    x >= 2 and
                    y >= 2 and
                    self.place[y - 2][x - 2] == 0 and
                    not (self.checkPlayerItem(self.place[y - 1][x - 1]) is None) and
                    self.checkPlayerItem(self.place[y - 1][x - 1]) != playerColor
            ):
                result.append((x, y, x - 2, y - 2))

        elif (item in (3, 4)):
            xv = -1
            yv = -1
            xi = x + xv
            yi = y + yv
            while (xi > 0 and yi > 0):
                itemI = self.place[yi][xi]
                if (itemI != 0):
                    if (
                            self.checkPlayerItem(itemI) != playerColor and
                            xi >= 1 and yi >= 1 and
                            self.place[yi + yv][xi + xv] == 0
                    ):
                        result.append((x, y, xi + xv, yi + yv))
                        break
                    else:
                        break

                xi += xv
                yi += yv

        # Right Forword
        if (item in (1, 2)):
            if (
                    x <= 5 and
                    y >= 2 and
                    self.place[y - 2][x + 2] == 0 and
                    not (self.checkPlayerItem(self.place[y - 1][x + 1]) is None) and
                    self.checkPlayerItem(self.place[y - 1][x + 1]) != playerColor
            ):
                result.append((x, y, x + 2, y - 2))

        elif (item in (3, 4)):
            xv = 1
            yv = -1
            xi = x + xv
            yi = y + yv
            while (xi < 7 and yi > 0):
                itemI = self.place[yi][xi]
                if (itemI != 0):
                    if (
                            self.checkPlayerItem(itemI) != playerColor and
                            xi <= 6 and yi >= 1 and
                            self.place[yi + yv][xi + xv] == 0
                    ):
                        result.append((x, y, xi + xv, yi + yv))
                        break
                    else:
                        break

                xi += xv
                yi += yv

        # Left Back
        if (item in (1, 2)):
            if (
                    x >= 2 and
                    y <= 5 and
                    self.place[y + 2][x - 2] == 0 and
                    not (self.checkPlayerItem(self.place[y + 1][x - 1]) is None) and
                    self.checkPlayerItem(self.place[y + 1][x - 1]) != playerColor
            ):
                result.append((x, y, x - 2, y + 2))
        elif (item in (3, 4)):
            xv = -1
            yv = 1
            xi = x + xv
            yi = y + yv
            while (xi > 0 and yi < 7):
                itemI = self.place[yi][xi]
                if (itemI != 0):
                    if (
                            self.checkPlayerItem(itemI) != playerColor and
                            xi >= 1 and yi <= 6 and
                            self.place[yi + yv][xi + xv] == 0
                    ):
                        result.append((x, y, xi + xv, yi + yv))
                        break
                    else:
                        break

                xi += xv
                yi += yv

        # Right Back
        if (item in (1, 2)):
            if (
                    x <= 5 and
                    y <= 5 and
                    self.place[y + 2][x + 2] == 0 and
                    not (self.checkPlayerItem(self.place[y + 1][x + 1]) is None) and
                    self.checkPlayerItem(self.place[y + 1][x + 1]) != playerColor
            ):
                result.append((x, y, x + 2, y + 2))

        elif (item in (3, 4)):
            xv = 1
            yv = 1
            xi = x + xv
            yi = y + yv
            while (xi < 7 and yi < 7):
                itemI = self.place[yi][xi]
                if (itemI != 0):
                    if (
                            self.checkPlayerItem(itemI) != playerColor and
                            xi <= 6 and yi <= 6 and
                            self.place[yi + yv][xi + xv] == 0
                    ):
                        result.append((x, y, xi + xv, yi + yv))
                        break
                    else:
                        break

                xi += xv
                yi += yv

        return result

    def requiredStepsForPlayer(self, playerColor: str):
        result = []

        for y in range(8):
            for x in range(8):
                if (self.checkPlayerItem(self.place[y][x]) == playerColor):
                    result += self.requiredStepsForItem(playerColor=playerColor, x=x, y=y)

        return result

    def checkStepAble(self, playerColor: str, x: int, y: int):
        result = []

        item = self.place[y][x]

        if (item in (1, 2)):
            if (playerColor == 'W'):
                # Left Forword
                if (x > 0 and y > 0 and self.place[y - 1][x - 1] == 0):
                    result.append((x - 1, y - 1))
                # Right Forword
                if (x < (8 - 1) and y > 0 and self.place[y - 1][x + 1] == 0):
                    result.append((x + 1, y - 1))

            if (playerColor == 'B'):
                # Left Back
                if (x > 0 and y < (8 - 1) and self.place[y + 1][x - 1] == 0):
                    result.append((x - 1, y + 1))
                # Right Back
                if (x < (8 - 1) and y < (8 - 1) and self.place[y + 1][x + 1] == 0):
                    result.append((x + 1, y + 1))

        elif (item in (3, 4)):
            xv = 0
            yv = 0
            for i in range(4):
                # Left Forword
                if (i == 0):
                    xv = -1
                    yv = -1

                # Right Forword
                elif (i == 1):
                    xv = 1
                    yv = -1

                # Left Back
                elif (i == 2):
                    xv = -1
                    yv = 1

                # Right Back
                elif (i == 3):
                    xv = 1
                    yv = 1

                xi = x + xv
                yi = y + yv

                while (
                        xi >= 0 and xi <= 7 and
                        yi >= 0 and yi <= 7 and
                        self.place[yi][xi] == 0
                ):
                    result.append((xi, yi))
                    xi += xv
                    yi += yv

        return result

    def printPlace(self):
        '''
        ○
        ●
                          ╔═══╤═══╤═══╤═══╤═══╤═══╤═══╤═══╗   ╔═══════╤════════╗
                        8 ║   │ ● │   │ ● │   │ ● │   │ ● ║   ║ Белые │ Чёрные ║
                          ╟───┼───┼───┼───┼───┼───┼───┼───╢   ╟───────┼────────╢
                        7 ║ ● │   │ ● │   │ ● │   │ ● │   ║   ║    12 │      8 ║
                          ╟───┼───┼───┼───┼───┼───┼───┼───╢   ╚═══════╧════════╝
                        6 ║   │ ● │   │ ● │   │ ● │   │ ● ║
                          ╟───┼───┼───┼───┼───┼───┼───┼───╢
                        5 ║   │   │   │   │   │   │   │   ║
                          ╟───┼───┼───┼───┼───┼───┼───┼───╢
                        4 ║   │   │   │   │   │   │   │   ║
                          ╟───┼───┼───┼───┼───┼───┼───┼───╢
                        3 ║ ● │   │ ● │   │ ● │   │ ● │   ║
                          ╟───┼───┼───┼───┼───┼───┼───┼───╢
                        2 ║   │ ● │   │ ● │   │ ● │   │ ● ║
                          ╟───┼───┼───┼───┼───┼───┼───┼───╢
                        1 ║ ● │   │ ● │   │ ● │   │ ● │   ║
                          ╚═══╧═══╧═══╧═══╧═══╧═══╧═══╧═══╝
                            A   B   C   D   E   F   G   H
        '''

        '''
__          __ _    _  _____  _______  ______       __          __ _____  _   _ 
\ \        / /| |  | ||_   _||__   __||  ____|      \ \        / /|_   _|| \ | |
 \ \  /\  / / | |__| |  | |     | |   | |__          \ \  /\  / /   | |  |  \| |
  \ \/  \/ /  |  __  |  | |     | |   |  __|          \ \/  \/ /    | |  | . ` |
   \  /\  /   | |  | | _| |_    | |   | |____          \  /\  /    _| |_ | |\  |
    \/  \/    |_|  |_||_____|   |_|   |______|          \/  \/    |_____||_| \_|

____   _                  _____  _  __ __          __ _____  _   _ 
|  _ \ | |         /\     / ____|| |/ / \ \        / /|_   _|| \ | |
| |_) || |        /  \   | |     | ' /   \ \  /\  / /   | |  |  \| |
|  _ < | |       / /\ \  | |     |  <     \ \/  \/ /    | |  | . ` |
| |_) || |____  / ____ \ | |____ | . \     \  /\  /    _| |_ | |\  |
|____/ |______|/_/    \_\ \_____||_|\_\     \/  \/    |_____||_| \_|
        '''

        FIGURES = {
            0: ' ',
            1: '●',
            2: '○',
            3: f'{bcolors.UNDERLINE}{bcolors.POWER}●{bcolors.ENDC}',
            4: f'{bcolors.UNDERLINE}{bcolors.POWER}○{bcolors.ENDC}',
        }

        placeCanvas = ''

        if (self.BLACK_COUNT <= 0):
            placeCanvas = '__          __ _    _  _____  _______  ______       __          __ _____  _   _ \n' \
                          '\ \        / /| |  | ||_   _||__   __||  ____|      \ \        / /|_   _|| \ | |\n' \
                          ' \ \  /\  / / | |__| |  | |     | |   | |__          \ \  /\  / /   | |  |  \| |\n' \
                          '  \ \/  \/ /  |  __  |  | |     | |   |  __|          \ \/  \/ /    | |  | . ` |\n' \
                          '   \  /\  /   | |  | | _| |_    | |   | |____          \  /\  /    _| |_ | |\  |\n' \
                          '    \/  \/    |_|  |_||_____|   |_|   |______|          \/  \/    |_____||_| \_|\n'

        elif (self.WHITE_COUNT <= 0):
            placeCanvas = ' ____   _                  _____  _  __         _          __ _____  _   _ \n' \
                          '|  _ \ | |         /\     / ____|| |/ /        \ \        / /|_   _|| \ | |\n' \
                          '| |_) || |        /  \   | |     | \' /          \ \  /\  / /   | |  |  \| |\n' \
                          '|  _ < | |       / /\ \  | |     |  <            \ \/  \/ /    | |  | . ` |\n' \
                          '| |_) || |____  / ____ \ | |____ | . \            \  /\  /    _| |_ | |\  |\n' \
                          '|____/ |______|/_/    \_\ \_____||_|\_\            \/  \/    |_____||_| \_|'

        else:
            for y in range(8):
                for x in range(8):
                    if (placeCanvas == ''):
                        placeCanvas += '   ╔═══╤═══╤═══╤═══╤═══╤═══╤═══╤═══╗   ╔═══════╤════════╗\n'
                    if (x == 0):
                        placeCanvas += f' {8 - y} ║'

                    if (self.lastStep and self.lastStep[0] == x and self.lastStep[1] == y):
                        placeCanvas += f' {bcolors.LASTSTEP}{FIGURES[self.place[y][x]]}{bcolors.ENDC} '
                    else:
                        placeCanvas += f' {FIGURES[self.place[y][x]]} '

                    if (x == (8 - 1)):
                        placeCanvas += '║'
                        if (y == 0):
                            placeCanvas += '   ║ Белые │ Чёрные ║'
                        if (y == 1):
                            placeCanvas += f'   ║    {self.WHITE_COUNT if (self.WHITE_COUNT >= 10) else f" {self.WHITE_COUNT}"} │     {self.BLACK_COUNT if (self.BLACK_COUNT >= 10) else f" {self.BLACK_COUNT}"} ║'
                        placeCanvas += '\n'
                    else:
                        placeCanvas += '│'

                if (y == (8 - 1)):
                    placeCanvas += '   ╚═══╧═══╧═══╧═══╧═══╧═══╧═══╧═══╝\n'
                    placeCanvas += '     A   B   C   D   E   F   G   H  \n'

                else:
                    placeCanvas += '   ╟───┼───┼───┼───┼───┼───┼───┼───╢'
                    if (y == 0):
                        placeCanvas += '   ╟───────┼────────╢'
                    if (y == 1):
                        placeCanvas += '   ╚═══════╧════════╝'
                    placeCanvas += '\n'

        os.system('cls' if os.name == 'nt' else 'clear')
        print(placeCanvas)

    def setPat(self):
        '''
         ______                       _
        |  ____|                     | |
        | |__     __ _  _   _   __ _ | | ___
        |  __|   / _` || | | | / _` || |/ __|
        | |____ | (_| || |_| || (_| || |\__ \
        |______| \__, | \__,_| \__,_||_||___/
                    | |
                    |_|

        '''

        if (self.IS_PRINT_PLACE):
            printCanvas = ' ______                       _      \n' \
                          '|  ____|                     | |\n' \
                          '| |__     __ _  _   _   __ _ | | ___\n' \
                          '|  __|   / _` || | | | / _` || |/ __|\n' \
                          '| |____ | (_| || |_| || (_| || |\__ \\\n' \
                          '|______| \__, | \__,_| \__,_||_||___/\n' \
                          '            | |\n' \
                          '            |_|'
            print(printCanvas)

        self.saveResults(pat=True)

    def saveResults(self, player: Player = None, playerColor: str = None, pat: bool = False):
        result = ''
        if (not(player is None) and not(playerColor is None)):
            result = f'Победа {"белых" if playerColor == "W" else "чёрных"}: {player.NAME}'
        if (pat):
            result = 'Ничья'

        path = f'{os.path.dirname(os.path.abspath(__file__))}\{self.RESULT_PATH}'
        with open(path, 'r+', encoding='UTF-8') as f:
            f.seek(0, 2)  # перемещение курсора в конец файла
            f.write(f'{result}\n')
