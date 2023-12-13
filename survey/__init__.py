from otree.api import *


class C(BaseConstants):
    NAME_IN_URL = 'survey'
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
    adjustment = models.BooleanField()
    informed = models.BooleanField()
    exp_order = models.BooleanField()
    justice1 = models.IntegerField(
        label='Process used to determine incentive payouts applied consistently',
        choices=[1, 2, 3, 4, 5, 6, 7],
        widget=widgets.RadioSelect
    )
    justice2 = models.IntegerField(
        label='Process used to determine incentive payout has been fair.',
        choices=[1, 2, 3, 4, 5, 6, 7],
        widget=widgets.RadioSelect
    )
    justice3 = models.IntegerField(
        label='Process used to determine incentive payout has been bias free.',
        choices=[1, 2, 3, 4, 5, 6, 7],
        widget=widgets.RadioSelect
    )
    justice4 = models.IntegerField(
        label='Amount of incentive payout received reflects effort I put into the task.',
        choices=[1, 2, 3, 4, 5, 6, 7],
        widget=widgets.RadioSelect
    )
    justice5 = models.IntegerField(
        label='Incentive payout is appropriate for effort I have put into the task.',
        choices=[1, 2, 3, 4, 5, 6, 7],
        widget=widgets.RadioSelect
    )
    justice6 = models.IntegerField(
        label='Most people will respond in kind when they are trusted by others.',
        choices=[1, 2, 3, 4, 5, 6, 7],
        widget=widgets.RadioSelect
    )
    justice7 = models.IntegerField(
        label='The amount of payout is justified given my performance at the task.',
        choices=[1, 2, 3, 4, 5, 6, 7],
        widget=widgets.RadioSelect
    )
    age = models.IntegerField(
        label='What is your age? (If you do not want to answer this question, you can leave it blank.)',
        min=15, max=80,
        blank = True,
        null = True
    )
    gender = models.IntegerField(
        label='With which gender do you identify most?',
        choices=[[1, 'Male'], [2, 'Female'], [3, 'Non-Binary'], [4, 'Prefer not to answer']],
        widget=widgets.RadioSelect
    )
    language = models.IntegerField(
        label='What is your native language?',
        choices=[[1, 'English'], [2, 'Non-English']],
        widget=widgets.RadioSelect
    )


# FUNCTIONS


# PAGES
class Post_Survey1(Page):
    form_model = "player"
    form_fields = ["justice1", "justice2", "justice3", "justice4", "justice5", "justice6", "justice7"]  ## とりあえず入力フォームの順番は固定のままにしておく．

class Post_Survey2(Page):
    form_model = "player"
    form_fields = ["age", "gender",  "language"]

class End(Page):
    pass

page_sequence = [Post_Survey1, Post_Survey2, End]
