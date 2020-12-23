import environ


def load_environment():
    env = environ.Env()
    base_dir = environ.Path(__file__) - 2
    env.read_env(base_dir(".env"))
