from django.test import TransactionTestCase
from nps.models import Company, CompanyUser

from nps.services.companies import (
    add_person_to_company,
    add_person_to_company_bulk,
    company_bulk_create,
    company_exist,
    company_exist_by_id,
    company_get,
    company_list,
    person_company_relationship_exists,
    remove_person_from_company,
    update_person_rol
)
from nps.tests.factories import CompanyFactory, CountryFactory, UserFactory


class CompanyTestCase(TransactionTestCase):
    def setUp(self) -> None:
        self.country = CountryFactory.create()
        return super().setUp()

    def test_company_insert_and_fetch(self):
        [company1, company2] = CompanyFactory.create(country=self.country, amount=2)

        exists = company_exist(name=company2.name)
        self.assertTrue(exists)

        companies_in_db = company_list()
        self.assertEqual(companies_in_db.count(), 2)

        company_in_db = company_get(id=company1.id)
        self.assertEqual(company_in_db.name, company1.name)

        exists_by_id = company_exist_by_id(id=company1.id)
        self.assertTrue(exists_by_id)

    def test_company_bulk_insert(self):
        companies = [
            Company(name="C1", description="Desc C1", country_name=self.country),
            Company(name="C2", description="Desc C2", country_name=self.country),
            Company(name="C3", description="Desc C3", country_name=self.country),
            Company(name="C4", description="Desc C4", country_name=self.country),
        ]

        result = company_bulk_create(companies=companies)
        self.assertEqual(len(result), len(companies))

        companies_in_db = company_list()
        self.assertEqual(companies_in_db.count(), len(companies))

    def test_company_user_relationship(self):
        user = UserFactory.create()
        company = CompanyFactory.create(country=self.country)

        add_person_to_company(
            user_id=user.id,
            company_id=company.id,
            role=CompanyUser.Roles.CONTACT
        )

        relationship_in_db = CompanyUser.objects.first()
        self.assertEqual(relationship_in_db.user.id, user.id)
        self.assertEqual(relationship_in_db.company.id, company.id)
        self.assertEqual(relationship_in_db.role, CompanyUser.Roles.CONTACT)

        update_person_rol(
            user_id=user.id,
            company_id=company.id,
            role=CompanyUser.Roles.ACCOUNT_MANAGER
        )

        relationship_in_db = CompanyUser.objects.first()
        self.assertEqual(relationship_in_db.user.id, user.id)
        self.assertEqual(relationship_in_db.company.id, company.id)
        self.assertEqual(relationship_in_db.role, CompanyUser.Roles.ACCOUNT_MANAGER)

        exists = person_company_relationship_exists(
            user_id=user.id, company_id=company.id
        )
        self.assertTrue(exists)

        remove_person_from_company(company_id=company.id, user_id=user.id)
        relationship_in_db = CompanyUser.objects.all()
        self.assertEqual(relationship_in_db.count(), 0)

    def test_add_person_to_company_bulk(self):
        user = UserFactory.create()
        [company1, company2, company3] = CompanyFactory.create(self.country, amount=3)

        relationships = [
            CompanyUser(role=role, user=user, company=company)
            for role, user, company in [
                (CompanyUser.Roles.ACCOUNT_MANAGER, user, company1),
                (CompanyUser.Roles.CONSULTANT, user, company2),
                (CompanyUser.Roles.CONTACT, user, company3),
            ]
        ]

        response = add_person_to_company_bulk(relationships=relationships)
        self.assertEqual(len(response), len(relationships))

        relationships_in_db = CompanyUser.objects.all()
        self.assertEqual(len(relationships), relationships_in_db.count())
