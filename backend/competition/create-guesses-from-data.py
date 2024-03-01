#! /usr/bin/env python3
import html
from collections import namedtuple, defaultdict
from pathlib import Path
import json
import hashlib

HEROES = [
    "Vasco da Gama",
    "Pachacuti",
    "Sumanguru",
    "Jean Bureau",
    "Jadwiga",
    "Otto the Great",
    "Gregory VII",
    "Gajah Mada",
    "King Stephen",
    "Selim the Grim",
    "Khosrau",
    "Emperor Sigismund",
    "Alfred the Alpaca",
    "Jan Zizka",
    "Alexios Komnenos",
    "Robert Guiscard",
]

PLAYERS = [
    "ACCM",
    "DauT",
    "Hera",
    "JorDan_AoE",
    "Liereyy",
    "Mr_Yo",
    "TheViper",
    "TaToH",
    "Vinchester",
    "Barles",
    "MbL",
    "Sitaux",
    "Sebastian2002",
    "Hearttt",
    "Mihai06",
    "Ganji",
]

CORRECT = {
    "Vasco da Gama": "ACCM",
    "Pachacuti": "DauT",
    "Sumanguru": "Hera",
    "Jean Bureau": "JorDan_AoE",
    "Jadwiga": "Liereyy",
    "Otto the Great": "Mr_Yo",
    "Gregory VII": "TheViper",
    "Gajah Mada": "TaToH",
    "King Stephen": "Vinchester",
    "Selim the Grim": "Barles",
    "Khosrau": "MbL",
    "Emperor Sigismund": "Sitaux",
    "Alfred the Alpaca": "Sebastian2002",
    "Jan Zizka": "Hearttt",
    "Alexios Komnenos": "Mihai06",
    "Robert Guiscard": "Ganji",
}

CORRECT_INV = {player: hero for hero, player in CORRECT.items()}

AG_TABLE_HEAD = '''<table class="table table-sm">
<thead>
<tr>
<th>Correct Guesses</th>
<th>Name</th>
<th>Guesses</th>
</tr>
</thead>
<tbody>
'''

TABLE_FOOT = '''</tbody>
</table>
'''

CGP_TABLE_HEAD = '''<table class="table table-sm">
<thead>
<tr>
<th>Player</th>
<th>Hero</th>
<th colspan="2">Correct Guesses</th>
</tr>
</thead>
<tbody>
'''


def assert_values(actual: list[str], expected: list[str]):
    assert set(actual) == set(expected)


class Guess:
    def __init__(self, jsonfile: Path):
        content = json.loads(jsonfile.read_text())
        self.username = content['username']
        assert_values(content['guess'].keys(), HEROES)
        assert_values(content['guess'].values(), PLAYERS)
        self.guess = content['guess']
        self.guess_inv = {player: hero for hero, player in content['guess'].items()}

    def correct_guesses(self) -> int:
        correct_guesses = 0
        for hero, player in CORRECT.items():
            if self.guess[hero] == player:
                correct_guesses += 1
        return correct_guesses

    def correctly_guessed_player_for_hero(self, hero: str) -> bool:
        return self.guess[hero] == CORRECT[hero]

    def correctly_guessed_hero_for_player(self, player: str) -> bool:
        return self.guess_inv[player] == CORRECT_INV[player]


PlayerGuesses = namedtuple('PlayerGuesses', ['player', 'correct_guesses'])


def guess_row(guess: Guess) -> str:
    row = f'''<tr>
<td>{guess.correct_guesses()} / 16</td>
<td>{html.escape(guess.username)}</td>
<td>
<details>
<summary>Detailed Guesses</summary>
<dl>
'''
    for hero in HEROES:
        emoji = '✅' if guess.correctly_guessed_player_for_hero(hero) else '❌'
        remark = '' if guess.correctly_guessed_player_for_hero(hero) else f' <small><i>correct: {CORRECT[hero]}</i></small>'
        row += f'''<dt>{hero}</dt>
<dd>{emoji} {guess.guess[hero]}{remark}</dd>
'''
    row += '''</dl>
</details>
</td>
</tr>
'''
    return row


def player_guess_details(player_guesses: PlayerGuesses, guess_counts: dict) -> str:
    details = f'<details><summary>{player_guesses.player}</summary><ul class="list-unstyled">'
    stats = []
    for hero in HEROES:
        key = (hero, player_guesses.player)
        count = guess_counts[key]
        stats.append((count, hero))
    for count, hero in sorted(stats, reverse=True):
        emoji = '✅' if hero == CORRECT_INV[player_guesses.player] else '❌'
        details += f'<li>{emoji} {hero}: {count}</li>'
    details += '</ul></details>'
    return details


def hero_guess_details(player_guesses: PlayerGuesses, guess_counts: dict) -> str:
    hero = CORRECT_INV[player_guesses.player]
    details = f'<details><summary>{hero}</summary><ul class="list-unstyled">'
    stats = []
    for player in PLAYERS:
        key = (hero, player)
        count = guess_counts[key]
        stats.append((count, player))
    for count, player in sorted(stats, reverse=True):
        emoji = '✅' if player == CORRECT[hero] else '❌'
        details += f'<li>{emoji} {player}: {count}</li>'
    details += '</ul></details>'
    return details


def player_row(player_guesses: PlayerGuesses, count: int, guess_counts: dict) -> str:
    percentage = player_guesses.correct_guesses / count
    player_details = player_guess_details(player_guesses, guess_counts)
    hero_details = hero_guess_details(player_guesses, guess_counts)
    return f'''        <tr>
            <td>{player_details}</td>
            <td>{hero_details}</td>
            <td>{percentage:.2f} %</td>
            <td>{player_guesses.correct_guesses} / {count}</td>
        </tr>
'''


def main():
    directory = Path(__file__).parent / 'data'
    guesses = []
    for jsonfile in sorted(directory.glob('*.json'), key=lambda x: x.name[-15:]):
        try:
            guesses.append(Guess(jsonfile))
        except Exception as e:
            print(f'skipping {jsonfile} {e}')
            raise e
    print(f'Number of valid guesses: {len(guesses)}')
    guesses = sorted(guesses, key=lambda g: g.correct_guesses(), reverse=True)
    count = len(guesses)
    guessed_players = []
    for player in PLAYERS:
        correct_guesses = sum(guess.correctly_guessed_hero_for_player(player) for guess in guesses)
        guessed_players.append(PlayerGuesses(player, correct_guesses))
    guessed_players = sorted(guessed_players, key=lambda gp: gp.correct_guesses, reverse=True)

    guess_counts = defaultdict(lambda: 0)
    for guess in guesses:
        for hero in HEROES:
            guess_counts[(hero, guess.guess[hero])] += 1

    correctly_guessed_players = CGP_TABLE_HEAD + ''.join([player_row(gp, count, guess_counts) for gp in guessed_players]) + TABLE_FOOT
    all_guesses_table = AG_TABLE_HEAD + ''.join([guess_row(guess) for guess in guesses]) + TABLE_FOOT

    template_file = Path(__file__).with_name('template.html')
    target_file = Path(__file__).with_name('index.html')
    content = template_file.read_text()
    content = content.replace('{%correctly_guessed_players%}', correctly_guessed_players)
    content = content.replace('{%all_guesses_table%}', all_guesses_table)
    target_file.write_text(content)


if __name__ == '__main__':
    main()
