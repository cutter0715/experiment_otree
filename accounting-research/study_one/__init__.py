# from re import S
from otree.api import *
# from settings import SESSION_FIELDS


doc = """
Your app description
"""


### MODELS ###
class C(BaseConstants):
    NAME_IN_URL = 'study'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 6 #This should be set to the number of matchups you have in a session. For the sake of testing this can be 2 but usually you will want 6.
    FIRM_ROLE = "firm"
    EMPLOYEE_ROLE = "employee"
    PRODUCTION_LEVELS = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    production = models.FloatField(label = "Please select your production level.", choices = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]) #This is the employee's production level level
    wage = models.IntegerField(min = 20) #This is the wage, regardless of who sets it.
    employee_set = models.BooleanField(label = "Who will set the employee's wage?", choices = [[True, "The employee"], [False, "The firm"]], widget = widgets.RadioSelect) #Contract type, default is firm set
    group_enter_market = models.BooleanField(label = "Would you like to enter the market?", choices = [[True, "Enter"],[False, "Exit"]], widget = widgets.RadioSelect) #Individuals choose to enter the labor market and so both have this kill switch.
    group_id = models.IntegerField() #This variable will help me assign trust groups.
    cap = models.IntegerField(min = 20, max = 120) #This is the cap set by the firm if they choose to delegate pay in the Choice - Capped condition.


class Player(BasePlayer):
    player_enter_market = models.BooleanField(label = "Would you like to enter the market?", choices = [[True, "Enter"],[False, "Exit"]], widget = widgets.RadioSelect) #Individuals choose to enter the labor market and so both have this kill switch.
    age = models.IntegerField(label = 'What is your age (in years)?') #Post-experimental questionaire
    gender = models.IntegerField(label = 'With which gender do you identify most?', choices = [[1, 'Male'], [2, 'Female'], [3, 'Non-Binary'], [4, 'Prefer not to answer']], widget = widgets.RadioSelect) #Post-experimental questionaire
    education = models.IntegerField(label = 'What is your highest level of education completed?', choices = [[1, 'No high school degree or equivalent'], [2, 'High school degree or equivalent'], [3, 'Some college'], [4, 'Undergraduate degree'], [5,'Graduate degree'], [6, 'Prefer not to answer'],], widget = widgets.RadioSelect) #Post-experimental questionaire
    experience = models.IntegerField(label = 'How many years of full-time work experience do you have?') #Post-experimental questionaire
    prior_wage_setting = models.BooleanField(label = 'As an employee, have you ever had experience setting your own wage before? Note, setting your wage is different than a negotiation.')
    trust = models.IntegerField(choices = [1,2,3,4,5,6,7], widget = widgets.RadioSelect) #Record how much the firm trusts the employee or the employee feels trusted by the firm.
    name = models.StringField(label='Name:')#Information required for compensation after the study
    email = models.StringField(label='Email:') #Information required for compensation after the study
    peq1 = models.LongStringField(label = "How did you decide whether you or the employee would set the employee's wage?")
    peq2 = models.LongStringField(label = "How did you decide the employee's wage level?")
    peq3 = models.LongStringField(label = "How did you decide your own wage level?")
    peq4 = models.LongStringField(label = "To what extent did you feel responsible for determining the firm's and your own payoff?")
    peq5 = models.LongStringField(label = "To what extent would you feel guilty choosing the lowest production level?")
    peq6 = models.LongStringField(label = "How do you see yourself? Are you generally a person who is fully prepared to take risks or do you try to avoid taking risks?")
    peq7 = models.LongStringField(label = "How hard was the labor market task?")
    peq8 = models.LongStringField(label = "How enjoyable was the labor market task?")
    peq9 = models.BooleanField(label = "As an employee, have you ever had experience setting your own wage before? Note, setting your wage is different than a negotiation.")
    peq10 = models.LongStringField(label = "How did you decide the employee's maximum level of pay that the employee could set for themselves?")
    rec1 = models.IntegerField(label = 'If someone does me a favor, I am prepared to return it.', choices=[1, 2, 3, 4, 5, 6, 7], widget=widgets.RadioSelect)
    rec2 = models.IntegerField(label = 'If I suffer a serious wrong, I will take revenge as soon as possible, no matter what the cost.', choices=[1, 2, 3, 4, 5, 6, 7], widget=widgets.RadioSelect)
    rec3 = models.IntegerField(label = 'If someone puts me in a difficult position, I will do the same to him/her.', choices=[1, 2, 3, 4, 5, 6, 7], widget=widgets.RadioSelect)
    rec4 = models.IntegerField(label = 'I go out of my way to help somebody who has been kind to me before.', choices=[1, 2, 3, 4, 5, 6, 7], widget=widgets.RadioSelect)
    rec5 = models.IntegerField(label = 'If somebody offends me, I will offend him/her back.', choices=[1, 2, 3, 4, 5, 6, 7], widget=widgets.RadioSelect)
    rec6 = models.IntegerField(label = 'I am ready to undergo personal costs to help somebody who helped me before.', choices=[1, 2, 3, 4, 5, 6, 7], widget=widgets.RadioSelect)


