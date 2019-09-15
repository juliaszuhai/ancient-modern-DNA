import os

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__))))
DATA_PATH = os.path.join(ROOT_DIR, "data//ancient")
TEST_DATA_PATH = os.path.join(DATA_PATH, "test")
IRIS_DATA_PATH = os.path.join(TEST_DATA_PATH, "iris.data.csv")
AUTOENCODER_MODELS_PATH = os.path.join(ROOT_DIR, "models/autoencoder_%s.h5")
