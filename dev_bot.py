from strategy_llm_engine import evaluate_strategy
#!/usr/bin/env python3

import os
import json
import subprocess
import shutil
from datetime import datetime
from pathlib import Path

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    CommandHandler,
    ContextTypes,
    filters,
)

# ==========================

# LLM ENGINE (CLEAN)

# ==========================



def generate_plan(text):

    from llm_engine import ask_llm

    try:

        return ask_llm(text)

    except Exception as e:

        return f"Erro LLM: {e}"



# COMMAND HANDLER
