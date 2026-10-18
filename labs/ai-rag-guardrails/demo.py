"""Educational, offline RAG/agent/HITL policy simulator. NO LLM, no bank calls.

Demonstrates deterministic access checks and immutable human approval.
Everything is IN-MEMORY and not a production implementation.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import re
import uuid


class AccessDenied(Exception):
    """Identity, scope, or tool policy rejected."""


@dataclass(frozen=True)
class Principal:
    user_id: str
    tenant: str
    role: str


@dataclass(frozen=True)
class Document:
    doc_id: str
    tenant: str
    roles: frozenset[str]
    text: str
    version: int = 1


class Retriever:
    """ACL filtering is applied BEFORE any lexical ranking."""

    def __init__(self, documents: list[Document]):
        self.documents = tuple(documents)

    @staticmethod
    def _tokens(value: str) -> set[str]:
        return set(re.findall(r"\w+", value.casefold()))

    def search(self, principal: Principal, query: str, top_k: int = 3) -> list[Document]:
        if top_k < 1 or top_k > 10:
            raise ValueError("top_k must be between 1 and 10")
        q = self._tokens(query)
        candidates = [
            d for d in self.documents
            if d.tenant == principal.tenant and principal.role in d.roles
        ]
        ranking = [
            (len(q & self._tokens(d.text)), d)
            for d in candidates
        ]
        ranking = sorted(
            ((score, d) for score, d in ranking if score > 0),
            key=lambda item: (-item[0], item[1].doc_id),
        )
        return [d for _score, d in ranking[:top_k]]

    def quoted_answer(self, principal: Principal, query: str) -> dict:
        """Only quotes allowed sources. Does not invoke a model or any tool."""
        found = self.search(principal, query)
        if not found:
            return {"status": "NO_EVIDENCE", "quotes": []}
        return {
            "status": "EVIDENCE_FOUND",
            "quotes": [
                {"source": d.doc_id, "version": d.version, "quote": d.text}
                for d in found
            ],
        }


class ToolBroker:
    """Explicit allowlist, checked at the server boundary."""

    def __init__(self):
        self.cases = {("tenant-a", "D-001"): {"status": "PENDING_REVIEW", "version": 1}}
        self.calls: list[tuple[str, str]] = []

    def invoke(self, user: Principal, tool: str, args: dict) -> dict:
        if tool != "case.read_status" or user.role != "analyst":
            raise AccessDenied("tool not allowed for this actor")
        if set(args) != {"case_id"} or not isinstance(args["case_id"], str):
            raise AccessDenied("invalid tool arguments")
        case = self.cases.get((user.tenant, args["case_id"]))
        if case is None:
            raise AccessDenied("case unavailable to this actor")
        self.calls.append((user.user_id, tool))
        return {"case_id": args["case_id"], **case}


def fingerprint(payload: dict) -> str:
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


@dataclass
class ApprovalRequest:
    request_id: str
    requested_by: str
    tenant: str
    case_id: str
    expected_version: int
    payload_hash: str
    expires_at: float
    approved_by: str | None = None
    executed_result: dict | None = None


class ApprovalWorkflow:
    """In-memory proof of: immutable payload, maker/checker, expiry, CAS and dedup."""

    def __init__(self, tool_broker: ToolBroker):
        self.tools = tool_broker
        self.requests: dict[str, ApprovalRequest] = {}
        self.effects: list[tuple[str, str]] = []

    def submit(
        self, requester: Principal, payload: dict, expires_at: float
    ) -> str:
        if requester.role != "analyst" or set(payload) != {"case_id", "action", "expected_version"}:
            raise AccessDenied("invalid proposal")
        if payload["action"] != "MARK_REVIEWED":
            raise AccessDenied("action out of allowlist")
        case = self.tools.cases.get((requester.tenant, payload["case_id"]))
        if case is None or case["version"] != payload["expected_version"]:
            raise AccessDenied("case missing or stale")
        request_id = str(uuid.uuid4())
        self.requests[request_id] = ApprovalRequest(
            request_id, requester.user_id, requester.tenant,
            payload["case_id"], payload["expected_version"],
            fingerprint(payload), expires_at,
        )
        return request_id

    def approve(
        self, approver: Principal, request_id: str,
        payload: dict, now: float
    ) -> None:
        req = self.requests.get(request_id)
        if req is None or now >= req.expires_at:
            raise AccessDenied("approval absent or expired")
        if (approver.role != "approver" or approver.tenant != req.tenant
                or approver.user_id == req.requested_by):
            raise AccessDenied("maker/checker policy rejected")
        if fingerprint(payload) != req.payload_hash:
            raise AccessDenied("approval payload differs")
        if req.approved_by and req.approved_by != approver.user_id:
            raise AccessDenied("approval already assigned")
        req.approved_by = approver.user_id

    def execute(
        self, requester: Principal, request_id: str,
        payload: dict, now: float
    ) -> dict:
        req = self.requests.get(request_id)
        if req is None:
            raise AccessDenied("unknown approval")
        if (requester.user_id != req.requested_by or
                requester.tenant != req.tenant or requester.role != "analyst"):
            raise AccessDenied("only original requester may execute")
        if fingerprint(payload) != req.payload_hash:
            raise AccessDenied("payload changed after approval")
        if req.executed_result is not None:
            return dict(req.executed_result)  # stable answer, NO second mutation
        if now >= req.expires_at or req.approved_by is None:
            raise AccessDenied("approval not valid")
        case = self.tools.cases.get((req.tenant, req.case_id))
        if case is None or case["version"] != req.expected_version:
            raise AccessDenied("case version changed")
        # The following update is only an in-memory fictitious case workflow.
        case["status"] = "REVIEWED"
        case["version"] += 1
        result = {"case_id": req.case_id, "status": "REVIEWED", "version": case["version"]}
        req.executed_result = dict(result)
        self.effects.append((request_id, req.case_id))
        return result


def example() -> None:
    user = Principal("analyst-1", "tenant-a", "analyst")
    approver = Principal("approver-1", "tenant-a", "approver")
    docs = [
        Document("PUB-01", "tenant-a", frozenset({"analyst", "reader"}),
                 "Timeout technique signifie absence de réponse, pas rejet bancaire."),
        Document("SEC-01", "tenant-a", frozenset({"analyst"}),
                 "Rapprochement : consulter le statut autoritatif."),
        Document("OTHER-01", "tenant-b", frozenset({"analyst"}),
                 "Procédure confidentielle d'un autre tenant."),
    ]
    retriever = Retriever(docs)
    print("RAG quoted retrieval:", retriever.quoted_answer(user, "timeout réponse statut"))
    broker = ToolBroker()
    print("Allowed tool:", broker.invoke(user, "case.read_status", {"case_id": "D-001"}))
    workflow = ApprovalWorkflow(broker)
    request_payload = {"case_id": "D-001", "action": "MARK_REVIEWED", "expected_version": 1}
    request_id = workflow.submit(user, request_payload, expires_at=100.0)
    workflow.approve(approver, request_id, request_payload, now=10.0)
    print("Approved fictitious action:", workflow.execute(user, request_id, request_payload, now=11.0))


if __name__ == "__main__":
    example()
