import random
import re
import json
from enum import Enum
from typing import Dict, Any, List

import openai

from emora_stdm import DialogueFlow
from emora_stdm import Macro, Ngrams

from utils import MacroGPTJSON, MacroNLG, MacroGPTJSONNLG, gpt_completion, MacroMakeIntroFillerText, \
    MacroMakeTechStackFillerText, MacroMakeWhyFillerText, MacroMakeSummary, MacroMakeSuggestions

PATH_API_KEY = 'openai_api.txt'


def api_key(filepath=PATH_API_KEY) -> str:
    fin = open(filepath)
    return fin.readline().strip()


openai.api_key = api_key()


class User(Enum):
    call_name = 'call_name'
    participation_status = 'participation_status'
    hackathon_type = 'hackathon_type'
    available_tracks = 'available_tracks'
    user_preferences = 'user_preferences'
    PROBLEM_SUMMARY = 'problem_summary'


early_avaliable_states = ['get_techstack_and_idea']


def get_call_name(vars: Dict[str, Any]):
    ls = vars[User.call_name.name]
    return ls


def set_call_names(vars: Dict[str, Any], user: Dict[str, Any]):
    vars[User.call_name.value] = user[User.call_name.value]


def generate_prompt_pre(vars: Dict[str, Any]) -> str:
    return ("What hackathon track are you interested in? For example, are you interested in healthcare, social good, "
            "finance, etc.?")


def get_hackathon_track(vars: Dict[str, Any], user: Dict[str, Any]) -> None:
    vars['TRACK'] = user['TRACK']


def set_tech_stack(vars: Dict[str, Any], user: Dict[str, Any]) -> None:
    vars['TECH_STACK'] = user['TECH_STACK']


def set_why_response(vars: Dict[str, Any], user: Dict[str, Any]) -> None:
    vars['WHY_RESPONSE'] = user.get('WHY_RESPONSE', 'n/a')






macros = {
    'SET_CALL_NAME': MacroGPTJSON(
        'What does the speaker want to be called? Give only one name. Respond in the one-line JSON format such as {'
        '"call_names": ["Mike", "Michael"]}: ',
        {User.call_name.name: ["Mike", "Michael"], 'NEXT_STATE': '...'},
        {User.call_name.name: "n/a", 'NEXT_STATE': '...'},
        set_call_names
    ),

    # New Macro for setting the hackathon track
    'GET_HACKATHON_TRACK': MacroGPTJSON(
        'What hackathon track are you interested in? For example, healthcare, social good, finance, etc.',
        {'TRACK': ["healthcare", "social good", "finance"], 'NEXT_STATE': '...'},
        {'TRACK': "n/a", 'NEXT_STATE': '...'},
        get_hackathon_track  # Function to set the hackathon track
    ),

    # New Macro for setting the tech stack
    'SET_TECH_STACK': MacroGPTJSON(
        'What tech stack do you plan to use? For example, Python, JavaScript, Java, etc.',
        {'TECH_STACK': ["Python", "JavaScript", "Java"], 'NEXT_STATE': '...'},
        {'TECH_STACK': "n/a", 'NEXT_STATE': '...'},
        set_tech_stack  # Function to set the tech stack
    ),

    'SET_WHY_RESPONSE': MacroGPTJSON(
        'Why do you want to pursue this track?',
        {
            'WHY_RESPONSE': 'I am passionate about education and want to make a difference.',
            'NEXT_STATE': '...'
        },
        {
            'WHY_RESPONSE': 'n/a',
            'NEXT_STATE': '...'
        },
        set_why_response  # Use the new function here
    ),
    # 'GET_HACKATHON_RESPONSE': MacroGPTJSONNLG(
    #
    # ),

    'GET_CALL_NAME': MacroNLG(get_call_name),
    'FILLER_RESPONSE': MacroMakeIntroFillerText(),
    'GET_SUMMARY': MacroMakeSummary(),
    'MAKE_SUGGESTIONS': MacroMakeSuggestions(),
    'TECH_STACK_FILLER': MacroMakeTechStackFillerText(),
    'WHY_FILLER': MacroMakeWhyFillerText(),

}
