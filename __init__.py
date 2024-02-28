import os, sys
from dotenv import load_dotenv

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
gdino_path = os.path.join(ROOT_PATH, 'GroundingDINO')
sys.path.append(gdino_path)

load_dotenv(os.path.join(ROOT_PATH, '.env'))
WEIGHTS_NAME = "groundingdino_swint_ogc.pth"
WEIGHTS_PATH = os.path.join(ROOT_PATH, "weights", WEIGHTS_NAME)
CONFIG_PATH = os.path.join(ROOT_PATH, "GroundingDINO/groundingdino/config/GroundingDINO_SwinT_OGC.py")