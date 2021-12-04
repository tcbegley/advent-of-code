import nox

SOURCES = ["2015", "2016", "2017", "2020", "2021", "src", "noxfile.py"]


@nox.session()
def lint(session):
    """Lint Python source"""
    session.install("black", "flake8", "isort")
    session.run("black", "--check", *SOURCES)
    session.run("flake8", *SOURCES)
    session.run("isort", "--check", *SOURCES)


@nox.session(name="format")
def format_(session):
    """Format Python source"""
    session.install("black", "isort")
    session.run("black", *SOURCES)
    session.run("isort", *SOURCES)
