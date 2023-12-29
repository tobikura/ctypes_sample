import pytest


def pytest_addoption(parser):
    parser.addoption("--build-type", action="store", help="Specify cmake build type")
    parser.addoption(
        "--build-dir", action="store", help="Specify cmake build directory"
    )


@pytest.fixture(scope="session")
def build_type(request):
    value = request.config.option.build_type
    if value is None:
        pytest.fail(
            "Not specified build type. Please use --build-type command line option"
        )
    return value


@pytest.fixture(scope="session")
def build_dir(request):
    value = request.config.option.build_dir
    if value is None:
        pytest.fail(
            "Not specified build directory. Please use --build-dir command line option"
        )
    return value
