from dataclasses import dataclass, fields
from datetime import datetime


@dataclass
class ServiceRequest:
    service_request: str
    address: str
    created: datetime
    last_updated: datetime
    status: str

    def __post_init__(self):
        self.created = datetime.strptime(self.created, "%m/%d/%Y")
        self.last_updated = datetime.strptime(self.last_updated, "%m/%d/%Y")

    def serialize_field(self, field):
        value = getattr(self, field)
        if isinstance(value, datetime):
            return datetime.strftime(value, "%Y-%m-%d")
        return value

    def to_dict(self):
        return {field.name: self.serialize_field(field.name) for field in fields(self)}
