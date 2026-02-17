# noxfile.py

import importlib
import os
import shutil

import nox

nox.options.sessions = []


@nox.session(name="cleanup", python=False)
def run_cleanup(session: nox.Session) -> None:
    """Use os/shutil to remove some files/directories"""

    if os.path.exists(".coverage"):
        os.remove(".coverage")

    if os.path.exists("reports"):
        shutil.rmtree("reports")

    folders = [".pytest_cache"]
    for f in folders:
        if os.path.exists(f):
            shutil.rmtree(f)

    # Recursively delete all __pycache__ folders and .pyc files
    session.run(
        "find",
        ".",
        "-type",
        "d",
        "-name",
        "__pycache__",
        "-exec",
        "rm",
        "-r",
        "{}",
        "+",
        external=True,
    )
    session.run(
        "find", ".", "-type", "f", "-name", "*.pyc", "-delete", external=True
    )


@nox.session(name="lint", python=False)
@nox.session(name="linter", python=False)
def run_lint(session: nox.Session) -> None:
    """
    Run black and isort with the github config file

    """

    session.run("pip", "install", "--upgrade", "--quiet", "black")
    session.run("pip", "install", "--upgrade", "--quiet", "isort")

    black_command = [
        "black",
        "--line-length",
        "79",
        "--target-version",
        "py310",
        ".",
    ]
    isort_command = [
        "isort",
        "--profile",
        "black",
        "--multi-line",
        "3",
        "--trailing-comma",
        "--force-grid-wrap",
        "0",
        "--line-length",
        "79",
        "--use-parentheses",
        ".",
    ]

    if not "write" in session.posargs:
        black_command.insert(1, "--check")
        isort_command.insert(1, "--check-only")
        isort_command.insert(2, "--diff")

    session.run(*black_command)
    session.run(*isort_command)


@nox.session(name="spell", python=False)
@nox.session(name="codespell", python=False)
def run_codespell(session: nox.Session) -> None:
    """
    Run codespell with the github config file

    Use the optional 'write' argument to write the corrections directly into
    the files. Otherwise, you will only see a summary of the found errors.

    """

    session.run("pip", "install", "--upgrade", "--quiet", "codespell")
    command = ["codespell", "--config", ".github/linters/.codespellrc"]

    if "write" in session.posargs:
        command.append("-w")

    session.run(*command)


@nox.session(name="tests", python=False)
@nox.session(name="test", python=False)
def run_pytest(session: nox.Session) -> None:
    """
    Run pytest and generate test/coverage reports

    Use the optional 'parallel' argument to run the tests in parallel. As just
    a flag, the number of workers will be determined automatically. Otherwise,
    you can specify the number of workers using an int, e.g., parallel=4.

    """

    package = importlib.util.find_spec("bird")

    if "no-reports" in session.posargs:
        command = [
            "pytest",
            f"--cov=.",  # for editable or site-packages
            "tests/",
        ]
    else:
        command = [
            "pytest",
            "--cov=bird",
            "--cov-report=html:reports/htmlcov",
            "--cov-report=xml:reports/coverage.xml",
            "--junitxml=reports/junit.xml",
            "tests/",
        ]

    for arg in session.posargs:
        if arg.startswith("parallel="):
            command[1:1] = ["-n", arg.split("=")[-1]]
        elif arg.startswith("parallel"):
            command[1:1] = ["-n", "auto"]
    session.run(*command)
    run_cleanup(session)


def run_pre_commit(session: nox.Session) -> None:
    """
    Run all linters/tests and make new badges

    Order of sessions: flake8, codespell, pytest, genbade. Using 'format' for
    linter, 'write' for codespell, and/or 'parallel' for pytest is permitted.

    """

    run_lint(session)
    run_codespell(session)
    run_pytest(session)
