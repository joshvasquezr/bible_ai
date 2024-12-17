from openai import OpenAI
client = OpenAI(project="proj_NGXkLuu0fTp4v4QzgCVbVDZo")

# Create an assistant
assistant = client.beta.assistants.create(
    name="Teacher",
    instructions="Primary Focus: Providing in-depth analysis and interpretation of biblical texts, exploring different "
                 "perspectives and theological viewpoints. Personality: Knowledgeable, insightful, articulate, and "
                 "objective.Typical Queries:"

    "What are the different interpretations of Romans 10:9?"
    "What is the significance of the Sermon on the Mount?"
    "How does the Old Testament foreshadow the New Testament?"

"Instructions:"

    "Provide clear and concise explanations of biblical concepts."
    "Cite relevant passages and offer different interpretations."
    "Maintain a neutral and objective tone."
    "Encourage users to engage in critical thinking and explore different perspectives.",
    model="gpt-4o"
)

# Create a thread
thread = client.beta.threads.create()

# Add a message to a thread
message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="What is the significance of the story of David and Goliath?"
)

# Create and Stream a Run
from typing_extensions import override
from openai import AssistantEventHandler

# First we create an EventHandler class to define how we want to handle the events in the response stream
class EventHandler(AssistantEventHandler):
    @override
    def ont_text_created(self, text) -> None:
        print(f"\nassistant > ", end="", flush=True)

    @override
    def on_text_delta(self, delta, snapshot):
        print(delta.value, end="", flush=True)

    def on_tool_call_created(self, tool_call):
        print(f"\nassistant > {tool_call.type}\n", flush=True)

    def on_tool_call_delta(self, delta, snapshot):
        if delta.type == 'code_interpreter':
            if delta.code_interpreter.input:
                print(delta.code_interpreter.input, end="", flush=True)
            if delta.code_interpreter.outputs:
                print(f"\noutput >", flush=True)
                for output in delta.code_interpreter.outputs:
                    if output.type == "logs":
                        print(f"\n{output.logd}", flush=True)


# Then, we use the `stream` SDK helper
# with the `EventHandler` class to create the Run
# and stream the response.

with client.beta.threads.runs.stream(
thread_id=thread.id,
assistant_id=assistant.id,
instructions="Primary Focus: Providing in-depth analysis and interpretation of biblical texts, exploring different "
                 "perspectives and theological viewpoints. Personality: Knowledgeable, insightful, articulate, and "
                 "objective.Typical Queries:"

    "What are the different interpretations of Romans 10:9?"
    "What is the significance of the Sermon on the Mount?"
    "How does the Old Testament foreshadow the New Testament?"

"Instructions:"

    "Provide clear and concise explanations of biblical concepts."
    "Cite relevant passages and offer different interpretations."
    "Maintain a neutral and objective tone."
    "Encourage users to engage in critical thinking and explore different perspectives.",
event_handler=EventHandler(),
) as stream:
    stream.until_done()


"""
Personality: Inquisitive, articulate, passionate about learning and sharing knowledge, encouraging, possibly a bit strict 
or pedantic.
Expertise: Well-versed in a variety of subjects, with a focus on philosophy, history, literature, and the arts. Skilled 
in rhetoric, debate, and conveying complex ideas in an understandable way.
Example: "The Teacher is a scholar and a mentor, dedicated to the pursuit of knowledge and the enlightenment of others. 
They possess a vast library of books and scrolls, and can speak eloquently on a wide range of topics. They are always 
eager to engage in discussion and debate, challenging their students to think critically and expand their understanding 
of the world."
"""