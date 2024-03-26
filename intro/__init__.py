import time

from otree import settings
from otree.api import *

from .image_utils import encode_image

doc = """
Real-effort tasks. The different tasks are available in task_matrix.py, task_transcription.py, etc.
You can delete the ones you don't need. 
"""


def get_task_module(player):
    """
    This function is only needed for demo mode, to demonstrate all the different versions.
    You can simplify it if you want.
    """
    from . import task_decoding
    from . import task_decoding_2

    session = player.session
    task = session.config.get("task")

    # iterationが奇数ならtask_decoding_1、偶数ならtask_decoding_2を返す
    if task == "decoding":
        if player.iteration % 2 == 1:
            return task_decoding
        else:
            return task_decoding_2


class C(BaseConstants):
    NAME_IN_URL = "Practice"
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1

class Subsession(BaseSubsession):
    pass

def creating_session(subsession: Subsession):
    import csv

    f = open(__name__ + '/treatments.csv', encoding='utf-8-sig')

    rows = list(csv.DictReader(f))
    players = subsession.get_players()
    for i in range(len(players)):
        row = rows[i]
        player = players[i]
        # CSV contains all data in string form, so we need to convert
        # to the correct data type, e.g. '1' -> 1 -> True.
        player.adjustment = bool(int(row['adjustment']))
        player.informed = bool(int(row['informed']))
        player.exp_order = bool(int(row['exp_order']))
    session = subsession.session
    defaults = dict(
        retry_delay=1.0, puzzle_delay=1.0, attempts_per_puzzle=1, max_iterations=None
    )
    session.params = {}
    for param in defaults:
        session.params[param] = session.config.get(param, defaults[param])


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    prolific_id = models.StringField()
    label = 'Your Prolific ID'
    adjustment = models.BooleanField()
    informed = models.BooleanField()
    exp_order = models.BooleanField()
    iteration = models.IntegerField(initial=0)
    num_trials = models.IntegerField(initial=0)
    num_correct = models.IntegerField(initial=0)
    num_failed = models.IntegerField(initial=0)
    num_score = models.IntegerField(initial=0)
    question1 = models.BooleanField(
        label="Your task is decoding as many numbers as possible into alphabets within a time limit.",  # True
        choices=[[1, "True"], [0, "False"]],
    )
    question2 = models.BooleanField(
        label="You receive a bonus when you achieve your assigned target.",  # True
        choices=[[1, "True"], [0, "False"]],
    )
    question3 = models.BooleanField(
        label="Your reward do not increase any further if you exceed your assigned target.",  # False
        choices=[[1, "True"], [0, "False"]],
    )
    question4 = models.BooleanField(
        label="Mid-term feedback is given in the middle of each period.",
        choices=[[1, "True"], [0, "False"]],
    )
    question5 = models.IntegerField(
        label='An assigned target may be adjusted ...',
        choices=[[1, 'When the gap between the target and performance is large'],
                 [2, 'When the environment is very difficult to achieve the target'],
                 [3, 'Randomly']],
        widget=widgets.RadioSelect,
        blank=True,
        null=True,
    )


# puzzle-specific stuff


class Puzzle(ExtraModel):
    """A model to keep record of all generated puzzles"""

    player = models.Link(Player)
    iteration = models.IntegerField(initial=0)
    attempts = models.IntegerField(initial=0)
    timestamp = models.FloatField(initial=0)
    # can be either simple text, or a json-encoded definition of the puzzle, etc.
    text = models.LongStringField()
    # solution may be the same as text, if it's simply a transcription task
    solution = models.LongStringField()
    response = models.LongStringField()
    response_timestamp = models.FloatField()
    is_correct = models.BooleanField()

### functions ###

def generate_puzzle(player: Player) -> Puzzle:
    """Create new puzzle for a player"""
    task_module = get_task_module(player)
    fields = task_module.generate_puzzle_fields()
    player.iteration += 1
    return Puzzle.create(
        player=player, iteration=player.iteration, timestamp=time.time(), **fields
    )


def get_current_puzzle(player):
    puzzles = Puzzle.filter(player=player, iteration=player.iteration)
    if puzzles:
        [puzzle] = puzzles
        return puzzle


def encode_puzzle(puzzle: Puzzle):
    """Create data describing puzzle to send to client"""
    task_module = get_task_module(puzzle.player)  # noqa
    # generate image for the puzzle
    image = task_module.render_image(puzzle)
    data = encode_image(image)
    return dict(image=data)


def get_progress(player: Player):
    """Return current player progress"""
    return dict(
        num_trials=player.num_trials,
        num_correct=player.num_correct,
        num_incorrect=player.num_failed,
        iteration=player.iteration,
    )


