"""
JarvisOS Core - Self-Building Operating System
"""

__version__ = "0.2.0"
__author__ = "Abderrahim"

from .observer import Observer
from .analyzer import Analyzer
from .generator import Generator
from .executor import Executor
from .evolution import Gene, GenePool, EvolutionEngine
from .dna import UserDNA

__all__ = [
    "Observer",
    "Analyzer", 
    "Generator",
    "Executor",
    "Gene",
    "GenePool",
    "EvolutionEngine",
    "UserDNA"
]
