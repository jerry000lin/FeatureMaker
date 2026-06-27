
from datetime import datetime
import enum

from sqlalchemy import Integer, BigInteger, DateTime, Enum, String, Text, func
from sqlalchemy.orm import Mapped, foreign, mapped_column, relationship
from featuremaker.models.mixins import AuditMixin
from featuremaker.db import Base
from sqlalchemy.dialects.postgresql import JSONB

class WorkflowRunStatus(enum.Enum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "succeeded"
    FAILED = "failed"

class WorkflowNodeExecutionStatus(enum.Enum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "succeeded"
    FAILED = "failed"


class Workflow(AuditMixin, Base):
    __tablename__ = "workflows"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    graph_json: Mapped[dict] = mapped_column(JSONB, nullable=False)

    workflow_runs: Mapped[list["WorkflowRun"]] = relationship(
        "WorkflowRun",
        primaryjoin=lambda: Workflow.id == foreign(WorkflowRun.workflow_id),
        back_populates="workflow"
    )
    

class WorkflowRun(AuditMixin, Base):
    __tablename__ = "workflow_runs"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    workflow_id: Mapped[int] = mapped_column(BigInteger)
    graph_snapshot_json: Mapped[dict] = mapped_column(JSONB, nullable=False)
    status: Mapped[WorkflowRunStatus] = mapped_column(Enum(WorkflowRunStatus))
    error_message: Mapped[str | None] = mapped_column(Text)
    started_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    finished_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    workflow: Mapped["Workflow"] = relationship(
        "Workflow",
        primaryjoin=lambda: Workflow.id == foreign(WorkflowRun.workflow_id),
        back_populates="workflow_runs"
    )
    workflow_node_executions: Mapped[list["WorkflowNodeExecution"]] = relationship(
        "WorkflowNodeExecution",
        primaryjoin=lambda: WorkflowRun.id == foreign(WorkflowNodeExecution.workflow_run_id),
        back_populates="workflow_run"
    )

class WorkflowNodeExecution(AuditMixin, Base):
    __tablename__ = "workflow_node_executions"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    workflow_run_id: Mapped[int] = mapped_column(BigInteger)
    node_id: Mapped[str] = mapped_column(String(255))
    node_type: Mapped[str] = mapped_column(String(255))
    title: Mapped[str] = mapped_column(String(255))
    status: Mapped[WorkflowNodeExecutionStatus] = mapped_column(Enum(WorkflowNodeExecutionStatus))
    elapsed_ms: Mapped[int | None] = mapped_column(Integer)
    error_message: Mapped[str | None] = mapped_column(Text)
    inputs_json: Mapped[dict | None] = mapped_column(JSONB)
    outputs_json: Mapped[dict | None] = mapped_column(JSONB)
    metadata_json: Mapped[dict | None] = mapped_column(JSONB)
    started_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    finished_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    workflow_run: Mapped["WorkflowRun"] = relationship(
        "WorkflowRun",
        primaryjoin=lambda: WorkflowRun.id == foreign(WorkflowNodeExecution.workflow_run_id),
        back_populates="workflow_node_executions"   
    )
