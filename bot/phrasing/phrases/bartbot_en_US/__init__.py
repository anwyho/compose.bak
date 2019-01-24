#  _                _   _           _
# | |__   __ _ _ __| |_| |__   ___ | |_
# | '_ \ / _` | '__| __| '_ \ / _ \| __|
# | |_) | (_| | |  | |_| |_) | (_) | |_
# |_.__/ \__,_|_|   \__|_.__/ \___/ \__|
# Get all things BART from your Messenger!

from typing import (Dict, List, Optional)  # noqa

from bot.phrasing.emojis import emojis

# NOTE:
# 1. Each string should be an f-string
# 2. Options should be double-bracketed to escape f-string
# 3. Emojis should be single-bracketed to be evaluated
# 4. Ideally, there should be no whitespace on the outsides,
#   but str.strip() is called anyway
# 5. Call bot.phrasing.emojis.print_all_emojis() for easily copy-paste

locale = "en_US"


bye: List[str] = [
    f"See ya later!",
    f"Adios!",
    f"Bye bye!",
    f"Zai jian!",
    f"Take care.",
    f"Love you!",
    f"BART safe!",
    f"Bye!",
    f"Tootles!",
    f"TTFN",
    f"TTYL",
    f"Later!",
    f"Until next time!",
]

byeWName: List[str] = [
    f"See ya later {{firstName}}!",
    f"Bye {{firstName}}!",
    f"TTYL {{firstName}}!",
    f"Until next time, {{firstName}}!",
]

cta: List[str] = [
    f"Where are you headed?",
    f"Where are you headed today?",
    f"Where would you like to go?",
    f"Where would you like to go today?",
    f"Where are you off to?",
    f"Where are you off to today?",
    f"Where to?",
    f"Where to, boss?"
    f"Where ya headed?",
    f"Where ya headed today?",
    f"Headed anywhere?",
]

ctaWName: List[str] = [
    f"Where are you headed {{firstName}}?",
    f"Where are you headed today {{firstName}}?",
    f"Where would you like to go {{firstName}}?",
    f"Where would you like to go today {{firstName}}?",
    f"Where are you off to {{firstName}}?",
    f"Where are you off to today {{firstName}}?",
    f"Where to, {{firstName}}?",
    f"Where ya headed {{firstName}}?",
    f"Where ya headed today {{firstName}}?",
    f"Headed anywhere {{firstName}}?",
]

delivery: List[str] = [
    f"Here it is!",
    f"Here you go!",
    f"Here ya go!",
    f"There ya go!",
    f"Special delivery!",
]

deliveryWName: List[str] = [
    f"Here ya go {{firstName}}!",
    f"Special delivery, for {{firstName}}",
    f"Here it is {{firstName}}!",
    f"There ya go {{firstName}}!",
]

hello: List[str] = [
    f"Greetings.",
    f"Hello there.",
    f"Sup!",
    f"Hello from the other side!",
    f"Good day!",
    f"Good {{timeOfDayNoNight}}!",
    f"Hi there!",
    f"Hello!",
    f"Hi!",
    f"Hey, didn't see ya there!",
]

helloWName: List[str] = [
    f"Sup {{firstName}}!",
    f"Good day, {{firstName}}!",
    f"Good {{timeOfDayNoNight}} {{firstName}}!",
    f"Hello {{firstName}}!",
    f"Hi {{firstName}}!",
]

helpText: List[str] = [
    f"[TODO: Fill in this help text.]",
]

sorry: List[str] = [
    f"Sorry about that!",
    f"Oops! {emojis['shushing_face']}",
    f"Oh no. {emojis['face_screaming_in_fear']}",
    f"Hmm...",
    f"Darn. {emojis['crying_face']}",
    f"Shucks. {emojis['crying_face']}",
    f"That's embarrassing... {emojis['grinning_face_with_sweat']}",
    f"Aiya!",
    f"Whoops! {emojis['dizzy_face']}",
    f"My bad! {emojis['grinning_face_with_sweat']}",
]

sorryWName: List[str] = [
    f"Sorry about that {{firstName}}!",
    f"Sorry {{firstName}}...",
    f"My bad, {{firstName}}!",
]

thanks: List[str] = [
    f"Thanks! {emojis['smiling_face_with_smiling_eyes']}",
    f"Thanks! {emojis['thumbs_up']}",
    f"Thanks!",
    f"Thankya!",
    f"Wow thanks!",
    f"tysm!",
    f"TY!",
    f"Xie xie!",
]

thanksWName: List[str] = [
    f"Thanks {{firstName}}! {emojis['smiling_face_with_smiling_eyes']}",
    f"Thanks {{firstName}}! {emojis['thumbs_up']}",
    f"Thanks {{firstName}}!",
    f"Thankya {{firstName}}!",
    f"Wow, thanks {{firstName}}!",
    f"TY {{firstName}}!",
]

wait: List[str] = [
    f"One moment please...",
    f"One sec...",
    f"BRB!",
    f"Hold up...",
    f"Lemme get something...",
    f"Just a moment!",
    f"Just a moment...",
]

waitWName: List[str] = [
    f"One moment {{firstName}}...",
    f"One sec {{firstName}}...",
    f"Just a moment {{firstName}}!",
    f"Just a moment {{firstName}}...",
]

yw: List[str] = [
    f"You're welcome!",
    f"Have a great {{timeOfDay}}!",
    f"Anytime!",
    f"Yeah, no problem!",
    f"Safe travels!",
]

ywWName: List[str] = [
    f"You're welcome {{firstName}}!",
    f"Have a great {{timeOfDay}} {{firstName}}!",
    f"Anytime {{firstName}}!",
    f"Yeah, no problem {{firstName}}!",
    f"Safe travels, {{firstName}}!",
]

timeOfDay: dict = {
    'night': f"night",
    'evening': f"evening",
    'afternoon': f"afternoon",
    'morning': f"morning",
    'generic': f"day",
}

unknown: List[str] = [
    f"I'm only fluent in BART.",
    f"I can't really understand much else outside of BART-speak.",
    f"I couldn't quite get that.",
    f"This is awkward.",
    f""
]


reset: List[str] = [
    f"Okay, I'll clear out my data on you in 3... 2... 1. Hey! Come here often? I'm Bartbot, here to help you with all your BART needs."  # noqa: E501
]
