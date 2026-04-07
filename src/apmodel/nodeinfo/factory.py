from typing import Literal

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


class NodeinfoFactory:
    def __init__(self, version: Literal["2.1", "2.0"] = "2.1") -> None:
        self.version: Literal["2.1", "2.0"] = version

        self.__protocols = None
        self.__open_registrations = None
        self.__metadata = {}

        # nodeinfo.software
        self.__software_name = None
        self.__software_version = None
        self.__software_repository = None
        self.__software_homepage = None

        # nodeinfo.services
        self.__services_inbound: list[Inbound] | None = None
        self.__services_outbound: list[Outbound] | None = None

        # nodeinfo.usage
        self.__usage_users_total = None
        self.__usage_local_comments = None
        self.__usage_local_posts = None
        self.__usage_active_halfyear = None
        self.__usage_active_month = None

    def set_software(
        self,
        name: str,
        version: str,
        repository: str | None,
        homepage: str | None,
    ) -> "NodeinfoFactory":
        self.__software_name = name
        self.__software_version = version
        self.__software_repository = repository
        self.__software_homepage = homepage
        return self

    def set_protocols(self, protocols: list[str | Protocol]) -> "NodeinfoFactory":
        self.__protocols = protocols
        return self

    def set_services(
        self,
        inbound: list[Inbound],
        outbound: list[Outbound],
    ) -> "NodeinfoFactory":
        self.__services_inbound = inbound
        self.__services_outbound = outbound
        return self

    def set_usage(
        self,
        users_total: int,
        local_comments: int | None = None,
        local_posts: int | None = None,
        active_halfyear: int | None = None,
        active_month: int | None = None,
    ) -> "NodeinfoFactory":
        self.__usage_users_total = users_total
        self.__usage_local_comments = local_comments
        self.__usage_local_posts = local_posts
        self.__usage_active_halfyear = active_halfyear
        self.__usage_active_month = active_month
        return self

    def set_open_registrations(self, *, status: bool) -> "NodeinfoFactory":
        self.__open_registrations = status
        return self

    def set_metadata(self, metadata: dict) -> "NodeinfoFactory":
        self.__metadata = metadata
        return self

    def build(self) -> Nodeinfo:
        if not self.__software_name or not self.__software_version:
            raise ValueError("Software name and version are mandatory fields for Nodeinfo.")

        if not self.__protocols:
            raise ValueError("Protocols list cannot be empty.")

        if self.__services_inbound is None or self.__services_outbound is None:
            raise ValueError("Both inbound and outbound services lists must be set.")

        if self.__usage_users_total is None:
            raise ValueError("Total number of users ('usage.users.total') must be set.")

        if self.__open_registrations is None:
            raise ValueError("'openRegistrations' must be set.")

        if self.version == "2.0" and (self.__software_homepage or self.__software_repository):
                raise ValueError("Software homepage and repository fields are not defined in Nodeinfo version 2.0 by this implementation.")

        return Nodeinfo(
            version=self.version,
            software=Software(
                name=self.__software_name,
                version=self.__software_version,
                homepage=self.__software_homepage,
                repository=self.__software_repository,
            ),
            protocols=self.__protocols,
            services=Services(
                inbound=self.__services_inbound,
                outbound=self.__services_outbound,
            ),
            open_registrations=self.__open_registrations,
            usage=Usage(
                users=Users(
                    total=self.__usage_users_total,
                    active_half_year=self.__usage_active_halfyear,
                    active_month=self.__usage_active_month,
                ),
                local_comments=self.__usage_local_comments,
                local_posts=self.__usage_local_posts,
            ),
            metadata=self.__metadata,
        )
