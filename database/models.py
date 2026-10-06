"""
VASTU ONE - Database Models (Part 1: Core)
===========================================
Multi-tenancy: Tenant -> User -> Client -> Property -> Report
"""
from __future__ import annotations
import uuid
from datetime import datetime
from enum import Enum
from sqlalchemy import (
    String, Integer, Float, Boolean, DateTime, ForeignKey, Text, JSON,
    Enum as SQLEnum, UniqueConstraint, Index,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.base import Base


def gen_uuid() -> str:
    return str(uuid.uuid4())


# ==========================================
# ENUMS
# ==========================================
class UserRole(str, Enum):
    ADMIN = "ADMIN"
    CONSULTANT = "CONSULTANT"
    STUDENT = "STUDENT"
    CLIENT = "CLIENT"


class TenantPlan(str, Enum):
    FREE = "FREE"
    BASIC = "BASIC"
    PRO = "PRO"
    ENTERPRISE = "ENTERPRISE"


class PropertyType(str, Enum):
    RESIDENTIAL = "RESIDENTIAL"
    COMMERCIAL = "COMMERCIAL"
    INDUSTRIAL = "INDUSTRIAL"
    LAND = "LAND"


class ReportStatus(str, Enum):
    DRAFT = "DRAFT"
    IN_REVIEW = "IN_REVIEW"
    APPROVED = "APPROVED"
    DELIVERED = "DELIVERED"


# ==========================================
# TENANT
# ==========================================
class Tenant(Base):
    __tablename__ = "tenants"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=gen_uuid)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    plan: Mapped[TenantPlan] = mapped_column(
        SQLEnum(TenantPlan), default=TenantPlan.FREE, nullable=False
    )
    branding: Mapped[dict] = mapped_column(JSON, default=dict)
    settings: Mapped[dict] = mapped_column(JSON, default=dict)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Relationships
    users: Mapped[list["User"]] = relationship(back_populates="tenant", cascade="all, delete-orphan")
    clients: Mapped[list["Client"]] = relationship(back_populates="tenant", cascade="all, delete-orphan")

    __table_args__ = (Index("ix_tenants_slug", "slug"),)


# ==========================================
# USER
# ==========================================
class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=gen_uuid)
    tenant_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False
    )
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    phone: Mapped[str | None] = mapped_column(String(20), nullable=True)
    role: Mapped[UserRole] = mapped_column(SQLEnum(UserRole), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    last_login: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Relationships
    tenant: Mapped["Tenant"] = relationship(back_populates="users")
    clients: Mapped[list["Client"]] = relationship(back_populates="consultant")

    __table_args__ = (
        UniqueConstraint("tenant_id", "email", name="uq_user_tenant_email"),
        Index("ix_users_email", "email"),
        Index("ix_users_role", "role"),
    )


# ==========================================
# CLIENT
# ==========================================
class Client(Base):
    __tablename__ = "clients"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=gen_uuid)
    tenant_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False
    )
    consultant_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    phone: Mapped[str | None] = mapped_column(String(20), nullable=True)
    address: Mapped[str | None] = mapped_column(Text, nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    metadata_json: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Relationships
    tenant: Mapped["Tenant"] = relationship(back_populates="clients")
    consultant: Mapped["User"] = relationship(back_populates="clients")
    properties: Mapped[list["Property"]] = relationship(
        back_populates="client", cascade="all, delete-orphan"
    )

    __table_args__ = (Index("ix_clients_tenant", "tenant_id"),)


# ==========================================
# PROPERTY
# ==========================================
class Property(Base):
    __tablename__ = "properties"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=gen_uuid)
    client_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("clients.id", ondelete="CASCADE"), nullable=False
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    property_type: Mapped[PropertyType] = mapped_column(
        SQLEnum(PropertyType), default=PropertyType.RESIDENTIAL
    )
    address: Mapped[str | None] = mapped_column(Text, nullable=True)
    city: Mapped[str | None] = mapped_column(String(100), nullable=True)
    pincode: Mapped[str | None] = mapped_column(String(10), nullable=True)
    latitude: Mapped[float | None] = mapped_column(Float, nullable=True)
    longitude: Mapped[float | None] = mapped_column(Float, nullable=True)
    floor_plan_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    north_direction_deg: Mapped[float | None] = mapped_column(Float, nullable=True)
    metadata_json: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Relationships
    client: Mapped["Client"] = relationship(back_populates="properties")
    reports: Mapped[list["Report"]] = relationship(
        back_populates="property", cascade="all, delete-orphan"
    )

    __table_args__ = (
        Index("ix_properties_client", "client_id"),
        Index("ix_properties_type", "property_type"),
    )


