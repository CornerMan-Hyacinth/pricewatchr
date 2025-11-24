from sqlalchemy import String, Float, ForeignKey, DateTime, func, Index, UniqueConstraint
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime, timezone
from uuid import uuid4
from typing import List, Optional
from app.database import Base

#----- USER MODEL --------------------------------
class User(Base):
    __tablename__ = "users"
    
    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, index=True, default=uuid4, nullable=False
    )
    email: Mapped[str] = mapped_column(String, index=True, unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    
    #----- Relationships --------------------------------
    products: Mapped[List["Product"]] = relationship(
        "Product", back_populates="owner", cascade="all, delete-orphan"
    )
    

#----- PRODUCT URL MODEL --------------------------------
class ProductURL(Base):
    __tablename__ = "product_urls"
    
    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, index=True, default=uuid4, nullable=False
    )
    product_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("products.id", ondelete="CASCADE"),
        index=True,
        nullable=False
    )
    url: Mapped[str] = mapped_column(String, unique=True, nullable=False, index=True)
    is_primary: Mapped[bool] = mapped_column(default=False)
    retailer: Mapped[str] = mapped_column(String(50), nullable=True)
    
    #----- Relationships --------------------------------
    product: Mapped["Product"] = relationship("Product", back_populates="urls")
    product_histories: Mapped[List["PriceHistory"]] = relationship(
        "PriceHistory", back_populates="product_url", cascade="all, delete-orphan"
    )
    
    #----- Constraints --------------------------------
    __table_args__ = (
        UniqueConstraint("product_id", "url", name="uq_product_url"),
        Index("ix_product_urls_product_id", "product_id"),
    )
    

#----- PRODUCT MODEL --------------------------------
class Product(Base):
    __tablename__ = "products"
    
    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, index=True, default=uuid4
    )
    user_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True,
        nullable=False
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    target_price: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    current_price: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    last_checked: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    added_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    
    #----- Relationships --------------------------------
    price_histories: Mapped[List["PriceHistory"]] = relationship(
        "PriceHistory", back_populates="product", cascade="all, delete-orphan"
    )
    urls: Mapped[List["ProductURL"]] = relationship(
        "ProductURL", back_populates="product", cascade="all, delete-orphan", lazy="joined"
    )
    owner: Mapped["User"] = relationship("User", back_populates="products")
    
    #----- Properties --------------------------------
    @property # get the primary url of the product
    def primary_url(self) -> str | None:
        for url in self.urls:
            if url.is_primary:
                return url.url
        return self.urls[0].url if self.urls else None
    

#----- PRICE HISTORY MODEL --------------------------------    
class PriceHistory(Base):
    __tablename__ = "price_history"
    __tableargs__ = (
        Index("ix_price_history_product_id_recorded_at", "product_id", "recorded_at"),
    )
    
    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, index=True, default=uuid4, nullable=False
    )
    product_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("products.id", ondelete="CASCADE"),
        index=True,
        nullable=False
    )
    product_url_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("product_urls.id", ondelete="CASCADE"),
        index=True,
        nullable=True
    )
    price: Mapped[float] = mapped_column(Float, nullable=False)
    recorded_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    
    #----- Relationships --------------------------------
    product: Mapped["Product"] = relationship("Product", back_populates="price_histories")
    product_url: Mapped[Optional["ProductURL"]] = relationship(
        "ProductURL", back_populates="product_histories"
    )
    
    #------ Indexes & Constraints ---------------------------
    __table_args__ = (
        Index("ix_price_history_product_recorded", "product_id", "recorded_at"),
        Index("ix_price_history_product_url_recorded", "product_url_id", "recorded_at"),
        UniqueConstraint("product_url_id", "recorded_at", name="uq_price_once_per_url_time"),
    )