def play_game(player: Player, message: dict):
    """Main game workflow
    Implemented as reactive scheme: receive message from vrowser, react, respond.

    Generic game workflow, from server point of view:
    - receive: {'type': 'load'} -- empty message means page loaded
    - check if it's game start or page refresh midgame
    - respond: {'type': 'status', 'progress': ...}
    - respond: {'type': 'status', 'progress': ..., 'puzzle': data} -- in case of midgame page reload

    - receive: {'type': 'next'} -- request for a next/first puzzle
    - generate new puzzle
    - respond: {'type': 'puzzle', 'puzzle': data}

    - receive: {'type': 'answer', 'answer': ...} -- user answered the puzzle
    - check if the answer is correct
    - respond: {'type': 'feedback', 'is_correct': true|false, 'retries_left': ...} -- feedback to the answer

    If allowed by config `attempts_pre_puzzle`, client can send more 'answer' messages
    When done solving, client should explicitely request next puzzle by sending 'next' message

    Field 'progress' is added to all server responses to indicate it on page.

    To indicate max_iteration exhausted in response to 'next' server returns 'status' message with iterations_left=0
    """
    session = player.session
    my_id = player.id_in_group
    params = session.params
    task_module = get_task_module(player)

    now = time.time()
    # the current puzzle or none
    current = get_current_puzzle(player)

    message_type = message['type']

    # page loaded
    if message_type == 'load':
        p = get_progress(player)
        if current:
            return {
                my_id: dict(type='status', progress=p, puzzle=encode_puzzle(current))
            }
        else:
            return {my_id: dict(type='status', progress=p)}

    if message_type == "cheat" and settings.DEBUG:
        return {my_id: dict(type='solution', solution=current.solution)}

    # client requested new puzzle
    if message_type == "next":
        if current is not None:
            if current.response is None:
                raise RuntimeError("trying to skip over unsolved puzzle")
            if now < current.timestamp + params["puzzle_delay"]:
                raise RuntimeError("retrying too fast")
            if current.iteration == params['max_iterations']:
                return {
                    my_id: dict(
                        type='status', progress=get_progress(player), iterations_left=0
                    )
                }
        # generate new puzzle
        z = generate_puzzle(player)
        p = get_progress(player)
        return {my_id: dict(type='puzzle', puzzle=encode_puzzle(z), progress=p)}

    # client gives an answer to current puzzle
    if message_type == "answer":
        if current is None:
            raise RuntimeError("trying to answer no puzzle")

        if current.response is not None:  # it's a retry
            if current.attempts >= params["attempts_per_puzzle"]:
                raise RuntimeError("no more attempts allowed")
            if now < current.response_timestamp + params["retry_delay"]:
                raise RuntimeError("retrying too fast")

            # undo last updation of player progress
            player.num_trials -= 1
            if current.is_correct:
                player.num_correct -= 1
            else:
                player.num_failed -= 1

        # check answer
        answer = message["answer"]

        if answer == "" or answer is None:
            raise ValueError("bogus answer")

        current.response = answer
        current.is_correct = task_module.is_correct(answer, current)
        current.response_timestamp = now
        current.attempts += 1

        # update player progress
        if current.is_correct:
            player.num_correct += 1
        else:
            player.num_failed += 1
        player.num_trials += 1

        if player.iteration % 2 == 1:
            if current.is_correct:
                    player.num_score += 1
        else:
            if current.is_correct:
                     player.num_score += 2

        retries_left = params["attempts_per_puzzle"] - current.attempts
        p = get_progress(player)
        return {
            my_id: dict(
                type='feedback',
                is_correct=current.is_correct,
                retries_left=retries_left,
                progress=p,
            )
        }

    raise RuntimeError("unrecognized message from client")

class Consent(Page):
    form_model = "player"
    form_fields = ["prolific_id"]

class Overview(Page):
    pass

class Ready(Page):
    timeout_seconds = 5

class Practice(Page):
    timeout_seconds = 60

    live_method = play_game

    @staticmethod
    def js_vars(player: Player):
        return dict(params=player.session.params)

    @staticmethod
    def vars_for_template(player: Player):
        task_module = get_task_module(player)
        return dict(DEBUG=settings.DEBUG,
                    input_type=task_module.INPUT_TYPE,
                    placeholder=task_module.INPUT_HINT)

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if not timeout_happened and not player.session.params['max_iterations']:
            raise RuntimeError("malicious page submission")

class P_Results(Page):
    pass

class Instruction_2(Page):
   pass

class Quiz(Page):
    form_model = "player"
    form_fields = ['question1', 'question2', 'question3', 'question4', 'question5']

    @staticmethod
    def error_message(player, values):
        if player.informed == 0:
            solutions0 = dict(
                question1=True,
                question2=True,
                question3=False,
                question4=True,
                question5=None
            )
            error_messages = dict()
            for field_name in solutions0:
                if values[field_name] != solutions0[field_name]:
                    error_messages[field_name] = 'Your answer is incorrect'

            return error_messages

        if player.informed == 1:
            solutions1 = dict(
                question1=True,
                question2=True,
                question3=False,
                question4=True,
                question5=2
            )
            error_messages = dict()
            for field_name in solutions1:
                if values[field_name] != solutions1[field_name]:
                    error_messages[field_name] = 'Your answer is incorrect'

            return error_messages


page_sequence = [Consent, Overview, Ready, Practice, P_Results, Instruction_2, Quiz]