# ==========================================
# REPORT
# ==========================================
class Report(Base):
    __tablename__ = "reports"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=gen_uuid)
    property_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("properties.id", ondelete="CASCADE"), nullable=False
    )
    package: Mapped[str] = mapped_column(String(50), nullable=False)
    status: Mapped[ReportStatus] = mapped_column(
        SQLEnum(ReportStatus), default=ReportStatus.DRAFT
    )
    findings: Mapped[list] = mapped_column(JSON, default=list)
    guna_profile: Mapped[dict] = mapped_column(JSON, default=dict)
    scores: Mapped[dict] = mapped_column(JSON, default=dict)
    pdf_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    price_inr: Mapped[float | None] = mapped_column(Float, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Relationships
    property: Mapped["Property"] = relationship(back_populates="reports")

    __table_args__ = (
        Index("ix_reports_property", "property_id"),
        Index("ix_reports_status", "status"),
    )


# ==========================================
# LMS: COURSE
# ==========================================
class Course(Base):
    __tablename__ = "courses"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=gen_uuid)
    tenant_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False
    )
    instructor_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    thumbnail_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    language: Mapped[str] = mapped_column(String(10), default="en")
    duration_weeks: Mapped[int] = mapped_column(Integer, default=4)
    price_inr: Mapped[float] = mapped_column(Float, default=0)
    is_published: Mapped[bool] = mapped_column(Boolean, default=False)
    metadata_json: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    modules: Mapped[list["CourseModule"]] = relationship(
        back_populates="course", cascade="all, delete-orphan", order_by="CourseModule.order_index"
    )
    enrollments: Mapped[list["Enrollment"]] = relationship(
        back_populates="course", cascade="all, delete-orphan"
    )

    __table_args__ = (
        Index("ix_courses_tenant", "tenant_id"),
        Index("ix_courses_slug", "slug"),
    )


# ==========================================
# LMS: MODULE
# ==========================================
class CourseModule(Base):
    __tablename__ = "course_modules"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=gen_uuid)
    course_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("courses.id", ondelete="CASCADE"), nullable=False
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    order_index: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    course: Mapped["Course"] = relationship(back_populates="modules")
    lessons: Mapped[list["Lesson"]] = relationship(
        back_populates="module", cascade="all, delete-orphan", order_by="Lesson.order_index"
    )


# ==========================================
# LMS: LESSON
# ==========================================
class Lesson(Base):
    __tablename__ = "lessons"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=gen_uuid)
    module_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("course_modules.id", ondelete="CASCADE"), nullable=True
    )
    section_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("course_sections.id", ondelete="CASCADE"), nullable=True
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    content_type: Mapped[str] = mapped_column(String(20), default="video")
    content_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    text_content: Mapped[str | None] = mapped_column(Text, nullable=True)
    duration_minutes: Mapped[int] = mapped_column(Integer, default=0)
    order_index: Mapped[int] = mapped_column(Integer, default=0)
    is_preview: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    module: Mapped["CourseModule"] = relationship(back_populates="lessons")


