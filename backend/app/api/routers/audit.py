from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import require_role
from app.db.session import get_db
from app.models import AuditLog

router = APIRouter(prefix="/audit-logs", tags=["audit"])


@router.get("")
def list_audit_logs(db: Session = Depends(get_db), _=Depends(require_role("admin"))):
    logs = db.query(AuditLog).order_by(AuditLog.created_at.desc()).limit(100).all()
    return [{"actor": log.actor, "action": log.action, "entity_type": log.entity_type, "entity_id": log.entity_id, "created_at": log.created_at} for log in logs]

