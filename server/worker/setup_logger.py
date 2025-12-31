import logging
import sys
import sanic

def setup_logger(app_name: str, log_level: int = logging.INFO) -> None:
    app = sanic.Sanic.get_app(app_name)

    logger = logging.getLogger(app_name)
    logger.setLevel(log_level)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(log_level)

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)

    logger.addHandler(handler)

    app.ctx.logger = logger