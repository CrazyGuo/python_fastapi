
# Import all the models, so that Base has them before being imported by Alembic
from app.db.base_class import Base
import app.models.user 
import app.models.iis_log
