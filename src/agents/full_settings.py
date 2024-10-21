import os
import openai
from dotenv import load_dotenv
import json
from tqdm import tqdm
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain.prompts import PromptTemplate

from src.agents.agent import get_simple_agent, get_insideout
from src.datasets.empathetic_dialogs import EmpDialogsDataset
from src.utils import read_files_to_dict, read_file
from src.logging_utils import get_logger
from src.agents.lcel_utils import LLMTaggerOutputParserCallback

logger = get_logger(__name__, to_file=True)
load_dotenv(".env")
assert "OPENAI_API_KEY" in os.environ
openai.api_key = os.environ["OPENAI_API_KEY"]


class BaseSettingAssembler:
    def __init__(self, config_dict_path) -> None:
        with open(config_dict_path, "r") as f:
            config = json.loads(f.read())
        logger.info(f"congig:\n{config}")
        self.insideout_block = self.get_isideout_block(config)
        self.simple_block = self.get_simple_block(config, tags=['simple_agent'])

    def get_isideout_block(self, config):
        emotions_dict = read_files_to_dict(config["insideout"]["emotion_prompts"])
        initial_prompt = read_file(config["insideout"]["prompt_step_one"])
        final_prompt = read_file(config["insideout"]["final_prompt"])
        logger.info(json.dumps(emotions_dict))
        logger.info(initial_prompt)
        logger.info(final_prompt)
        insideout = get_insideout(
            initial_prompt=initial_prompt,
            emotions_dict=emotions_dict,
            final_prompt=final_prompt,
            model_name=config["insideout"]["model_name"],
        )
        return insideout

    def get_simple_block(self, config, tags=[]):
        prompt_template = read_file(config["simple_model"]["prompt_template"])
        logger.info(prompt_template)
        simple_model = get_simple_agent(
            model_name=config["simple_model"]["model_name"],
            evaluation_prompt_template=prompt_template,
            output_parcer=StrOutputParser(),
            tags=tags
        )
        return simple_model

    def assemble(self, insideout_block, simple_block):
        pass


class SettingOneAssembler(BaseSettingAssembler):
    def __init__(self, config_dict_path) -> None:
        super().__init__(config_dict_path)

    def assemble(self):
        # planner  ───> pass through───> simple_block ───>
        #  └───> insideout_block──> lambda ───└
        names = ["tag: ", "confidence: ", "additional information: "]
        # reformat input into str suitable for llm prompt
        aggr_output = RunnableLambda(
            lambda x: "\n".join([name + value for name, value in zip(names, x)])
        )
        planner = {"dialog": RunnablePassthrough()}
        setting_pipe = (
            planner
            | {
                "emotional_state_info": (self.insideout_block | aggr_output),
                "dialog": RunnablePassthrough(),
            }
            | self.simple_block
        )
        return setting_pipe


class SettingTwoAssembler(BaseSettingAssembler):
    def __init__(self, config_dict_path) -> None:
        super().__init__(config_dict_path)

    def assemble(self):
        # planner  ───> pass through──────────> insideout_block ───>
        #  └─> simple_block / tagger ──> lambda ───└

        names = ["tag: ", "confidence: ", "additional information: "]
        # reformat input into str suitable for llm prompt
        aggr_output = RunnableLambda(
            lambda x: "\n".join([name + value for name, value in zip(names, x)])
        )
        planner = {"dialog": RunnablePassthrough()}
        setting_pipe = (
            planner
            | {
                "emotional_state_info": (self.simple_block | aggr_output),
                "dialog": RunnablePassthrough(),
            }
            | self.insideout_block
        )
        return setting_pipe


def assemble_baseline(config_dict_path):
    with open(config_dict_path, "r") as f:
        config = json.loads(f.read())
    logger.info(f"congig:\n{config}")
    prompt_template = read_file(config["output_model"]["prompt_template"])
    logger.info(prompt_template)
    output_model = get_simple_agent(
        model_name=config["output_model"]["model_name"],
        evaluation_prompt_template=prompt_template,
        output_parcer=LLMTaggerOutputParserCallback(),
    )
    return output_model
