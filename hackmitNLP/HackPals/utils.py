import json
import re
import random
from json import JSONDecodeError
from typing import Dict, Any, List, Callable, Pattern
import random
import regexutils
import openai
from emora_stdm import Macro, Ngrams

#

OPENAI_API_KEY_PATH = 'openai_api.txt'
CHATGPT_MODEL = 'gpt-3.5-turbo'


class MacroMakeIntroFillerText(Macro):
    def run(self, ngrams: Ngrams, vars: Dict[str, Any], args: List[Any]):
        filler_text = ['Got it. Thank you!',
                       "I understand.",
                       "Sounds good!.",
                       "That's an awsome track to consider!",
                       "That field needs inovation for sure. Glad you are working on that "
                      ]
        return random.choice(filler_text)

class MacroMakeTechStackFillerText(Macro):
    def run(self, ngrams: Ngrams, vars: Dict[str, Any], args: List[Any]):
        filler_text = ['Working with this group of technologies excites me!',
                       "I think I see where you guys are going here ",
                       "This combo is intersting for sure",
                       "Hmm.... let me think",
                       "I see the potential here!"
                      ]
        return random.choice(filler_text)

class MacroMakeWhyFillerText(Macro):
    def run(self, ngrams: Ngrams, vars: Dict[str, Any], args: List[Any]):
        filler_text = ["That's a compelling reason, and it sounds like you're passionate about it!",
                       "Ah, I see. That's a unique approach!",
                       "Interesting! Your idea could really make a difference in that field.",
                       "Wow, that's a thoughtful choice. It sounds like you've done your research.",
                       "Your reasoning is solid. I can see a lot of potential in your idea."
                      ]
        return random.choice(filler_text)


class MacroMakeSummary(Macro):
    def run(self, ngrams: Ngrams, vars: Dict[str, Any], args: List[Any]):
        output = gpt_completion(
            f"Given the user's interest in the hackathon track: {vars.get('TRACK', 'n/a')}, "
            f"their chosen tech stack: {vars.get('TECH_STACK', 'n/a')}, and their reason for choosing this track: {vars.get('WHY_RESPONSE', 'n/a')}, "
            f"can you synthesize ax very detailed recap of this info? "
            f"Respond with only the content of the summary. It should be extremely detailed and show that you truly "
            f"listened. Respond as if speaking to the user and ask if you have the details right in yes or no format."
        )
        vars['SUMMARY'] = output
        return vars['SUMMARY']


# Macro for suggesting hackathon project ideas
class MacroMakeSuggestions(Macro):
    def run(self, ngrams: Ngrams, vars: Dict[str, Any], args: List[Any]):
        output = gpt_completion(
            f"Given the user's interest in the hackathon track: {vars.get('TRACK', 'n/a')}, "
            f"their chosen tech stack: {vars.get('TECH_STACK', 'n/a')}, and their reason for choosing this track: {vars.get('WHY_RESPONSE', 'n/a')}, "
            f"can you suggest a detailed project idea that aligns with these preferences?"
        )
        vars['SUGGESTION'] = output
        return vars['SUGGESTION']


class MacroGPTJSON(Macro):
    def __init__(self, request: str, full_ex: Dict[str, Any], empty_ex: Dict[str, Any] = None,
                 set_variables: Callable[[Dict[str, Any], Dict[str, Any]], None] = None):
        """
        :param request: the task to be requested regarding the user input (e.g., How does the speaker want to be called?).
        :param full_ex: the example output where all values are filled (e.g., {"call_names": ["Mike", "Michael"]}).
        :param empty_ex: the example output where all collections are empty (e.g., {"call_names": []}).
        :param set_variables: it is a function that takes the STDM variable dictionary and the JSON output dictionary and sets necessary variables.
        """
        self.request = request
        self.full_ex = json.dumps(full_ex)
        self.empty_ex = '' if empty_ex is None else json.dumps(empty_ex)
        self.check = re.compile(regexutils.generate(full_ex))
        self.set_variables = set_variables

    def run(self, ngrams: Ngrams, vars: Dict[str, Any], args: List[Any]):
        examples = f'{self.full_ex} or {self.empty_ex} if unavailable' if self.empty_ex else self.full_ex
        prompt = f'{self.request} Respond in the JSON schema such as {examples}: {ngrams.text().strip()}'
        output = gpt_completion(prompt)
        if not output: return False

        try:
            d = json.loads(output)
        except JSONDecodeError:
            print(f'Invalid: {output}')
            return False

        if self.set_variables:
            self.set_variables(vars, d)
        else:
            vars.update(d)

        return True


class MacroNLG(Macro):
    def __init__(self, generate: Callable[[Dict[str, Any]], str]):
        self.generate = generate

    def run(self, ngrams: Ngrams, vars: Dict[str, Any], args: List[Any]):
        return self.generate(vars)


class MacroGPTJSONNLG(MacroGPTJSON, MacroNLG):
    def __init__(self, request: Callable, full_ex: Dict[str, Any], empty_ex: Dict[str, Any] = None,
                 set_variables: Callable[[Dict[str, Any], Dict[str, Any]], None] = None,
                 generate: Callable[[Dict[str, Any]], str] = None):
        MacroGPTJSON.__init__(self, request, full_ex, empty_ex, set_variables)
        MacroNLG.__init__(self, generate)

    def run(self, ngrams: Ngrams, vars: Dict[str, Any], args: List[Any]):
        request = self.request(vars) if callable(self.request) else self.request
        examples = f'{self.full_ex} or {self.empty_ex} if unavailable' if self.empty_ex else self.full_ex
        prompt = f'{request} Respond in the JSON schema such as {examples}: {ngrams.text().strip()}'
        output = gpt_completion(prompt)
        if not output: return False

        try:
            d = json.loads(output)
        except JSONDecodeError:
            print(f'Invalid: {output}')
            return False

        if self.set_variables:
            self.set_variables(vars, d)
        else:
            vars.update(d)

        return True


# Function for GPT completion, adjusted for hackathon context
def gpt_completion(input: str, regex: Pattern = None) -> str:
    response = openai.ChatCompletion.create(
        model=CHATGPT_MODEL,
        messages=[
            {'role': 'system', 'content': 'You are a helpful assistant for hackathon participants.'},
            {'role': 'user', 'content': input},
        ],
        temperature=0.4,
    )
    output = response['choices'][0]['message']['content'].strip()
    if regex is not None:
        m = regex.search(output)
        output = m.group().strip() if m else None
    return output