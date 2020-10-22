from app.db_service import user_service
from app.core.config import settings
from app.models_params.user_model_param import UserCreateModelParam
from app.models import model_table_register  # noqa: F401

# make sure all SQL Alchemy models are imported (app.db.base) before initializing DB
# otherwise, SQL Alchemy might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28


def init_db_data():
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next line
    # Base.metadata.create_all(bind=engine)

    user = user_service.user.get_by_logon_name(logon_name=settings.FIRST_SUPERUSER)
    if not user:
        user_in = UserCreateModelParam
        user_in.email = settings.FIRST_SUPERUSER_EMAIL
        user_in.password = settings.FIRST_SUPERUSER_PASSWORD
        user_in.full_name = settings.FIRST_SUPERUSER
        user_in.is_superuser = True

        user = user_service.user.create(obj_in=user_in)  # noqa: F841