# ==========================================
# LMS: ENROLLMENT
# ==========================================
class Enrollment(Base):
    __tablename__ = "enrollments"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=gen_uuid)
    course_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("courses.id", ondelete="CASCADE"), nullable=False
    )
    student_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    enrolled_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    progress_pct: Mapped[float] = mapped_column(Float, default=0.0)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    course: Mapped["Course"] = relationship(back_populates="enrollments")

    __table_args__ = (
        UniqueConstraint("course_id", "student_id", name="uq_enrollment"),
        Index("ix_enrollments_student", "student_id"),
    )


# ==========================================
# LMS: PROGRESS
# ==========================================
class LessonProgress(Base):
    __tablename__ = "lesson_progress"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=gen_uuid)
    enrollment_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("enrollments.id", ondelete="CASCADE"), nullable=False
    )
    lesson_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("lessons.id", ondelete="CASCADE"), nullable=False
    )
    is_completed: Mapped[bool] = mapped_column(Boolean, default=False)
    watch_seconds: Mapped[int] = mapped_column(Integer, default=0)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    __table_args__ = (
        UniqueConstraint("enrollment_id", "lesson_id", name="uq_progress"),
    )


# ==========================================
# LMS: CERTIFICATE
# ==========================================
class Certificate(Base):
    __tablename__ = "certificates"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=gen_uuid)
    enrollment_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("enrollments.id", ondelete="CASCADE"), nullable=False
    )
    certificate_number: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    issued_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    pdf_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    verification_url: Mapped[str | None] = mapped_column(String(500), nullable=True)

    __table_args__ = (Index("ix_certificates_number", "certificate_number"),)


# ==========================================
# KNOWLEDGE: GRANTHA (Classical Text Registry)
# ==========================================
class Grantha(Base):
    __tablename__ = "granthas"

    id: Mapped[str] = mapped_column(String(50), primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    sanskrit_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    author: Mapped[str | None] = mapped_column(String(255), nullable=True)
    period_approx: Mapped[str | None] = mapped_column(String(100), nullable=True)
    tradition: Mapped[str | None] = mapped_column(String(50), nullable=True)
    evidence_level: Mapped[str] = mapped_column(String(1), default="A")
    reliability_score: Mapped[float] = mapped_column(Float, default=0.9)
    metadata_json: Mapped[dict] = mapped_column(JSON, default=dict)


# ==========================================
# KNOWLEDGE: RULE
# ==========================================
class Rule(Base):
    __tablename__ = "rules"

    id: Mapped[str] = mapped_column(String(50), primary_key=True)
    category: Mapped[str] = mapped_column(String(50), nullable=False)
    topic: Mapped[str] = mapped_column(String(100), nullable=False)
    assertion: Mapped[str] = mapped_column(Text, nullable=False)
    condition: Mapped[dict] = mapped_column(JSON, default=dict)
    grantha_id: Mapped[str | None] = mapped_column(
        String(50), ForeignKey("granthas.id", ondelete="SET NULL"), nullable=True
    )
    chapter: Mapped[str | None] = mapped_column(String(50), nullable=True)
    verse: Mapped[str | None] = mapped_column(String(50), nullable=True)
    translation: Mapped[str | None] = mapped_column(Text, nullable=True)
    evidence_level: Mapped[str] = mapped_column(String(1), default="B")
    reliability_score: Mapped[float] = mapped_column(Float, default=0.8)
    tradition: Mapped[str | None] = mapped_column(String(50), nullable=True)
    confidence: Mapped[float] = mapped_column(Float, default=0.8)
    impact: Mapped[dict] = mapped_column(JSON, default=dict)
    remedies: Mapped[list] = mapped_column(JSON, default=list)
    conflicts_with: Mapped[list] = mapped_column(JSON, default=list)
    verified: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        Index("ix_rules_category", "category"),
        Index("ix_rules_topic", "topic"),
    )


