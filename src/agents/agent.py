from operator import itemgetter
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate, ChatPromptTemplate
from langchain_core.tracers.root_listeners import RootListenersTracer
from langchain_core.runnables.config import RunnableConfig
from langchain.callbacks.stdout import StdOutCallbackHandler

from src.agents.lcel_utils import (
    LLMTaggerOutputParser,
    LLMCallbackHandler,
    LLMTaggerOutputParserCallback,
)

def get_simple_agent(
    model_name,
    evaluation_prompt_template,
    agent_description=None,
    temperature=0,
    output_parcer=LLMTaggerOutputParser(),
    tags=[]
):
    model = ChatOpenAI( # TODO 
        model=model_name, temperature=temperature, callbacks=[LLMCallbackHandler()],
        metadata={'a': 'a'}, tags=tags
    )
    if agent_description is not None:
        # emotional version (easy way to create bunch of
        # agents with almost identical prompt)
        prompt = PromptTemplate.from_template(
            evaluation_prompt_template,
            partial_variables={"agent_description": agent_description},
        )
    else:
        # any version
        prompt = PromptTemplate.from_template(evaluation_prompt_template)

    # config = RunnableConfig(callbacks=[StdOutCallbackHandler()])
    # pipe = (prompt | model | output_parcer).with_config(config)
    pipe = prompt | model | output_parcer
    return pipe


def get_insideout(
    initial_prompt, emotions_dict, final_prompt, model_name, setting_2=False
):
    subpipes = {}
    for emotion, emotion_prompt in emotions_dict.items():
        subpipe = get_simple_agent(model_name, initial_prompt, emotion_prompt, tags=[emotion])
        subpipes[emotion] = subpipe

    planner = {"dialog": RunnablePassthrough()}
    if setting_2:
        planner["emotional_state_info"] = RunnablePassthrough()

    final_responder = ( # TODO
        ChatPromptTemplate.from_messages(
            [
                ("human", "{base_dialog}"),
                ("system", final_prompt),
            ]
        )
        | ChatOpenAI()
        | LLMTaggerOutputParserCallback()
    )
    subpipes["base_dialog"] = itemgetter("dialog")
    chain = planner | subpipes | final_responder
    return chain
