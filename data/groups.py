import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property
import uuid


class Group(SqlAlchemyBase):
    __tablename__ = 'groups'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    invite_link = sqlalchemy.Column(sqlalchemy.String, unique=True, default=lambda: str(uuid.uuid4()))
    member_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    is_teacher = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    points = sqlalchemy.Column(sqlalchemy.Integer, default=0)

    user = relationship("User", back_populates="groups")

    def __repr__(self):
        return f'<Group> {self.id} {self.name}'

    @hybrid_property
    def link(self):
        return f"/group/join/{self.invite_link}"