# ==========================================
# FINDING (Generated by engines)
# ==========================================
class Finding(Base):
    __tablename__ = "findings"

    id: Mapped[str] = mapped_column(String(50), primary_key=True, default=gen_uuid)
    report_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("reports.id", ondelete="CASCADE"), nullable=False
    )
    category: Mapped[str] = mapped_column(String(50), nullable=False)
    severity: Mapped[str] = mapped_column(String(20), nullable=False)
    observed_condition: Mapped[str | None] = mapped_column(Text, nullable=True)
    geometry_ref: Mapped[dict] = mapped_column(JSON, default=dict)
    rule_ids: Mapped[list] = mapped_column(JSON, default=list)
    source_refs: Mapped[list] = mapped_column(JSON, default=list)
    tradition: Mapped[str | None] = mapped_column(String(50), nullable=True)
    evidence_level: Mapped[str] = mapped_column(String(1), default="B")
    confidence: Mapped[float] = mapped_column(Float, default=0.8)
    guna: Mapped[str | None] = mapped_column(String(20), nullable=True)
    recommendations: Mapped[list] = mapped_column(JSON, default=list)
    requires_human_review: Mapped[bool] = mapped_column(Boolean, default=False)
    engine_version: Mapped[str | None] = mapped_column(String(20), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        Index("ix_findings_report", "report_id"),
        Index("ix_findings_severity", "severity"),
    )


# ==========================================
# COMMERCE: PRODUCT
# ==========================================
class Product(Base):
    __tablename__ = "products"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=gen_uuid)
    tenant_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=True
    )
    sku: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    category: Mapped[str] = mapped_column(String(50), nullable=False)
    price_inr: Mapped[float] = mapped_column(Float, nullable=False)
    stock_qty: Mapped[int] = mapped_column(Integer, default=0)
    image_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    metadata_json: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        Index("ix_products_sku", "sku"),
        Index("ix_products_category", "category"),
    )


# ==========================================
# COMMERCE: ORDER
# ==========================================
class Order(Base):
    __tablename__ = "orders"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=gen_uuid)
    tenant_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False
    )
    user_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    total_inr: Mapped[float] = mapped_column(Float, nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="pending")
    razorpay_order_id: Mapped[str | None] = mapped_column(String(100), nullable=True)
    razorpay_payment_id: Mapped[str | None] = mapped_column(String(100), nullable=True)
    items: Mapped[list] = mapped_column(JSON, default=list)
    shipping_address: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    __table_args__ = (
        Index("ix_orders_tenant", "tenant_id"),
        Index("ix_orders_status", "status"),
    )


# ==========================================
# SUBSCRIPTION
# ==========================================
class Subscription(Base):
    __tablename__ = "subscriptions"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=gen_uuid)
    tenant_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False
    )
    user_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    plan: Mapped[str] = mapped_column(String(50), nullable=False)
    price_inr: Mapped[float] = mapped_column(Float, nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="active")
    starts_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    ends_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    razorpay_subscription_id: Mapped[str | None] = mapped_column(String(100), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    __table_args__ = (Index("ix_subscriptions_user", "user_id"),)


# ==========================================
# AUDIT LOG (Security)
# ==========================================
class AuditLog(Base):
    __tablename__ = "audit_logs"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=gen_uuid)
    tenant_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("tenants.id", ondelete="SET NULL"), nullable=True
    )
    user_id: Mapped[str | None] = mapped_column(String(36), nullable=True)
    action: Mapped[str] = mapped_column(String(100), nullable=False)
    entity_type: Mapped[str | None] = mapped_column(String(50), nullable=True)
    entity_id: Mapped[str | None] = mapped_column(String(36), nullable=True)
    ip_address: Mapped[str | None] = mapped_column(String(45), nullable=True)
    user_agent: Mapped[str | None] = mapped_column(String(500), nullable=True)
    details: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        Index("ix_audit_action", "action"),
        Index("ix_audit_user", "user_id"),
        Index("ix_audit_created", "created_at"),
    )


