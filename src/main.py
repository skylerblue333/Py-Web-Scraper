import ipaddress
import os
from collections import OrderedDict
from urllib.parse import urlsplit, urlunsplit
from uuid import uuid4

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator

app = FastAPI(title="Sky Fetch Planner", version="0.1.0")

MAX_JOBS = 100
MAX_SELECTOR_CHARS = 256
ALLOW_HOSTS = {
    host.strip().lower()
    for host in os.getenv("SKY_FETCH_ALLOW_HOSTS", "").split(",")
    if host.strip()
}


class FetchPlanRequest(BaseModel):
    url: str = Field(min_length=1, max_length=2048)
    selector: str = Field(min_length=1, max_length=MAX_SELECTOR_CHARS)

    @field_validator("selector")
    @classmethod
    def selector_not_blank(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("selector cannot be blank")
        return value


class FetchPlan(BaseModel):
    id: str
    url: str
    selector: str
    host: str
    status: str = "planned"


plans: OrderedDict[str, FetchPlan] = OrderedDict()


def _canonical_public_https_url(raw_url: str) -> tuple[str, str]:
    parsed = urlsplit(raw_url.strip())
    if parsed.scheme.lower() != "https":
        raise ValueError("only https URLs are accepted")
    if not parsed.hostname or parsed.username or parsed.password:
        raise ValueError("URL must contain a hostname and no embedded credentials")
    host = parsed.hostname.rstrip(".").lower()
    if not host:
        raise ValueError("URL hostname cannot be empty")
    try:
        address = ipaddress.ip_address(host)
    except ValueError:
        address = None
    if address is not None and not address.is_global:
        raise ValueError("private, loopback, link-local, and reserved IPs are not accepted")
    if host == "localhost" or host.endswith(".localhost"):
        raise ValueError("localhost is not accepted")
    if ALLOW_HOSTS and host not in ALLOW_HOSTS:
        raise ValueError("host is not in SKY_FETCH_ALLOW_HOSTS")
    canonical = urlunsplit(("https", parsed.netloc.lower(), parsed.path or "/", parsed.query, ""))
    return canonical, host


@app.get("/healthz")
def healthz() -> dict[str, str]:
    return {"status": "ok", "service": "sky-fetch-planner"}


@app.get("/readyz")
def readyz() -> dict[str, object]:
    return {"status": "ready", "capacity": MAX_JOBS, "planned": len(plans)}


@app.post("/v1/plans", response_model=FetchPlan, status_code=201)
def create_plan(request: FetchPlanRequest) -> FetchPlan:
    if len(plans) >= MAX_JOBS:
        raise HTTPException(status_code=503, detail="in-memory plan capacity reached")
    try:
        url, host = _canonical_public_https_url(request.url)
    except ValueError as error:
        raise HTTPException(status_code=422, detail=str(error)) from error
    plan = FetchPlan(
        id=str(uuid4()),
        url=url,
        selector=request.selector,
        host=host,
    )
    plans[plan.id] = plan
    return plan


@app.get("/v1/plans/{plan_id}", response_model=FetchPlan)
def get_plan(plan_id: str) -> FetchPlan:
    plan = plans.get(plan_id)
    if plan is None:
        raise HTTPException(status_code=404, detail="plan not found")
    return plan
