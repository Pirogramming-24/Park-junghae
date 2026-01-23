import os
from functools import lru_cache

import torch
from transformers import pipeline


# (선택) 모델 캐시 위치를 프로젝트 내로 고정하고 싶으면 사용
# os.environ.setdefault("HF_HOME", os.path.join(os.getcwd(), ".hf_cache"))


def _device():
    # GPU 있으면 0, 없으면 -1
    return 0 if torch.cuda.is_available() else -1


@lru_cache(maxsize=1)
def get_summarizer():
    return pipeline(
        "summarization",
        model="google/pegasus-xsum",
        device=_device(),
    )


@lru_cache(maxsize=1)
def get_sentiment():
    return pipeline(
        "sentiment-analysis",
        model="distilbert-base-uncased-finetuned-sst-2-english",
        device=_device(),
    )


@lru_cache(maxsize=1)
def get_generator():
    # gpt2 금지 대체: OPT-125m (가볍고 접근 제한 적음)
    return pipeline(
        "text-generation",
        model="facebook/opt-125m",
        device=_device(),
    )


@lru_cache(maxsize=1)
def get_translator():
    # nllb 금지 대체: opus-mt-en-ko (로컬에서 잘 동작)
    return pipeline(
        "translation",
        model="Helsinki-NLP/opus-mt-en-ko",
        device=_device(),
    )


def run_summarize(text: str) -> str:
    text = (text or "").strip()
    if not text:
        return ""
    summarizer = get_summarizer()
    out = summarizer(text, max_length=60, min_length=20, do_sample=False)
    return out[0]["summary_text"]


def run_sentiment(text: str) -> str:
    text = (text or "").strip()
    if not text:
        return ""
    clf = get_sentiment()
    out = clf(text)[0]
    return f'{out["label"]} ({out["score"]:.2f})'


def run_generate(prompt: str) -> str:
    prompt = (prompt or "").strip()
    if not prompt:
        return ""
    gen = get_generator()
    out = gen(
        prompt,
        max_new_tokens=120,
        do_sample=True,
        temperature=0.8,
        top_p=0.9,
        repetition_penalty=1.1,
        no_repeat_ngram_size=3,
    )
    return out[0]["generated_text"]


def run_translate_en_to_ko(text: str) -> str:
    text = (text or "").strip()
    if not text:
        return ""

    gen = get_generator()  # t5-small을 generator로 사용
    prompt = f"translate English to Korean: {text}"

    out = gen(
        prompt,
        max_new_tokens=200,
        do_sample=False,
    )
    return out[0]["generated_text"]
