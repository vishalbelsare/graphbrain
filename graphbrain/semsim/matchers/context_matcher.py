import logging

from spacy.language import Language
from spacy.lang.en import English
from spacy_transformers.pipeline_component import Transformer
from thinc.types import Ragged
from torch import Tensor

from graphbrain.hyperedge import Hyperedge
from graphbrain.hypergraph import Hypergraph
from graphbrain.semsim.matchers.matcher import SemSimMatcher, SemSimConfig

logger: logging.Logger = logging.getLogger(__name__)


class ContextEmbeddingMatcher(SemSimMatcher):
    def __init__(self, config: SemSimConfig):
        super().__init__(config)
        self._spacy_trf_pipe: Language = create_spacy_pipeline(config.model_name)

    def filter_oov(self, words: list[str]) -> list[str]:
        pass

    def _similar(
            self,
            candidate: str,
            references: list[str],
            threshold: float = None,
            root_edge: Hyperedge = None,
            hg: Hypergraph = None
    ) -> bool | None:
        # Embedding for reference(s) is missing, needs example sentences

        # Find out to which token in the root edge the candidate refers to




        root_edge_text: str = hg.text(root_edge)
        spacy_doc = self._spacy_trf_pipe(root_edge_text)

        trf_data = spacy_doc._.trf_data


def create_spacy_pipeline(model_name: str) -> Language:
    nlp: Language = English()
    config = {
        "model": {
            "@architectures": "spacy-transformers.TransformerModel.v3",
            "name": model_name,
            "tokenizer_config": {"use_fast": True},
        }
    }
    trf: Transformer = nlp.add_pipe("transformer", config=config)  # noqa
    trf.model.initialize()
    return nlp


# Taken from: https://huggingface.co/intfloat/e5-base
def average_pool(last_hidden_states: Tensor, attention_mask: Tensor) -> Tensor:
    last_hidden = last_hidden_states.masked_fill(~attention_mask[..., None].bool(), 0.0)
    return last_hidden.sum(dim=1) / attention_mask.sum(dim=1)[..., None]


def get_lex2trf_idx(lexical_tokens: list[str], alignment_data: Ragged) -> dict[int, list[int]]:
    """
    Make alignment between lexical tokens and transformer (sentencepiece, wordpiece, ...) tokens.
    :param lexical_tokens:
    :param alignment_data:
    :return:
    """
    lex2trf_idx: dict[int, list[int]] = {}
    trf_idx: int = 0
    for lex_idx in range(len(lexical_tokens)):
        trf_token_length: int = alignment_data.lengths[lex_idx]
        lex2trf_idx[lex_idx] = list(alignment_data.dataXd[trf_idx:trf_idx + trf_token_length])
        trf_idx += trf_token_length
    return lex2trf_idx

# def get_lex2trf_idx(lexical_tokens: list[str], alignment_data: Ragged) -> dict[int, list[int]]:
#     return {lex_idx: get_trf_token_idxes(lex_idx, alignment_data) for lex_idx in range(len(lexical_tokens))}

# def get_trf_token_idxes(lex_idx_: int, alignment_data: Ragged):
#     start_idx: int = int(np.sum(alignment_data.lengths[:lex_idx_]))
#     end_idx: int = start_idx + alignment_data.lengths[lex_idx_]
#     return alignment_data.dataXd[start_idx:end_idx]
