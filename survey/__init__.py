from otree.api import *


class C(BaseConstants):
    NAME_IN_URL = 'survey'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):


    justice1 = models.IntegerField(
        label="Process used to determine incentive payouts applied consistently.",
        choices=[-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5],
        widget=widgets.RadioSelect,
    )
    justice2 = models.IntegerField(
        label="Process used to determine incentive payout has been fair.",
        choices=[-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5],
        widget = widgets.RadioSelect,
    )
    justice3 = models.IntegerField(
        label="Process used to determine incentive payout has been bias free.",
        choices=[-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5],
        widget = widgets.RadioSelect,
    )
    justice4 = models.IntegerField(
        label="Amount of incentive payout received reflects effort I put into the task.",
        choices=[-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5],
        widget = widgets.RadioSelect,
    )
    justice5 = models.IntegerField(
        label="Incentive payout is appropriate for effort I have put into the task.",
        choices=[-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5],
        widget = widgets.RadioSelect,
    )
    justice6 = models.IntegerField(
        label="The amount of incentive payout reflects my contribution to the task.",
        choices=[-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5],
        widget = widgets.RadioSelect,
    )
    justice7 = models.IntegerField(
        label="The amount of payout is justified given my performance at the task.",
        choices=[-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5],
        widget = widgets.RadioSelect,
    )
    age = models.IntegerField(
        label='What is your age (in years)?'
    )
    gender = models.IntegerField(
        label='With which gender do you identify most?',
        choices=[[1, 'Male'], [2, 'Female'], [3, 'Non-Binary'], [4, 'Prefer not to answer']],
        widget=widgets.RadioSelect
    )
    education = models.IntegerField(
        label='What is your highest level of education completed?',
        choices=[[1, 'No high school degree or equivalent'],  [2, 'High school degree or equivalent'], [3, 'Some college'],  [4, 'Undergraduate degree'], [5, 'Graduate degree'],  [6, 'Prefer not to answer'], ],
        widget=widgets.RadioSelect
    )
    work_experience = models.IntegerField(
        label='How many years of full-time work experience do you have?'
    )


# FUNCTIONS


# PAGES
class Post_Survey1(Page):
    form_model = 'player'
    form_fields = ['justice1', 'justice2', 'justice3', 'justice4', 'justice5', 'justice6', 'justice7']

class Post_Survey2(Page):
    form_model = 'player'
    form_fields = ['age', 'gender', 'education', 'work_experience']

class End(Page):
    pass

page_sequence = [Post_Survey1, Post_Survey2, End]