#### FUNCTIONS ###
def right_rotate(lst, r_num): #Takes a list (lst) and right rotates it by r_num positions. For example, given lst = [1, 2, 3] and r_num = 1, right_rotate returns [3, 1, 2].
    return lst[-r_num:] + lst[0:len(lst)-r_num]


def shuffle_groups_assign_trust(subsession):
    odd_players = [1,3,5,7,9,11]
    even_players = [2,4,6,8,10,12]
    for s in subsession.in_rounds(1, C.NUM_ROUNDS):
        round_num = 1
        even_players = right_rotate(even_players, round_num)# Only the even players are rotated, then they are paired back with the odd players list.
        new_matrix = [[i, j] for i,j in zip(odd_players,even_players)]
        s.set_group_matrix(new_matrix)
        round_num += 1

    group_count = 1
    for g in subsession.get_groups():
        g.group_id = group_count
        if g.group_id % 2 == 1:
            for player in g.get_players():
                player.participant.trust_part = True
        group_count += 1


def cost_of_production(production):
    coe_dict = {
        0.1: 0,
        0.2: 1,
        0.3: 2,
        0.4: 4,
        0.5: 6,
        0.6: 8,
        0.7: 10,
        0.8: 12,
        0.9: 15,
        1.0: 18,
    }
    return coe_dict[production]


def fill_payoff_table(player: Player, data):
    firm_poss_payoff = []
    employee_poss_payoff = []
    fill_table = True

    if data.isnumeric() == False or int(data) < 20 or int(data) > 120:
        fill_table = False
        response = dict(type='error', message='Your wage amount is not valid.\n Please enter a whole number between 20 and 120.')
        return {player.id_in_group: response}
    elif player.session.capped_condition == True and player.group.employee_set == True and player.role == C.EMPLOYEE_ROLE:
        if int(data) > player.group.cap:
            fill_table = False
            response = dict(type='error', message="Your wage amount is not valid due to the wage cap set by the firm.\n Please enter a number less than or equal to the firm's cap of "+str(player.group.cap)+".")
            return {player.id_in_group: response}
    
    if fill_table == True:
        data = int(data)
        if player.session.fixed_contract_condition == True:
            for i in C.PRODUCTION_LEVELS: # Fixed payoffs
                firm_payoff = 120 * i - data
                firm_poss_payoff.append(int(firm_payoff))
                employee_payoff = data - cost_of_production(i)
                employee_poss_payoff.append(employee_payoff)
        else:
            for i in C.PRODUCTION_LEVELS: # Incentive payoffs
                if i == 1:
                    firm_payoff = 120 * i - data
                    firm_poss_payoff.append(int(firm_payoff))
                    employee_payoff = data - cost_of_production(i)
                    employee_poss_payoff.append(employee_payoff)
                else:
                    firm_payoff = 120 * i - 15
                    firm_poss_payoff.append(int(firm_payoff))
                    employee_payoff = 15 - cost_of_production(i)
                    employee_poss_payoff.append(employee_payoff)
        response = dict(type='possible_payoffs', f1 = firm_poss_payoff[0], f2 = firm_poss_payoff[1], f3 = firm_poss_payoff[2], f4 = firm_poss_payoff[3], f5 = firm_poss_payoff[4], f6 = firm_poss_payoff[5], f7 = firm_poss_payoff[6], f8 = firm_poss_payoff[7], f9 = firm_poss_payoff[8], f10 = firm_poss_payoff[9], e1 = employee_poss_payoff[0], e2 = employee_poss_payoff[1], e3 = employee_poss_payoff[2], e4 = employee_poss_payoff[3], e5 = employee_poss_payoff[4], e6 = employee_poss_payoff[5], e7 = employee_poss_payoff[6], e8 = employee_poss_payoff[7], e9 = employee_poss_payoff[8], e10 = employee_poss_payoff[9])
        return {player.id_in_group: response}


