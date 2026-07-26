"""
Pydantic schemas for Business Rules. model_validator enforces that a
guardrail rule has guardrail_text, and an automation rule has all four
trigger/action fields - a rule that's malformed for its own type would
otherwise silently do nothing when applied.
"""
import uuid
from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, model_validator

TRIGGER_FIELDS = ("intent", "sentiment", "priority")
ACTION_FIELDS = ("lead_status", "priority")


class BusinessRuleRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    rule_type: Literal["guardrail", "automation"]
    is_active: bool
    guardrail_text: Optional[str] = None
    trigger_field: Optional[str] = None
    trigger_value: Optional[str] = None
    action_field: Optional[str] = None
    action_value: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class BusinessRuleCreate(BaseModel):
    name: str
    rule_type: Literal["guardrail", "automation"]
    is_active: bool = True
    guardrail_text: Optional[str] = None
    trigger_field: Optional[Literal["intent", "sentiment", "priority"]] = None
    trigger_value: Optional[str] = None
    action_field: Optional[Literal["lead_status", "priority"]] = None
    action_value: Optional[str] = None

    @model_validator(mode="after")
    def check_fields_for_type(self):
        if self.rule_type == "guardrail" and not self.guardrail_text:
            raise ValueError("guardrail_text is required for a guardrail rule")
        if self.rule_type == "automation" and not all(
            [self.trigger_field, self.trigger_value, self.action_field, self.action_value]
        ):
            raise ValueError("trigger_field, trigger_value, action_field, and action_value are all required for an automation rule")
        return self


class BusinessRuleUpdate(BaseModel):
    name: Optional[str] = None
    is_active: Optional[bool] = None
    guardrail_text: Optional[str] = None
    trigger_field: Optional[Literal["intent", "sentiment", "priority"]] = None
    trigger_value: Optional[str] = None
    action_field: Optional[Literal["lead_status", "priority"]] = None
    action_value: Optional[str] = None
