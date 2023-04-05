

TORTOISE_ORM_CONFIG = {
    "connections": {"default": "postgres://dab:qwerasdf@localhost:5432/loanpro"},
    "apps": {
        "models": {
            "data_model.record", "data_model.operation", "data_model.user", "aerich.models"
        },
        "default_connection": "default"
    }
}


AUTH_SEC = "loanprorocks"
AUTH_ALGROR = "HS256"





