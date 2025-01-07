from be import Cell, Game, GameState


def cell_to_str(c: Cell, m: int):
    ret = str(m) if c.uncovered else "-"
    ret += c.state.name[0]
    ret += "M" if c.is_mine else " "
    return ret


def render(game: Game):
    print()
    for i in range(game.rows):
        for j in range(game.cols):
            cell = game.get_cell(i, j)
            print(cell_to_str(cell, game.get_adjacent_mine_num(i, j)), end=" ")
        print()

    print(game.state.name)


def get_new_game() -> Game:
    s = input("请输入行数、列数、地雷数（以空格分隔）：")
    rows, cols, mines = s.split()
    rows, cols, mines = int(rows), int(cols), int(mines)
    return Game(rows, cols, mines)


def main():
    game = get_new_game()

    while True:
        render(game)
        if game.ended:
            game = get_new_game()

        s = input().split()
        cmd = s[0]
        if cmd == "new":
            game = get_new_game()
            continue

        x, y = int(s[1]), int(s[2])
        if cmd == "l":
            game.lclick(x, y)
        elif cmd == "r":
            game.rclick(x, y)
        elif cmd == "lr":
            game.lrclick(x, y)


if __name__ == "__main__":
    main()
