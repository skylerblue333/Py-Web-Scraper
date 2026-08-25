import ipaddress
import os
import socket
import threading
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
plans_lock = threading.Lock()


def _canonical_public_https_url(raw_url: str) -> tuple[str, str]:
    parsed = urlsplit(raw_url.strip())
    if parsed.scheme.lower() != "https":
        raise ValueError("only https URLs are accepted")
    if not parsed.hostname or parsed.username or parsed.password:
        raise ValueError("URL must contain a hostname and no embedded credentials")
    try:
        port = parsed.port
    except ValueError as error:
        raise ValueError("URL port is invalid") from error

    host = parsed.hostname.rstrip(".").lower()
    if not host:
        raise ValueError("URL hostname cannot be empty")
    try:
        address = ipaddress.ip_address(host)
    except ValueError:
        address = None
        try:
            socket.inet_aton(host)
        except OSError:
            pass
        else:
            raise ValueError("non-canonical numeric IPv4 hosts are not accepted")
    if address is not None and not address.is_global:
        raise ValueError("private, loopback, link-local, and reserved IPs are not accepted")
    if host == "localhost" or host.endswith(".localhost"):
        raise ValueError("localhost is not accepted")
    if ALLOW_HOSTS and host not in ALLOW_HOSTS:
        raise ValueError("host is not in SKY_FETCH_ALLOW_HOSTS")

    host_for_netloc = f"[{host}]" if ":" in host else host
    netloc = f"{host_for_netloc}:{port}" if port is not None else host_for_netloc
    canonical = urlunsplit(("https", netloc, parsed.path or "/", parsed.query, ""))
    return canonical, host


@app.get("/healthz")
def healthz() -> dict[str, str]:
    return {"status": "ok", "service": "sky-fetch-planner"}


@app.get("/readyz")
def readyz() -> dict[str, object]:
    with plans_lock:
        planned = len(plans)
    return {"status": "ready", "capacity": MAX_JOBS, "planned": planned}


@app.post("/v1/plans", response_model=FetchPlan, status_code=201)
def create_plan(request: FetchPlanRequest) -> FetchPlan:
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
    with plans_lock:
        if len(plans) >= MAX_JOBS:
            raise HTTPException(status_code=503, detail="in-memory plan capacity reached")
        plans[plan.id] = plan
    return plan


@app.get("/v1/plans/{plan_id}", response_model=FetchPlan)
def get_plan(plan_id: str) -> FetchPlan:
    with plans_lock:
        plan = plans.get(plan_id)
    if plan is None:
        raise HTTPException(status_code=404, detail="plan not found")
    return plan
