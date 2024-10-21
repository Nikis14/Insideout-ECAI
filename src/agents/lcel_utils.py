from typing import Any, Dict, List
from uuid import UUID

from langchain_core.output_parsers import StrOutputParser
from langchain.callbacks import StdOutCallbackHandler
from langchain.callbacks.base import BaseCallbackHandler
from langchain_core.outputs import LLMResult

from src.logging_utils import get_logger, FeatureLogger

logger = get_logger(__name__, to_file=True)
feature_logger = FeatureLogger()

class LLMTaggerOutputParser(StrOutputParser):
    def parse(self, text: str) -> str:
        tagger_out = text.strip()
        return tagger_out.split("/")


class LLMTaggerOutputParserCallback(StrOutputParser):
    def parse(self, text: str) -> str:
        tagger_out = text.strip()
        logger.info(f"tagger_end: {tagger_out}")
        feature_logger.log_value("tagger_end", tagger_out)
        return tagger_out.split("/")


class LLMCallbackHandler(BaseCallbackHandler):
    def __init__(self) -> None:
        super().__init__()

    def on_llm_end(
        self,
        response: LLMResult,
        *,
        run_id: UUID,
        parent_run_id: UUID | None = None,
        **kwargs: Any,
    ) -> Any:
        text_out = response.generations[0][0].text
        if 'tags' in kwargs.keys() and len(kwargs['tags']) > 1: 
            tags = kwargs['tags']
            feature_logger.log_value(tags[-1], text_out)
        else:
            logger.info(f"llm_end: {text_out}")


class PipeCallbackHandler(BaseCallbackHandler):
    def __init__(self) -> None:
        super().__init__()

    def on_llm_end(
        self,
        response: LLMResult,
        *,
        run_id: UUID,
        parent_run_id: UUID | None = None,
        **kwargs: Any,
    ) -> Any:
        text_out = response.generations[0][0].text
        print(text_out)
        logger.info(f"chain_end: {text_out}")
