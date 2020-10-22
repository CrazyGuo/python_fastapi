from typing import Any, Dict, Optional, Union

from sqlalchemy.orm import Session

from app.core.security import get_password_hash, verify_password
from app.db_service.base_db_service import BaseDbService
from app.models.user import AppUsers
from app.models_params.user_model_param import UserCreateModelParam, UserUpdateModelParam


class UserService(BaseDbService[AppUsers, UserCreateModelParam, UserUpdateModelParam]):
    def get_by_logon_name(self, *, logon_name: str):
        return self.db.query(AppUsers).filter(AppUsers.full_name == logon_name).first()

    def create(self, *, obj_in: UserCreateModelParam):
        db_obj = AppUsers(
            email=obj_in.email,
            hashed_password=get_password_hash(obj_in.password),
            full_name=obj_in.full_name,
            is_superuser=obj_in.is_superuser,
        )
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def update(self, *, db_obj: AppUsers, obj_in: Union[UserUpdateModelParam, Dict[str, Any]]):
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        if update_data.get("password", None):
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password
        return super().update(db_obj=db_obj, obj_in=update_data)

    def authenticate(self, *, logon_name: str, password: str):
        user = self.get_by_logon_name(logon_name=logon_name)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def is_available(self, user: AppUsers):
        return user.is_available

    def is_superuser(self, user: AppUsers):
        return user.is_superuser

user = UserService(AppUsers)