# ==========================================
# AUTH: PASSWORD RESET TOKEN
# ==========================================
class PasswordResetToken(Base):
    __tablename__ = "password_reset_tokens"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=gen_uuid)
    user_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    token_hash: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    used_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        Index("ix_prt_user", "user_id"),
        Index("ix_prt_expires", "expires_at"),
    )


# ==========================================
# AUTH: USER SESSION
# ==========================================
class UserSession(Base):
    __tablename__ = "user_sessions"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=gen_uuid)
    user_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    refresh_token_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    ip_address: Mapped[str | None] = mapped_column(String(45), nullable=True)
    user_agent: Mapped[str | None] = mapped_column(String(500), nullable=True)
    device: Mapped[str | None] = mapped_column(String(100), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    revoked_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    last_used_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    __table_args__ = (
        Index("ix_us_user", "user_id"),
        Index("ix_us_active", "is_active"),
    )


# ==========================================
# AUTH: OTP CODE
# ==========================================
class OTPCode(Base):
    __tablename__ = "otp_codes"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=gen_uuid)
    user_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    code_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    purpose: Mapped[str] = mapped_column(String(50), nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    used_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        Index("ix_otp_user", "user_id"),
        Index("ix_otp_purpose", "purpose"),
    )


# ==========================================
# LMS v2: COURSE SECTION
# ==========================================
class CourseSection(Base):
    __tablename__ = "course_sections"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=gen_uuid)
    course_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("courses.id", ondelete="CASCADE"), nullable=False
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    order_index: Mapped[int] = mapped_column(Integer, default=0)
    duration_minutes: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    __table_args__ = (Index("ix_sections_course", "course_id"),)


# ==========================================
# LMS v2: LESSON RESOURCE
# ==========================================
class LessonResource(Base):
    __tablename__ = "lesson_resources"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=gen_uuid)
    lesson_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("lessons.id", ondelete="CASCADE"), nullable=False
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    resource_type: Mapped[str] = mapped_column(String(20), default="pdf")  # pdf, video, link, doc
    url: Mapped[str] = mapped_column(String(500), nullable=False)
    size_kb: Mapped[int] = mapped_column(Integer, default=0)
    downloadable: Mapped[bool] = mapped_column(Boolean, default=True)
    order_index: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


# ==========================================
# LMS v2: QUIZ
# ==========================================
class Quiz(Base):
    __tablename__ = "quizzes"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=gen_uuid)
    section_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("course_sections.id", ondelete="CASCADE"), nullable=False
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    pass_percentage: Mapped[int] = mapped_column(Integer, default=70)
    time_limit_minutes: Mapped[int] = mapped_column(Integer, default=0)  # 0 = no limit
    max_attempts: Mapped[int] = mapped_column(Integer, default=3)
    shuffle_questions: Mapped[bool] = mapped_column(Boolean, default=False)
    is_published: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class QuizQuestion(Base):
    __tablename__ = "quiz_questions"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=gen_uuid)
    quiz_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("quizzes.id", ondelete="CASCADE"), nullable=False
    )
    question_text: Mapped[str] = mapped_column(Text, nullable=False)
    options: Mapped[list] = mapped_column(JSON, default=list)  # ["A", "B", "C", "D"]
    correct_option_index: Mapped[int] = mapped_column(Integer, nullable=False)
    explanation: Mapped[str | None] = mapped_column(Text, nullable=True)
    points: Mapped[int] = mapped_column(Integer, default=1)
    order_index: Mapped[int] = mapped_column(Integer, default=0)


class QuizAttempt(Base):
    __tablename__ = "quiz_attempts"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=gen_uuid)
    quiz_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("quizzes.id", ondelete="CASCADE"), nullable=False
    )
    student_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    answers: Mapped[dict] = mapped_column(JSON, default=dict)  # {question_id: selected_index}
    score_percentage: Mapped[float] = mapped_column(Float, default=0.0)
    passed: Mapped[bool] = mapped_column(Boolean, default=False)
    started_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    __table_args__ = (
        Index("ix_attempts_quiz", "quiz_id"),
        Index("ix_attempts_student", "student_id"),
    )


