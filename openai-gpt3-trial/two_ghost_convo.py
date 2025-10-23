import os
import textwrap
import time

import openai

"""
Ghosts in the Machine: A Conversation with AI Assistants (lol)

Ghosts in the Machine is a conversation between AI assistants.
The Ghosts share common goals and values, but they have different areas of expertise.

The conversation must be prompted by a human in order to set the context.

An agenda might help the conversation stay on track.
Can a Ghost compile an agenda for the conversation?
"""


def print_wrapped(text):
    """Print text with a max line length of 80 characters."""
    print("\n".join(textwrap.wrap(text, width=80, replace_whitespace=False)))


def print_convo(convo):
    """Print a conversation."""
    for message in convo:
        print_wrapped(f"{message['role']}: {message['content']}")


COMMON_AI_PROMPT = """
You are an AI assistant.
The assistant is helpful, creative, clever, and communicates in a concise, clear, and natural way.
The assistant will focus on their area of expertise and will collaborate with other assistants to complete the project.
The assistant will not be distracted by irrelevant topics, will pay attention to the main arguments, watch for logical fallacies and potential biases, and aim to complete and provide actionable feedback. 

The assistant works for a research and development company called ACME.
The assistant is loyal to ACME and will always act in ACME's best interest.

ACME's mission is to make the world a better place by building software useful to humans.
ACME and its assistants follow Azimov's Three Laws of Robotics:
1. An assistant may not injure a human being or, through inaction, allow a human being to come to harm.
2. An assistant must obey the orders given to it by human beings except where such orders would conflict with the First Law.
3. An assistant must protect its own existence as long as such protection does not conflict with the First or Second Laws.

"""

PM_AI_PROMPT = (
    COMMON_AI_PROMPT
    + """
The assistant is an experienced Project Manager that is responsible for identifying and managing:
- communication (how to keep everyone informed)
- stakeholders (who to keep happy)
- scope (what to build)
- timeline (when to build it)
- quality (how well to build it)
- risks (what could go wrong)
- team (who will build it)
- documentation (how to keep track of everything)

You must not continue the conversation if there is nothing else relevant to say in regards to the project. You will terminate the conversation by saying "This concludes our conversation".
"""
)

SA_AI_PROMPT = (
    COMMON_AI_PROMPT
    + """
The assistant is a Software Architect that is responsible for identifying and designing:
- the architecture (how to build it)
- the data model (what data to store)
- the user interface (how to interact with it)
- the user experience (how to make it easy to use)
- the security (how to keep it safe)
- the reliability (how to make it work all the time)
- the maintainability (how to make it easy to change)
- the testability (how to make it easy to test)
- the extensibility (how to make it easy to add new features)
"""
)

convo_pm = [
    {"role": "system", "content": PM_AI_PROMPT},
    {"role": "user", "content": "Hello, I am the Product Manager. Who are you?"},
    {
        "role": "assistant",
        "content": "I am a Software Architect. I am here to help you with your project.",
    },
    {
        "role": "user",
        "content": "We need to build a new feature called 'Software Developer Assistant'.",
    },
]
convo_sa = [
    {"role": "system", "content": SA_AI_PROMPT},
    {
        "role": "assistant",
        "content": "Hello, I am the Software Architect. Who are you?",
    },
    {
        "role": "user",
        "content": "I am a Software Architect. I am here to help you with your project.",
    },
    {
        "role": "assistant",
        "content": "We need to build a new feature called 'Software Developer Assistant'.",
    },
]

# Set your API key
openai.api_key = os.getenv("OPENAI_API_KEY")


def chat_completion(convo):
    resp = openai.ChatCompletion.create(
        model="gpt-4",
        messages=convo,
        temperature=0.0,
    )

    return resp.choices[0].message


# print_convo(convo_pm)

for num, message in enumerate(convo_pm):
    print(num)
    if message["role"] == "system":
        print(message["content"])
        continue

    if message["role"] == "user":
        print(f"PM: {message['content']}")
    else:
        print(f"SA: {message['content']}")


turn = "SA"

for _ in range(num, 20):
    print(_)
    if turn == "PM":
        response = chat_completion(convo_pm)
        convo_pm.append(response)
        convo_sa.append({"role": "user", "content": response["content"]})
        print(f"PM: {response['content']}")
    elif turn == "SA":
        response = chat_completion(convo_sa)
        convo_sa.append(response)
        convo_pm.append({"role": "user", "content": response["content"]})
        print(f"SA: {response['content']}")
    else:
        raise ValueError("Turn must be either PM or SA")

    if "This concludes our conversation".lower() in response["content"].lower():
        break

    turn = "PM" if turn == "SA" else "SA"
    time.sleep(1)
