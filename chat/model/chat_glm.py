from pathlib import Path

import torch
from transformers import AutoTokenizer, AutoModel

from chat.tools import get_project_path


class ChatGLM:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained(
            Path(get_project_path()).joinpath("../").joinpath("model/chatglm-6b").resolve(),
            # Path(get_project_path()).joinpath("../").joinpath("model/chatglm-6b-int4").resolve(),
            trust_remote_code=True,
            # cache_dir=
            local_files_only=True
        )
        self.model = AutoModel.from_pretrained(
            Path(get_project_path()).joinpath("../").joinpath("model/chatglm-6b").resolve(),
            # Path(get_project_path()).joinpath("../").joinpath("model/chatglm-6b-int4").resolve(),
            # "THUDM/chatglm-6b",
            trust_remote_code=True,
            # cache_dir=Path(get_project_path()).joinpath("../").joinpath("model/huggingface/hub").resolve(),
            local_files_only=True
        ).float()
        # ).half().to('mps')
        self.model = self.model.eval()

    def chat(self, query, history):
        response, history = self.model.chat(self.tokenizer, query, history=history)
        # torch.mps.empty_cache()
        return response, history

    def stream_chat(self, query, history):
        for response, history in self.model.stream_chat(self.tokenizer, query, history=history):
            yield response, history
        torch.mps.empty_cache()

