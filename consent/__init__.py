from otree.api import *


doc = """
Your app description
"""


### MODELS ###
class C(BaseConstants):
    NAME_IN_URL = 'consent'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    CHOICE_PHASES_LINK = "https://www.dropbox.com/s/dknq2k8cec1y1lz/Timeline%20Choice%20condition%20-%20Phases.png?raw=1"
    CHOICE_CAPPED_PHASES_LINK = "https://www.dropbox.com/scl/fi/ktv2y2gc45wdhvar5tdhq/Timeline-Choice-Capped-condition-Phases.png?rlkey=72v17xh80l0w47wj3sj3r1zee&dl=1"
    NO_CHOICE_EMPLOYEE_SET_PHASES_LINK = "https://www.dropbox.com/s/88ei27riqtbnniw/Timeline%20No%20Choice%20Employee%20Set%20condition%20-%20Phases.png?raw=1"
    NO_CHOICE_FIRM_SET_PHASES_LINK = "https://www.dropbox.com/s/ilmxll74ai5p8a5/Timeline%20No%20Choice%20Firm%20Set%20condition%20-%20Phases.png?raw=1"
    F1_E1_LINK = "https://www.dropbox.com/s/vfh7ih1pswe0lcl/Phase%201%20and%202%20-%20Firm%201%20and%20Employee%201.png?raw=1"
    F2_LINK = "https://www.dropbox.com/s/jnm18ngx4nb8bv1/Phase%201%20-%20Firm%202.png?raw=1"
    F3_LINK = "https://www.dropbox.com/s/9uc8v2mmk8x6rxo/Phase%201%20-%20Firm%203.png?raw=1"
    F3_ALTERNATE_LINK = "https://www.dropbox.com/scl/fi/2rjyswwoaxr4qmtkgqqe7/Phase-1-Firm-3-Capped-Condition-Alternate.png?rlkey=6x0ssmnfpn5t5cvcrfhokzlsg&dl=1"
    E2_CHOICE_LINK = "https://www.dropbox.com/s/2ughdsexlqqn7ls/Phase%202%20-%20Employee%202%20-%20Choice%20Condition.png?raw=1"
    E2_CHOICE_ALTERNATE_LINK = "https://www.dropbox.com/s/8utsd6kw31erfwe/Phase%202%20-%20Employee%202%20-%20Choice%20Condition%20Alternate.png?raw=1"
    E2_CAPPED_ALTERNATE_LINK = "https://www.dropbox.com/scl/fi/9s1j76p2mdrmxowx224xw/Phase-2-Employee-2-Capped-Condition-Alternate.png?rlkey=2a2z8u0iez0d8u61v8bcy0r1j&dl=1"
    E2_NO_CHOICE_LINK = "https://www.dropbox.com/s/dq6zszzvp9916eg/Phase%202%20-%20Employee%202.png?raw=1"
    E3_LINK = "https://www.dropbox.com/s/ec2ghmdb7kw2ww6/Phase%202%20-%20Employee%203.png?raw=1"
    PAYOFFS_LINK = "https://www.dropbox.com/s/ria5w7m3mz5yq7r/Phase%203%20-%20All.png?raw=1"


class Subsession(BaseSubsession):
    pass


def creating_session(subsession: Subsession):
    subsession.session.choice_condition = True # Decides whether this is a Choice or No Choice condition
    subsession.session.fixed_contract_condition = True  # Decides whether this is a fixed pay or incentive pay condition
    subsession.session.session_employee_set = False # Leave as "False" when running a choice condition. Decides whether employees or firms will set pay in No Choice condition
    subsession.session.capped_condition = True # Decides whether this is the capped condition. True == Capped Condition. False == NOT Capped Condition

    for player in subsession.get_players(): 
        player.participant.trust_part = False # Default is to set no one as receiving the trust question
        player.participant.employee_set_count = 0 # Counting starts at 0

#    if subsession.session.choice_condition == False: # If in the No Choice condition, then assign who sets pay. Otherwise, leave blank for the firm to decide later.
#        for group in subsession.get_groups():
#            group.employee_set = False


class Group(BaseGroup):
    pass

class Player(BasePlayer):
    consent = models.BooleanField()
    comp1 = models.BooleanField(choices = [[1, "True"], [0, "False"]]) # The label is defined on the html page.
    comp2 = models.IntegerField(label = "The lowest possible employee wage is ____ and the highest possible employee wage is ____.", choices = [[1, "15 Lira and 120 Lira"],[2, "20 Lira and 120 Lira"],[3, "15 Lira and 100 Lira"],[4, "20 Lira and 100 Lira"]],widget = widgets.RadioSelect)
    comp3 = models.IntegerField(label = "Who sets the employee's wage?", choices = [[1, "The firm"],[2, "Either the firm or employee, determined randomly"],[3, "The employee"],[4, "Either the firm or the employee, whoever the employee selects"],[5, "Either the firm or the employee, whoever the firm selects."]], widget = widgets.RadioSelect)
    comp4 = models.BooleanField(label = "If the firm decides to let the employee set the employee's wage and sets a cap, the employee may set their wage anywhere in the possible range of wages.", choices = [[1, "True"], [0, "False"]], widget = widgets.RadioSelect)
    comp5 = models.IntegerField(label = "The production level increases by increments of 0.1 and can range from ___ to ___ (inclusive)?", choices = [[1, "0.1 to 5.0"],[2, "0.1 to 1.0"],[3, "9.0 to 10.0"],[4, "1.0 to 10.0"]], widget = widgets.RadioSelect)
    comp6 = models.IntegerField(label = "What is the firm's payoff?")
    comp7 = models.IntegerField(label = "What is the employee's payoff?")
    comp8 = models.IntegerField(label = "What is the firm's payoff?")
    comp9 = models.IntegerField(label = "What is the employee's payoff?")