def wage_max(player):
    if player.session.capped_condition == True and player.employee_set == True:
        return player.cap
    else:
        return 120


def player_payoff(player: Player):
    if player.role == C.EMPLOYEE_ROLE: #Employee payoff calculation
        if player.session.fixed_contract_condition == True or player.group.production == 1: #Fixed Contract or Output Contract where an production level of 1 is provided
            player.payoff = player.group.wage - cost_of_production(player.group.production)
        else: #Output Contract where an production level less than 1 is provided
            player.payoff = 15 - cost_of_production(player.group.production)
    elif player.role == C.FIRM_ROLE: #Firm payoff calculation
        if player.session.fixed_contract_condition == True or player.group.production == 1: #Fixed Contract or Output Contract where an production level of 1 is provided
            player.payoff = 120 * player.group.production - player.group.wage
        else: #Output Contract where an production level less than 1 is provided
            player.payoff = 120 * player.group.production - 15


### PAGES ###
class Form_groups(WaitPage):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1
    
    wait_for_all_groups = True

    after_all_players_arrive = shuffle_groups_assign_trust
    
    title_text = "Please wait!"
    body_text = ""


class Begin(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1


class Start_round(WaitPage):
    title_text = "Please wait!"
    body_text = ""


class Firm1(Page): #The firm decides whether to enter the labor market.
    @staticmethod
    def is_displayed(player: Player):
        return player.role == C.FIRM_ROLE

    form_model = 'player'
    form_fields = ['player_enter_market']

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.group.group_enter_market = player.player_enter_market


class Firm1_wait(WaitPage):
    @staticmethod
    def is_displayed(player):
        return player.role == C.EMPLOYEE_ROLE

    title_text = "Please wait!"
    body_text = ""


class Firm_trust(Page):
    @staticmethod
    def is_displayed(player):
        return player.group.group_enter_market == True and player.participant.trust_part == True and player.role == C.FIRM_ROLE

    form_model = 'player'
    form_fields = ['trust']


class Firm_trust_wait(WaitPage):
    @staticmethod
    def is_displayed(player):
        return player.group.group_enter_market == True and player.role == C.EMPLOYEE_ROLE

    title_text = "Please wait!"
    body_text = ""


class Firm2(Page): # Firm decides whether to offer employee-set or firm-set compensation.
    @staticmethod
    def is_displayed(player: Player):
        if player.session.choice_condition == True:
            return player.group.group_enter_market == True and player.session.choice_condition == True and player.role == C.FIRM_ROLE
        else:
            return False

    form_model = 'group'
    form_fields = ['employee_set']

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if player.group.employee_set == True:
            player.participant.employee_set_count += 1


class Firm2_wait(WaitPage):
    @staticmethod
    def is_displayed(player):
        if player.group.group_enter_market == True and player.session.choice_condition == True and player.role == C.EMPLOYEE_ROLE:
            return True
        else:
            return False

    title_text = "Please wait!"
    body_text = ""


class Firm3(Page): # Firm sets employee wage or Firm sets employee cap
    @staticmethod
    def is_displayed(player: Player):
        if player.group.group_enter_market == True and player.role == C.FIRM_ROLE:
            group_employee_set = player.group.field_maybe_none('employee_set')
            if player.session.choice_condition == False and player.session.session_employee_set == False:
                return True
            elif player.session.choice_condition == True and group_employee_set == False:
                return True
            elif player.session.choice_condition == True and group_employee_set == True and player.session.capped_condition == True:
                return True
            else:
                return False
        else:
            return False

    form_model = 'group'
    @staticmethod
    def get_form_fields(player: Player):
        if player.session.capped_condition == True and player.group.employee_set == True:
            return ['cap']
        else:
            return ['wage']

    @staticmethod
    def live_method(player, data):
        return fill_payoff_table(player, data)


class Firm3_wait(WaitPage):
    @staticmethod
    def is_displayed(player):
        if player.group.group_enter_market == True and player.role == C.EMPLOYEE_ROLE:
            group_employee_set = player.group.field_maybe_none('employee_set')
            if player.session.choice_condition == False and player.session.session_employee_set == False:
                return True
            elif player.session.choice_condition == True and group_employee_set == False:
                return True
            elif player.session.choice_condition == True and group_employee_set == True and player.session.capped_condition == True:
                return True
            else:
                return False
        else:
            return False

    title_text = "Please wait!"
    body_text = ""


class Employee1(Page): # Employee decides whether to accept firm offer (if firm set) or employee makes wage request (if employee-set)
    @staticmethod
    def is_displayed(player):
        return player.group.group_enter_market == True and  player.role == C.EMPLOYEE_ROLE

    form_model = 'player'
    form_fields = ['player_enter_market']

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.group.group_enter_market = player.player_enter_market


class Employee1_wait(WaitPage):
    @staticmethod
    def is_displayed(player):
        if player.group.group_enter_market == True  and player.role == C.FIRM_ROLE:
            return True
        else:
            return False
    
    title_text = "Please wait!"
    body_text = ""


class Employee2(Page): #Employee chooses wage amount
    @staticmethod
    def is_displayed(player):
        return player.group.group_enter_market == True and player.role == C.EMPLOYEE_ROLE

    form_model = 'group'
    @staticmethod
    def get_form_fields(player: Player):
        group_employee_set = player.group.field_maybe_none('employee_set')
        if player.session.session_employee_set == True:
            return ['wage']
        elif group_employee_set == True:
            return ['wage']
        else:
            return

    @staticmethod
    def vars_for_template(player: Player):
        group_employee_set = player.group.field_maybe_none('employee_set')
        if player.session.choice_condition == False and player.session.session_employee_set == True:
            return dict(
                employee_set = False,
            )
        elif group_employee_set == True:
            return dict(
                employee_set =  True,
            )
        else:
            return dict(
                employee_set = False,
            )

    @staticmethod
    def live_method(player, data):
        return fill_payoff_table(player, data)

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        group_employee_set = player.group.field_maybe_none('employee_set')
        if group_employee_set == True:
            player.participant.employee_set_count += 1


class Employee2_wait(WaitPage):
    @staticmethod
    def is_displayed(player):
        return player.group.group_enter_market == True and player.role == C.FIRM_ROLE

    title_text = "Please wait!"
    body_text = ""


class Employee_trust(Page):
    @staticmethod
    def is_displayed(player):
        return player.group.group_enter_market == True and player.participant.trust_part == True and player.role == C.EMPLOYEE_ROLE

    form_model = 'player'
    form_fields = ['trust']


class Employee_trust_wait(WaitPage):
    @staticmethod
    def is_displayed(player):
        return player.group.group_enter_market == True and player.role == C.FIRM_ROLE

    title_text = "Please wait!"
    body_text = ""


class Employee3(Page): #Employee chooses production level
    @staticmethod
    def is_displayed(player):
        return player.group.group_enter_market == True and player.role == C.EMPLOYEE_ROLE

    form_model = 'group'
    form_fields = ['production']

    @staticmethod
    def vars_for_template(player: Player):
        firm_poss_payoff = []
        employee_poss_payoff = []
        if player.session.fixed_contract_condition == True:
            for i in C.PRODUCTION_LEVELS: # Fixed payoffs
                firm_payoff = 120 * i - player.group.wage
                firm_poss_payoff.append(int(firm_payoff))
                employee_payoff = player.group.wage - cost_of_production(i)
                employee_poss_payoff.append(employee_payoff)
        else:
            for i in C.PRODUCTION_LEVELS: # Incentive payoffs
                if i == 1:
                    firm_payoff = 120 * i - player.group.wage
                    firm_poss_payoff.append(int(firm_payoff))
                    employee_payoff = player.group.wage - cost_of_production(i)
                    employee_poss_payoff.append(employee_payoff)
                else:
                    firm_payoff = 120 * i - 15
                    firm_poss_payoff.append(int(firm_payoff))
                    employee_payoff = 15 - cost_of_production(i)
                    employee_poss_payoff.append(employee_payoff)
        return dict(
            f1 = firm_poss_payoff[0], f2 = firm_poss_payoff[1], f3 = firm_poss_payoff[2], f4 = firm_poss_payoff[3], f5 = firm_poss_payoff[4], f6 = firm_poss_payoff[5], f7 = firm_poss_payoff[6], f8 = firm_poss_payoff[7], f9 = firm_poss_payoff[8], f10 = firm_poss_payoff[9], e1 = employee_poss_payoff[0], e2 = employee_poss_payoff[1], e3 = employee_poss_payoff[2], e4 = employee_poss_payoff[3], e5 = employee_poss_payoff[4], e6 = employee_poss_payoff[5], e7 = employee_poss_payoff[6], e8 = employee_poss_payoff[7], e9 = employee_poss_payoff[8], e10 = employee_poss_payoff[9]) 


class Employee3_wait(WaitPage):
    @staticmethod
    def is_displayed(player):
        return player.group.group_enter_market == True and player.role == C.FIRM_ROLE

    title_text = "Please wait!"
    body_text = ""


class Calculation_wait(WaitPage): #Calculate firm and employee payoff
    @staticmethod
    def is_displayed(player: Player):
        return player.group.group_enter_market == True

    @staticmethod
    def after_all_players_arrive(group: Group):
        for player in group.get_players():
            player_payoff(player)

    title_text = "Please wait!"
    body_text = "Your payoff is being calculated."


class Payoffs(Page): #Display firm and employee payoff
    pass


class PEQ(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS


class PEQ1(Page):
    @staticmethod
    def is_displayed(player: Player):
        if player.round_number == C.NUM_ROUNDS:
            if player.role == C.FIRM_ROLE and player.session.choice_condition == False and player.session.session_employee_set == True:
                return False
            elif player.role == C.EMPLOYEE_ROLE and player.session.choice_condition == False and player.session.session_employee_set == False:
                return False
            elif player.role == C.EMPLOYEE_ROLE and player.session.choice_condition == True and player.participant.employee_set_count == 0:
                return False
            else:
                return True
        
    form_model = 'player'
    @staticmethod
    def get_form_fields(player: Player):
        if player.role == C.FIRM_ROLE and player.session.choice_condition == True:
            if player.session.capped_condition == True and player.participant.employee_set_count == 0:
                return ['peq1', 'peq2']
            elif player.session.capped_condition == True and player.participant.employee_set_count > 0:
                return ['peq1', 'peq10', 'peq2']
            elif player.session.capped_condition == False and player.participant.employee_set_count < C.NUM_ROUNDS:
                return ['peq1', 'peq2']
            else:
                return ['peq1'] 
        elif player.role == C.FIRM_ROLE and player.session.choice_condition == False:
            return ['peq2']
        elif player.role == C.EMPLOYEE_ROLE:
            return ['peq3']
    
    
class PEQ2(Page):
    @staticmethod
    def is_displayed(player: Player):
        if player.round_number == C.NUM_ROUNDS and player.role == C.EMPLOYEE_ROLE:
            return True

    form_model = 'player'
    form_fields = ['peq4', 'peq5', 'peq6', 'peq7', 'peq8']

class PEQ3(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS

    form_model = 'player'
    form_fields = ['rec1', 'rec2', 'rec3', 'rec4', 'rec5', 'rec6']


class PEQ4(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS

    form_model = 'player'
    form_fields = ['age', 'gender', 'education', 'experience', 'prior_wage_setting']


class Contact_info(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS

    form_model = 'player'
    form_fields = ['name', 'email']


class Close_screen(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS


page_sequence = [Form_groups, Begin, Start_round, Firm1, Firm1_wait, Firm_trust, Firm_trust_wait, Firm2, Firm2_wait, Firm3, Firm3_wait, Employee1, Employee1_wait, Employee2, Employee2_wait, Employee_trust, Employee_trust_wait, Employee3, Employee3_wait, Calculation_wait, Payoffs, PEQ, PEQ1, PEQ2, PEQ3, PEQ4, Contact_info, Close_screen]