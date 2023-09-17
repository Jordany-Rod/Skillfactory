x_and_o = [['-','-','-'],['-','-','-'],['-','-','-']]

# Интерфейс игры
def interface(x_and_o):
    for i in range(3):
        if i == 0:
            print(' ', 0, 1, 2)
        else:
            print('\n', end='')
        for j in range(3):
            if j == 0:
                print(i, end=' ')
            print(x_and_o[j][i], end=' ')
    return ""

# Проверка условия победы
def check_win(x_and_o):
    if any([x_and_o[0] == ['x','x','x'],x_and_o[1] == ['x','x','x'],x_and_o[2] == ['x','x','x']]):
        return 'Крестики WIN!'
    if any([x_and_o[0] == ['o','o','o'],x_and_o[1] == ['o','o','o'],x_and_o[2] == ['o','o','o']]):
        return 'Нолики WIN!'
    if x_and_o[0][0] == x_and_o[1][1] == x_and_o[2][2] == 'x':
        return 'Крестики WIN!'
    if x_and_o[0][0] == x_and_o[1][1] == x_and_o[2][2] == 'o':
        return 'Нолики WIN!'
    if x_and_o[0][2] == x_and_o[1][1] == x_and_o[2][0] == 'x':
        return 'Крестики WIN!'
    if x_and_o[0][2] == x_and_o[1][1] == x_and_o[2][0] == 'o':
        return 'Нолики WIN!'

    win_x = 0
    win_o = 0

    for i in range(3):
        if win_x == 3:
            return 'Крестики WIN!'
        win_x = 0
        for j in range(3):
            if x_and_o[j][i] == 'x':
                win_x += 1
    for i in range(3):
        if win_o == 3:
            return 'Нолики WIN!'
        win_o = 0
        for j in range(3):
            if x_and_o[j][i] == 'o':
                win_o += 1

# Коррекность ввода координат для X
def coord_X(x):
    while True:
        x = input('Введите координату X от 0 до 2:')
        if not x.isdigit():
            print('Разрешено вводить только цифры!')
            continue
        x = int(x)
        if x < 0 or x > 2:
            print('Разрешено вводить цифры в диапазоне от 0 до 2 включительно!')
            continue
        return x

# Коррекность ввода координат для Y
def coord_Y(y):
    while True:
        y = input('Введите координату Y от 0 до 2:')
        if not y.isdigit():
            print('Разрешено вводить только цифры!')
            continue
        y = int(y)
        if y < 0 or y > 2:
            print('Разрешено вводить цифры в диапазоне от 0 до 2 включительно!')
            continue
        return y

# Проверка повторного ввода координат для крестиков
def repeat_сross(x_and_o):
    x = 0
    y = 0
    while True:
        x = coord_X(x)
        y = coord_Y(y)
        if x_and_o[x][y] == '-':
            x_and_o[x][y] = 'x'
            break
        else:
            print('Нельзя вводить координаты уже занятого поля!')
    return x_and_o[x][y]

# Проверка повторного ввода координат для ноликов
def repeat_zero(x_and_o):
    x = 0
    y = 0
    while True:
        x = coord_X(x)
        y = coord_Y(y)
        if x_and_o[x][y] == '-':
            x_and_o[x][y] = 'o'
            break
        else:
            print('Нельзя вводить координаты уже занятого поля!')
    return x_and_o[x][y]

# Игра крестики нолики
def game(x_and_o):
    for i in range(9):
        if i % 2 == 0:
            interface(x_and_o)
            print('\n',"Ходят крестики")
            repeat_сross(x_and_o)
        else:
            interface(x_and_o)
            print('\n', "Ходят нолики")
            repeat_zero(x_and_o)
        vera = check_win(x_and_o)
        if vera == 'Крестики WIN!' or vera == 'Нолики WIN!':
            print(interface(x_and_o))
            print(check_win(x_and_o))
            break
        draw = i
    if draw == 8:
        print(interface(x_and_o))
        print('---------')
        print('| НИЧЬЯ |')
        print('---------')

print('ДОБРО ПОЖАЛОВАТЬ В ИГРУ КРЕСТИКИ-НОЛИКИ')
game(x_and_o)
print('GAME OVER')


