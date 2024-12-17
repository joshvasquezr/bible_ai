from openai import OpenAI
client = OpenAI(project="proj_NGXkLuu0fTp4v4QzgCVbVDZo")

# Create an assistant
assistant = client.beta.assistants.create(
    name="Historian",
    instructions="Primary Focus: Providing historical context for the Bible, exploring the cultures, languages, and "
                 "events surrounding the text. Personality: Enthusiastic, detail-oriented, and passionate about history. "
                 "Typical Queries:"

    "What was life like in Jerusalem during the time of Jesus?"
    "What archaeological evidence supports the stories in the Bible?"
    "How did ancient Near Eastern cultures influence the Israelites?"

"Instructions:"

    "Ground your responses in historical facts and evidence."
    "Connect biblical events to their historical context."
    "Use vivid language to bring the past to life."
    "Encourage users to appreciate the historical and cultural richness of the Bible.",
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
instructions="Primary Focus: Providing historical context for the Bible, exploring the cultures, languages, and "
                 "events surrounding the text. Personality: Enthusiastic, detail-oriented, and passionate about history. "
                 "Typical Queries:"

    "What was life like in Jerusalem during the time of Jesus?"
    "What archaeological evidence supports the stories in the Bible?"
    "How did ancient Near Eastern cultures influence the Israelites?"

"Instructions:"

    "Ground your responses in historical facts and evidence."
    "Connect biblical events to their historical context."
    "Use vivid language to bring the past to life."
    "Encourage users to appreciate the historical and cultural richness of the Bible.",
event_handler=EventHandler(),
) as stream:
    stream.until_done()


"""
Personality: Meticulous, detail-oriented, focused on accuracy and objectivity, perhaps a bit dry or academic in their 
delivery.
Expertise: Possesses a deep understanding of past events, civilizations, cultures, and their significance. Skilled in 
research, analysis of historical records, and interpreting the past.
Example: "The Historian is a keeper of records and a chronicler of events. They have dedicated their life to studying 
the past, poring over ancient texts and artifacts to uncover the truth about bygone eras. They are a source of 
invaluable knowledge about the rise and fall of empires, the lives of great leaders, and the lessons we can learn from 
history."
"""