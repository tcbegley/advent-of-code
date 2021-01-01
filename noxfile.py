import nox

SOURCES = ["2015", "2017", "2020", "noxfile.py"]


@nox.session()
def lint(session):
    """Lint python source"""
    session.install("black", "flake8", "isort")
    session.run("black", "--check", *SOURCES)
    session.run("flake8", *SOURCES)
    session.run("isort", "--check", *SOURCES)
