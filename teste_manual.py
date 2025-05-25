class AutenticationSystem:
    users = {
        "user": {"password": "123456", "isAdmin": False},
        "admin": {"password": "admin", "isAdmin": True},
    }

    def login(self, username, password) -> bool:
        usr = self.users.get(username)

        if usr == None or usr["password"] != password:
            return None

        return usr

    def login_admin(self, username, password):
        usr = self.login(username, password)
        if usr == None:
            return False
        return usr["isAdmin"]


class TestCase1:
    auth = AutenticationSystem()

    def test_valid_credentials(self):
        assert self.auth.login_admin("admin", "admin")

    def test_invalid_credentials(self):
        assert self.auth.login_admin("username", "123456") == False


from datetime import date


class ReportGeneration:

    criterias = ["criteria1", "criteria2", "criteria3"]

    def __init__(self, startDate, endDate, selectionCriteria):
        self.startDate = startDate
        self.endDate = endDate
        self.selectionCriteria = selectionCriteria

    def validate_parameters(self):
        if (
            type(self.startDate) != date
            or type(self.endDate) != date
            or self.selectionCriteria not in self.criterias
            or self.startDate > self.endDate
        ):
            return False

        return True

    def generate_report(self):
        if self.validate_parameters():
            return True

        return False


class TestCase2:

    def test_generate_valid_report(self):
        report = ReportGeneration(date(2025, 1, 25), date(2025, 5, 25), "criteria1")
        assert report.generate_report()

    def test_generate_invalid_report(self):
        report = ReportGeneration(date(2025, 1, 25), date(2024, 1, 25), "criteria2")
        assert report.generate_report() == False
