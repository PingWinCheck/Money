from uuid import uuid4, UUID
from datetime import datetime, timezone
from typing import TYPE_CHECKING

from sqlalchemy import func, Enum as PostgresEnum, ForeignKey, UniqueConstraint
# from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import expression
from sqlalchemy.types import DateTime
# from catalog.models import MoneyForUser
from database import Base
from enum import Enum


if TYPE_CHECKING:
    from catalog.models import Money


class User(Base):
    __tablename__ = 'users'

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    username: Mapped[str] = mapped_column(unique=True, index=True)
    email: Mapped[str]
    password_hash: Mapped[str]
    is_active: Mapped[bool] = mapped_column(default=True)
    is_verification_email: Mapped[bool] = mapped_column(default=False, server_default=expression.false())
    created_at: Mapped[datetime] = mapped_column(server_default=func.current_timestamp())
    update_at: Mapped[datetime] = mapped_column(server_default=func.current_timestamp(),
                                                server_onupdate=func.current_timestamp())
    # update_at = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc),
    #                           onupdate=datetime.now(timezone.utc))
    moneys: Mapped[list["Money"]] = relationship('Money', secondary='money_for_users', back_populates='users')
    roles: Mapped[list["Role"]] = relationship('Role', secondary='user_roles_association', back_populates='users')


class Role(Base):
    __tablename__ = 'roles'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, index=True)
    description: Mapped[str | None] = mapped_column(default=None)
    users: Mapped[list["User"]] = relationship('User', secondary='user_roles_association', back_populates='roles')
    permissions: Mapped[list["Permission"]] = relationship('Permission',
                                                           secondary='role_permission_association',
                                                           back_populates='roles')


class Permission(Base):
    __tablename__ = 'permissions'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, index=True)
    description: Mapped[str | None] = mapped_column(default=None)
    roles: Mapped[list["Role"]] = relationship('Role',
                                               secondary='role_permission_association',
                                               back_populates='permissions')


class RolePermissionAssociation(Base):
    __tablename__ = 'role_permission_association'
    __table_args__ = (UniqueConstraint('role_id', 'permission_id',
                                       name='idx_unique_role_permission'),
                      )

    id: Mapped[int] = mapped_column(primary_key=True)
    role_id: Mapped[int] = mapped_column(ForeignKey('roles.id'))
    permission_id: Mapped[int] = mapped_column(ForeignKey('permissions.id'))


class UserRoleAssociation(Base):
    __tablename__ = 'user_roles_association'
    __table_args__ = (UniqueConstraint('role_id', 'user_id',
                                       name='idx_unique_user_role'),
                      )

    id: Mapped[int] = mapped_column(primary_key=True)
    role_id: Mapped[int] = mapped_column(ForeignKey('roles.id'))
    user_id: Mapped[UUID] = mapped_column(ForeignKey('users.id'))

