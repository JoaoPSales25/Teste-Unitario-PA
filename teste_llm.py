import datetime
import pytest


class System:
    def __init__(self):
        self._logged_in_user_role = None

    def login(self, username, password):
        """Simula o login do usuário."""
        if username == "admin" and password == "valid_password":
            self._logged_in_user_role = "admin"
            return True
        self._logged_in_user_role = None
        return False

    def has_admin_privilege(self):
        """Verifica se o usuário logado tem privilégio de administrador."""
        return self._logged_in_user_role == "admin"

    def generate_report(self, start_date_str, end_date_str):
        """Simula a validação de parâmetros para geração de relatório."""
        try:
            start_date = datetime.datetime.strptime(start_date_str, "%Y-%m-%d")
            end_date = datetime.datetime.strptime(end_date_str, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Formato de data inválido. Use AAAA-MM-DD.")

        if end_date < start_date:
            raise ValueError("A data final não pode ser anterior à data inicial.")

        return "Relatório gerado com sucesso."


# Fixture para fornecer uma nova instância do sistema para cada função de teste
@pytest.fixture
def system_instance():
    """Fornece uma instância limpa do Sistema."""
    return System()


def test_successful_admin_login(system_instance):
    """
    Testa se um usuário com credenciais de administrador válidas pode fazer login com sucesso.
    Corresponde a: TC-1, Etapa 1
    """
    # Cenário: Tentativa de login com credenciais de admin corretas
    result = system_instance.login("admin", "valid_password")

    # Verificação: O login deve ser bem-sucedido e o privilégio de admin concedido
    assert (
        result is True
    ), "O login de admin deveria ser bem-sucedido com as credenciais corretas."
    assert (
        system_instance.has_admin_privilege() is True
    ), "O usuário deveria ter privilégio de admin após o login."


def test_failed_login_with_invalid_credentials(system_instance):
    """
    Testa se um usuário com credenciais inválidas não consegue fazer login.
    Corresponde a: TC-1, Etapa 2
    """
    # Cenário: Tentativa de login com credenciais incorretas
    result = system_instance.login("user", "invalid")

    # Verificação: O login deve falhar e o privilégio de admin não deve ser concedido
    assert result is False, "O login deveria falhar com credenciais incorretas."
    assert (
        system_instance.has_admin_privilege() is False
    ), "O privilégio de admin não deveria ser concedido após um login falho."


@pytest.fixture
def logged_in_system():
    """
    Fornece uma instância do Sistema com um usuário admin já logado.
    Pré-condição para TC-2.
    """
    system = System()
    system.login("admin", "valid_password")
    return system


def test_report_generation_with_valid_parameters(logged_in_system):
    """
    Testa a geração de relatório com parâmetros válidos.
    Corresponde a: TC-2, Etapa 2
    """
    # Cenário: Fornecer datas de início e fim válidas
    start_date = "2023-01-01"
    end_date = "2023-01-31"

    # Ação e Verificação: O sistema deve aceitar os parâmetros e proceder
    try:
        result = logged_in_system.generate_report(start_date, end_date)
        assert result == "Relatório gerado com sucesso."
    except ValueError:
        pytest.fail(
            "A geração do relatório falhou inesperadamente com parâmetros válidos."
        )


def test_report_generation_with_invalid_date_range(logged_in_system):
    """
    Testa a geração de relatório com um intervalo de datas inválido (data final antes da inicial).
    Corresponde a: TC-2, Etapa 3
    """
    # Cenário: Fornecer uma data final que é anterior à data inicial
    start_date = "2023-02-01"
    end_date = "2023-01-31"

    # Ação e Verificação: O sistema deve lançar um erro de valor
    with pytest.raises(ValueError) as excinfo:
        logged_in_system.generate_report(start_date, end_date)
    assert "A data final não pode ser anterior à data inicial." in str(excinfo.value)


def test_report_generation_with_invalid_date_format(logged_in_system):
    """
    Testa a geração de relatório com formatos de data inválidos.
    """
    # Cenário: Fornecer datas em um formato incorreto
    start_date = "01-01-2023"
    end_date = "31-01-2023"

    # Ação e Verificação: O sistema deve lançar um erro de valor devido ao formato
    with pytest.raises(ValueError) as excinfo:
        logged_in_system.generate_report(start_date, end_date)
    assert "Formato de data inválido. Use AAAA-MM-DD." in str(excinfo.value)
