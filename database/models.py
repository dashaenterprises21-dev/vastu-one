"""
Vastu One - Database Models
"""

from sqlalchemy import (
    Column, Integer, String, Boolean, DateTime, Text, JSON,
    ForeignKey, Index
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database.db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    phone = Column(String(20), unique=True, index=True, nullable=True)
    password_hash = Column(String(255), nullable=False)

    # Verification
    email_verified = Column(Boolean, default=False)
    phone_verified = Column(Boolean, default=False)

    # Status
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    role = Column(String(20), default="user")  # user, premium, consultant, admin

    # Profile
    profile_image = Column(String(500), nullable=True)
    city = Column(String(100), nullable=True)
    state = Column(String(100), nullable=True)

    # Audit
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_login = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    reports = relationship("Report", back_populates="user", cascade="all, delete-orphan")
    sessions = relationship("Session", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User {self.email}>"


class Session(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    token = Column(String(500), unique=True, index=True, nullable=False)
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(String(500), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=False)
    is_active = Column(Boolean, default=True)

    user = relationship("User", back_populates="sessions")


class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    report_id = Column(String(50), unique=True, index=True, nullable=False)

    # Package info
    package = Column(String(20), default="silver")  # bronze/silver/gold/platinum
    price = Column(Integer, default=0)
    payment_status = Column(String(20), default="pending")  # pending/paid/failed
    payment_id = Column(String(100), nullable=True)

    # Data
    plan_data = Column(JSON, nullable=True)
    analysis_data = Column(JSON, nullable=True)

    # Meta
    client_name = Column(String(100), nullable=True)
    client_address = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=True)

    user = relationship("User", back_populates="reports")


class LoginAttempt(Base):
    """Track login attempts for rate limiting"""
    __tablename__ = "login_attempts"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), index=True, nullable=False)
    ip_address = Column(String(45), nullable=True)
    success = Column(Boolean, default=False)
    attempted_at = Column(DateTime(timezone=True), server_default=func.now())


class PasswordReset(Base):
    """Password reset tokens"""
    __tablename__ = "password_resets"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    token = Column(String(100), unique=True, index=True, nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    used = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


# Indexes for performance
Index("idx_user_email", User.email)
Index("idx_report_user", Report.user_id)
Index("idx_report_id", Report.report_id)