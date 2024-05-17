# -*- coding: utf-8 -*-
""" Import all agent related modules in the package. """
from .text_agents import QwenAgent,KimiAgent,DeepSeekAgent,ClaudeAgent,ChatGPTAgent,AgentConfig,BaiChuanAgent,PhiAgent,LlamaAgent,MixtralAgent
from .text2image_agents import WanxAgent
from .Audio_Agents import QwenAudioAgent,SambertAgent
from .images2text_agents import ImageAnalyzer

__all__ = [
    "QwenAgent",
    "KimiAgent",
    "DeepSeekAgent",
    "ClaudeAgent",
    "ChatGPTAgent",
    "AgentConfig",
    "BaiChuanAgent",
    "PhiAgent",
    "LlamaAgent",
    "MixtralAgent",
    "WanxAgent",
    "QwenAudioAgent",
    "SambertAgent",
    "ImageAnalyzer",
]