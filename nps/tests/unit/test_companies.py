from django.test import TransactionTestCase
from nps.models import Company, CompanyUser, Country

from nps.services.companies import add_person_to_company, add_person_to_company_bulk, company_bulk_create, company_create, company_exist, company_exist_by_id, company_get, company_list, person_company_relationship_exists, remove_person_from_company, update_person_rol
from users.models import User


class CompanyTestCase(TransactionTestCase):
    def setUp(self) -> None:
        self.country = Country.objects.create(name="Country1")
        return super().setUp()

    def test_company_insert_and_fetch(self):
        company1 = company_create(
            name="Company1",
            country=self.country.name,
            description="Company number 1"
        )
        company_create(
            name="Company2",
            country=self.country.name,
            description="Company number 2"
        )

        exists = company_exist(name="Company2")
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
        user = User.objects.create(full_name="Cristian", email="cristian@email.com")
        user.set_password("123456")
        user.save()

        company = company_create(
            name="Company2",
            country=self.country.name,
            description="Company number 2"
        )

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
        user = User.objects.create(full_name="Cristian", email="cristian@email.com")
        company1 = company_create(
            name="Company1",
            country=self.country.name,
            description="Company number 1"
        )
        company2 = company_create(
            name="Company2",
            country=self.country.name,
            description="Company number 2"
        )
        company3 = company_create(
            name="Company3",
            country=self.country.name,
            description="Company number 3"
        )

        relationships = [
            CompanyUser(role=CompanyUser.Roles.ACCOUNT_MANAGER, user=user, company=company1),
            CompanyUser(role=CompanyUser.Roles.CONSULTANT, user=user, company=company2),
            CompanyUser(role=CompanyUser.Roles.CONTACT, user=user, company=company3),
        ]

        response = add_person_to_company_bulk(relationships=relationships)
        self.assertEqual(len(response), len(relationships))

        relationships_in_db = CompanyUser.objects.all()
        self.assertEqual(len(relationships), relationships_in_db.count())
