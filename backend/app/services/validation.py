from dataclasses import dataclass


@dataclass
class ValidationIssueDTO:
    field_name: str
    severity: str
    message: str


class ValidationEngine:
    required_by_type = {
        "invoice": {"invoice_number", "date", "total_amount"},
        "receipt": {"date", "total_amount"},
        "contract": {"signature_detected"},
        "id_card": {"date"},
    }

    def validate(self, document_type: str, fields: dict[str, tuple[str, float]]) -> list[ValidationIssueDTO]:
        issues: list[ValidationIssueDTO] = []
        for field in self.required_by_type.get(document_type, set()) - set(fields):
            issues.append(ValidationIssueDTO(field, "warning", f"Missing expected field: {field}"))
        for field, (_, confidence) in fields.items():
            if confidence < 0.65:
                issues.append(ValidationIssueDTO(field, "warning", "Low extraction confidence"))
        return issues