### FUNCTIONS ###
def comp1_error_message(player, value):
    if player.session.fixed_contract_condition == True:
        if value != True:
            return 'Incorrect, the correct answer is True. Employees will be awarded the wage regardless of production level. Please select the correct answer to continue.'
    else:
        if value != True:
            return 'Incorrect, the correct answer is True. The employee’s wage depends on production level. Please select the correct answer to continue.'


def comp2_error_message(player, value):
    if player.session.fixed_contract_condition == True:
        if value != 2:
            return 'Incorrect. The lowest possible employee wage is 20 Lira and the highest possible employee wage is 120 Lira. Please select the correct answer to continue.'
    else:
        if value != 1:
            return 'Incorrect. The lowest possible employee wage is 15 Lira and the highest possible employee wage is 120 Lira. Please select the correct answer to continue.'


def comp3_error_message(player, value):
    if player.session.choice_condition == True:
        if value != 5:
            return 'Incorrect, wage is set by either the firm or the employee, whoever the firm selects. Please select the correct answer to continue.'
    else:
        if player.session.session_employee_set == True:
            if value != 3:
                return 'Incorrect, wage is set by the employee. Please select the correct answer to continue.'
        else:
            if value != 1:
                return 'Incorrect, wage is set by the firm. Please select the correct answer to continue.'


def comp4_error_message(player, value):
    if value != False:
        return 'Incorrect, the correct answer is False. If the firm decides to let the employee set the employee’s wage and the firm sets a cap, the employee must set the wage below the firm’s cap.'


def comp5_error_message(player, value):
    if value != 2:
        return 'Incorrect, production level can range from 0.1 to 1.0 (inclusive). Please select the correct answer to continue.'


def comp6_error_message(player, value):
    if value != 20:
        return 'Incorrect. Don’t forget, firm payoff = (120 × production level) – wage. Given the wage of 100 Lira and the production level of 1.0, the firm payoff is calculated as (120 × 1.0) – 100 = 20. Please input the correct answer to continue.'


def comp7_error_message(player, value):
    if value != 82:
        return 'Incorrect. Don’t forget, employee payoff = wage – cost of production. Given the wage of 100 Lira and production level of 1.0, the employee payoff is calculated as 100 – 18 = 82. Please input the correct answer to continue.'


def comp8_error_message(player, value):
    if player.session.fixed_contract_condition == True:
        if value != 8:
            return 'Incorrect. Don’t forget, firm payoff = (120 × production level) – wage. Given the wage of 40 Lira and the production level of 0.4, the firm payoff is calculated as (120 × 0.4) – 40 = 8. Please input the correct answer to continue.'
    else:
        if value != 33:
            return 'Incorrect. Don’t forget, firm payoff = (120 × production level) – wage. Given the wage of 40 Lira and the production level of 0.4, the firm payoff is calculated as (120 × 0.4) – 15 = 33. Please input the correct answer to continue.'


def comp9_error_message(player, value):
    if player.session.fixed_contract_condition == True:
        if value != 36:
            return 'Incorrect. Don’t forget, employee payoff = wage – cost of production. Given the wage of 40 Lira and production level of 0.4, the employee payoff is calculated as 40 – 4 = 36. Please input the correct answer to continue.'
    else:
        if value != 11:
            return 'Incorrect. Don’t forget, employee payoff = wage – cost of production. Given the wage of 40 Lira and production level of 0.4, the employee payoff is calculated as 15 – 4 = 11. Please input the correct answer to continue.'


### PAGES ###
class IRB_Consent(Page):
    @staticmethod
    def is_displayed(player):
        return player.round_number == 1

    form_model = 'player'
    form_fields = ['consent']


class Disagree(Page):
    @staticmethod
    def is_displayed(player): # Display this page only if paricipant disagrees with the terms.
        if player.consent == False:
            return True


class Overview_Earnings(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number==1


class Labor_Market(Page):
    pass


class Phase_1(Page):
    pass


class Phase_2(Page):
    pass


class Phase_3(Page):
    pass


class Examples(Page):
    pass


class Ready(Page):
    pass


class Comprehension_1(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number==1

    form_model = 'player'
    form_fields = ['comp1'] 


class Comprehension_2(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number==1

    form_model = 'player'
    form_fields = ['comp2'] 


class Comprehension_3(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number==1

    form_model = 'player'
    form_fields = ['comp3'] 


class Comprehension_4(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.session.capped_condition == True
    
    form_model = 'player'
    form_fields = ['comp4']


class Comprehension_5(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number==1

    form_model = 'player'
    form_fields = ['comp5'] 


class Comprehension_6(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number==1

    form_model = 'player'
    form_fields = ['comp6', 'comp7', 'comp8', 'comp9'] 


page_sequence = [IRB_Consent, Disagree, Overview_Earnings, Labor_Market, Phase_1, Phase_2, Phase_3, Examples, Ready, Comprehension_1, Comprehension_2, Comprehension_3, Comprehension_4, Comprehension_5, Comprehension_6]