# compiler: skip
from apmodel.nodeinfo.nodeinfo import (
    Nodeinfo,
)
from apmodel.nodeinfo.nodeinfo import (
    NodeinfoInbound as Inbound,
)
from apmodel.nodeinfo.nodeinfo import (
    NodeinfoOutbound as Outbound,
)
from apmodel.nodeinfo.nodeinfo import (
    NodeinfoProtocol as Protocol,
)
from apmodel.nodeinfo.nodeinfo import (
    NodeinfoServices as Services,
)
from apmodel.nodeinfo.nodeinfo import (
    NodeinfoSoftware as Software,
)
from apmodel.nodeinfo.nodeinfo import (
    NodeinfoUsage as Usage,
)
from apmodel.nodeinfo.nodeinfo import (
    NodeinfoUsageUsers as Users,
)

__all__ = [
    "Nodeinfo",
    "Inbound",
    "Outbound",
    "Protocol",
    "Services",
    "Software",
    "Usage",
    "Users"
]


def from_dict(obj: dict) -> Nodeinfo:
    return Nodeinfo.model_validate(obj)