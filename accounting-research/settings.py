from os import environ


SESSION_CONFIGS = [
    dict(
        name='Study_One',
        app_sequence=['consent', 'study_one'],
        num_demo_participants=12,
    ),
]


# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']


SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=0.00, doc=""
)


PARTICIPANT_FIELDS = ['trust_part', 'employee_set_count']
SESSION_FIELDS = ['choice_condition', 'fixed_contract_condition', 'session_employee_set', 'capped_condition']


# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'


# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True
POINTS_CUSTOM_NAME = 'Lira'

ROOMS = [
    dict(
        name='study_lab',
        display_name='Accounting Research'
    ),
]

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')


DEMO_PAGE_INTRO_HTML = """ """


SECRET_KEY = '7127719641177'


INSTALLED_APPS = ['otree']