class CompanyAddress(Base):
    """Company Address Module"""

    __tablename__ = 'companyAddress'
    id = Column(Integer, primary_key=True)
    country = Column(String(100), nullable=False)
    street = Column(String, nullable=False)
    town = Column(String(100), nullable=False)
    building = Column(String(100), nullable=False)
    phone = Column(String(10), nullable=False)
    email = Column(String, nullable=False)
    bp = Column(String(10), nullable=True)
    website = Column(String, nullable=True)
    company_id = Column(Integer, ForeignKey('companies.id'))

    company = relationship("Company", back_populates='addresses')