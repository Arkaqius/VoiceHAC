from abc import abstractmethod
from .common.HAS_request import HAS_request
from HomeAssistantAPI.homeassistant_api import Client
from .common.HAS_common import HAS_result
from ..NLP_skill import NLPSkill
from typing import Tuple, TYPE_CHECKING
import inspect, sys
from NLP.NER.VH_NER import VH_NER
import hashlib

if TYPE_CHECKING:
    from VHOrchestator import VHOrchestator


class HAS_Base(NLPSkill):
    def __init__(self):
        self.latest_utterance_data = {"utterance_hash": None, "request": None}
        self.child_skills_dict = {}

    def init_own_childs(self):
        self.child_skills_dict = {
            skill.__name__: skill() for skill in HAS_Base.__subclasses__()
        }  # All child classes instances that inherit from HAS_Base

    def request_handling_score(self, ner_result: NER_result, utterance: str) -> Tuple:
        handler, best_score = self._find_handler(ner_result)
        if handler is not None:
            utterance_hash = hashlib.sha256(utterance.encode()).hexdigest()
            self.latest_utterance_data = {
                "utterance_hash": utterance_hash,
                "request": req,
            }
            return (handler, best_score)
        return 0

    def _find_handler(self, ner_result: NER_result):
        score_dict: dict = {}
        for subclass_inst in self.child_skills_dict.values():
            score = subclass_inst.get_req_score(ner_result)
            score_dict[subclass_inst] = score
        max_score_subclass = max(score_dict, key=score_dict.get)
        max_score = score_dict[max_score_subclass]
        if max_score == 0:
            return None, 0
        else:
            return max_score_subclass, max_score

    def get_req_score(self, ner_result: NER_result):
        return 0

    @staticmethod
    def get_subclasses():
        subclasses = []
        for name, obj in inspect.getmembers(sys.modules[__name__]):
            if inspect.isclass(obj) and issubclass(obj, HAS_Base) and obj != HAS_Base:
                subclasses.append(obj)
        return subclasses

    def handle_utterance(
        self, orchst: "VHOrchestator", ner_result: NER_result, utterance: str
    ) -> HAS_result:
        pass