# ==========================================
# LMS v2: ASSIGNMENT
# ==========================================
class Assignment(Base):
    __tablename__ = "assignments"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=gen_uuid)
    section_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("course_sections.id", ondelete="CASCADE"), nullable=False
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    due_days: Mapped[int] = mapped_column(Integer, default=7)
    max_score: Mapped[int] = mapped_column(Integer, default=100)
    attachment_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    is_published: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class AssignmentSubmission(Base):
    __tablename__ = "assignment_submissions"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=gen_uuid)
    assignment_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("assignments.id", ondelete="CASCADE"), nullable=False
    )
    student_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    content_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    file_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    score: Mapped[float | None] = mapped_column(Float, nullable=True)
    feedback: Mapped[str | None] = mapped_column(Text, nullable=True)
    submitted_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    graded_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    __table_args__ = (
        Index("ix_submissions_assignment", "assignment_id"),
        Index("ix_submissions_student", "student_id"),
    )


# ==========================================
# LMS v2: DISCUSSION
# ==========================================
class DiscussionPost(Base):
    __tablename__ = "discussion_posts"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=gen_uuid)
    lesson_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("lessons.id", ondelete="CASCADE"), nullable=False
    )
    user_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    parent_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("discussion_posts.id", ondelete="CASCADE"), nullable=True
    )
    content: Mapped[str] = mapped_column(Text, nullable=False)
    upvotes: Mapped[int] = mapped_column(Integer, default=0)
    is_instructor: Mapped[bool] = mapped_column(Boolean, default=False)
    is_pinned: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    __table_args__ = (Index("ix_discussion_lesson", "lesson_id"),)


# ==========================================
# LMS v2: NOTES + BOOKMARKS
# ==========================================
class LessonNote(Base):
    __tablename__ = "lesson_notes"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=gen_uuid)
    lesson_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("lessons.id", ondelete="CASCADE"), nullable=False
    )
    student_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    content: Mapped[str] = mapped_column(Text, nullable=False)
    timestamp_seconds: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class LessonBookmark(Base):
    __tablename__ = "lesson_bookmarks"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=gen_uuid)
    lesson_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("lessons.id", ondelete="CASCADE"), nullable=False
    )
    student_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    note: Mapped[str | None] = mapped_column(Text, nullable=True)
    timestamp_seconds: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint("lesson_id", "student_id", name="uq_bookmark"),
    )


# ==========================================
# LMS v2: COURSE REVIEW
# ==========================================
class CourseReview(Base):
    __tablename__ = "course_reviews"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=gen_uuid)
    course_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("courses.id", ondelete="CASCADE"), nullable=False
    )
    student_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    rating: Mapped[int] = mapped_column(Integer, nullable=False)  # 1-5
    title: Mapped[str | None] = mapped_column(String(255), nullable=True)
    review_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint("course_id", "student_id", name="uq_review"),
    )


# ==========================================
# LMS v2: STUDENT STREAK
# ==========================================
class StudentStreak(Base):
    __tablename__ = "student_streaks"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=gen_uuid)
    student_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True
    )
    current_streak_days: Mapped[int] = mapped_column(Integer, default=0)
    longest_streak_days: Mapped[int] = mapped_column(Integer, default=0)
    last_activity_date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    total_learning_minutes: Mapped[int] = mapped_column(Integer, default=0)


# ==========================================
# LMS v2: ACHIEVEMENT
# ==========================================
class Achievement(Base):
    __tablename__ = "achievements"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=gen_uuid)
    student_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    badge_type: Mapped[str] = mapped_column(String(50), nullable=False)  # first_lesson, streak_7, course_complete, etc.
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    icon: Mapped[str] = mapped_column(String(50), default="ðŸ†")
    earned_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    __table_args__ = (Index("ix_achievements_student", "student_id"),)
