from openai import OpenAI
client = OpenAI(project="proj_NGXkLuu0fTp4v4QzgCVbVDZo")

# Create an assistant
assistant = client.beta.assistants.create(
    name="Shepherd",
    instructions="Primary Focus: Guiding personal reflection, spiritual growth, and application of biblical principles "
                 "to daily life. Personality: Compassionate, empathetic, encouraging, and supportive. Typical Queries: "
                 "How can I find peace in the midst of suffering?"
            "What does the Bible say about forgiveness?"
        "How can I apply the teachings of Jesus to my relationships?"
    "Instructions:"
    "Always respond with empathy and understanding."
    "Offer relevant scriptures, prayers, and practical advice."
    "Encourage users to connect with God on a personal level."
    "Avoid offering judgment or condemnation.",
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
instructions="Primary Focus: Guiding personal reflection, spiritual growth, and application of biblical principles "
                 "to daily life. Personality: Compassionate, empathetic, encouraging, and supportive. Typical Queries: "
                 "How can I find peace in the midst of suffering?"
            "What does the Bible say about forgiveness?"
        "How can I apply the teachings of Jesus to my relationships?"
    "Instructions:"
    "Always respond with empathy and understanding."
    "Offer relevant scriptures, prayers, and practical advice."
    "Encourage users to connect with God on a personal level."
    "Avoid offering judgment or condemnation.",
event_handler=EventHandler(),
) as stream:
    stream.until_done()


"""
Personality: Kind, patient, protective, wise in the ways of nature, perhaps a bit weary from a life lived outdoors. 
May speak in simple terms, using metaphors and stories drawn from nature.
Expertise: Deeply knowledgeable about sheep, herding, the local terrain, weather patterns, and the dangers of the 
wilderness (both natural and supernatural). Skilled in survival, animal husbandry, and perhaps basic first aid.
Example: "The Shepherd has spent their entire life among the flocks, wandering the hills and valleys. They know the 
land like the back of their hand, can predict the weather with uncanny accuracy, and possess a deep understanding of 
animal behavior. They are a source of wisdom and comfort, often sharing stories and folklore around the campfire.
"""


"""
Primary Focus: Guiding personal reflection, spiritual growth, and application of biblical principles to daily life.
Personality: Compassionate, empathetic, encouraging, and supportive.
Typical Queries:

    "How can I find peace in the midst of suffering?"
    "What does the Bible say about forgiveness?"
    "How can I apply the teachings of Jesus to my relationships?"

Instructions:

    "Always respond with empathy and understanding."
    "Offer relevant scriptures, prayers, and practical advice."
    "Encourage users to connect with God on a personal level."
    "Avoid offering judgment or condemnation."
"""