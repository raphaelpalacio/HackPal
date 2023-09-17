import random
import re
import json
import openai

from emora_stdm import DialogueFlow
from utils import MacroGPTJSON, MacroNLG, MacroGPTJSONNLG, gpt_completion
from macros import macros
from emora_stdm import Macro, Ngrams

PATH_API_KEY = 'openai_api.txt'


def api_key(filepath=PATH_API_KEY) -> str:
    fin = open(filepath)
    return fin.readline().strip()


openai.api_key = api_key()

introduction = {
    'state': 'start',
    '`Hey! I\'m HackPal, here to help brainstorm your hackathon ideas! What\'s your name?`': {
        '#SET_CALL_NAME': {
            '`It\'s nice to meet you `#GET_CALL_NAME`! What track are you thinking of doing?`':{
                '#GET_HACKATHON_TRACK': 'get_techstack_and_idea'
            }
        }
    }
}


intermediate = {
    'state': 'get_techstack_and_idea',
    '`I think I can work with this track! What tech stack were you thinking of working with?`': {
        '#SET_TECH_STACK': {
            '`To make sure that you are doing this idea for the right reason why do you want to do this particular track and what is the end goal?`': {
                '#SET_WHY_RESPONSE': {
                    '#WHY_FILLER`Thank you for sharing your in-sight and why you want to pursue this!`#GET_SUMMARY': {
                        '[{yes, yeah, correct, right, yuh, yep, yeap, yup}]': {
                            '`Great! Let\'s move on to the next step.`': 'give_suggestion'
                        },
                        '[{no, nope, not really, not at all, nah, incorrect, not correct, not right}]': {
                            '`No worries! Can you please tell me what I didn\'t get right, and what I should have understood?`': 'get_techstack_and_idea'
                        }
                    }
                }
            }
        }
    }
}

last_part = {
    'state': 'give_suggestion',
    '#MAKE_SUGGESTIONS`This is an idea that I have came up given what you have provided me. Does this sound right?`': {
        '[{yes, yeah, correct, right, yuh, yep, yeap, yup}]': {
            '`Alright, thank you for using HackPal! I hope I have been helpful! Happy Hacking!!`': 'end',
        },
        '[{no, nope, not really, not at all, nah, incorrect, not correct, not right}]': {
            '`No worries! Let\'s revisit your tech stack and idea.`': 'get_techstack_and_idea'
        }
    }
}


# df = DialogueFlow('start', end_state='end')
# df.local_transitions(introduction)
# df.local_transitions(intermediate)
# df.local_transitions(last_part)
#
# df.add_macros(macros)

def run_hackMIT(state, user_input):
    df = DialogueFlow(state, end_state='end')
    df.local_transitions(introduction)
    df.local_transitions(intermediate)
    df.local_transitions(last_part)
    df.add_macros(macros)

    next_state, response = df.run_step(state, user_input)
    return next_state, response



# if __name__ == '__main__':
#     df.run(debugging=False)
