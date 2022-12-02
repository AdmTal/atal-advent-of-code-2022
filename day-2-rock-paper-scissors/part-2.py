import enum


class Choice(enum.Enum):
    ROCK = enum.auto()
    PAPER = enum.auto()
    SCISSORS = enum.auto()


class Result(enum.Enum):
    WIN = enum.auto()
    LOSE = enum.auto()
    DRAW = enum.auto()


STRATEGY_DECODER_OPPONENT_MOVE = {
    'A': Choice.ROCK,
    'B': Choice.PAPER,
    'C': Choice.SCISSORS,
}

STRATEGY_DECODER_REQUIRED_RESULT = {
    'X': Result.LOSE,
    'Y': Result.DRAW,
    'Z': Result.WIN,
}

GAME_LOGIC = {
    Choice.ROCK: {
        Choice.ROCK: Result.DRAW,
        Choice.PAPER: Result.LOSE,
        Choice.SCISSORS: Result.WIN,
    },
    Choice.PAPER: {
        Choice.ROCK: Result.WIN,
        Choice.PAPER: Result.DRAW,
        Choice.SCISSORS: Result.LOSE,
    },
    Choice.SCISSORS: {
        Choice.ROCK: Result.LOSE,
        Choice.PAPER: Result.WIN,
        Choice.SCISSORS: Result.DRAW,
    },
}

CHOICE_BY_RESULT = {
    Result.WIN: {
        Choice.ROCK: Choice.PAPER,
        Choice.PAPER: Choice.SCISSORS,
        Choice.SCISSORS: Choice.ROCK,
    },
    Result.DRAW: {
        Choice.ROCK: Choice.ROCK,
        Choice.PAPER: Choice.PAPER,
        Choice.SCISSORS: Choice.SCISSORS,
    },
    Result.LOSE: {
        Choice.ROCK: Choice.SCISSORS,
        Choice.PAPER: Choice.ROCK,
        Choice.SCISSORS: Choice.PAPER,
    },
}

POINTS_BY_CHOICE = {
    Choice.ROCK: 1,
    Choice.PAPER: 2,
    Choice.SCISSORS: 3,
}

POINTS_BY_RESULT = {
    Result.LOSE: 0,
    Result.DRAW: 3,
    Result.WIN: 6,
}

strategy_guide_rounds = [
    (
        STRATEGY_DECODER_OPPONENT_MOVE[x],
        STRATEGY_DECODER_REQUIRED_RESULT[y]
    )
    for x, y in [i.split(' ') for i in open('./input.txt').read().split('\n')]
]

your_score = 0

for opponent_choice, required_result in strategy_guide_rounds:
    your_choice = CHOICE_BY_RESULT[required_result][opponent_choice]
    round_result = GAME_LOGIC[your_choice][opponent_choice]
    your_score += POINTS_BY_CHOICE[your_choice] + POINTS_BY_RESULT[round_result]

print(your_score)
