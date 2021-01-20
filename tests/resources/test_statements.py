import pytest

from cuenca import Statement


@pytest.mark.vcr
def test_statement_one_download_pdf():
    statement: Statement = Statement.one(year=2019, month=5)
    assert isinstance(statement.pdf, bytes)


@pytest.mark.vcr
def test_statement_one_download_xml():
    statement: Statement = Statement.one(year=2019, month=7)
    assert isinstance(statement.xml, bytes)
