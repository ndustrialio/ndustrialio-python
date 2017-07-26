set -e
coverage run --include ./ndustrialio/apiservices/* test_runner.py
if [ -z ${MIN_CODE_COVERAGE+x} ]; then
    echo "env variable MIN_CODE_COVERAGE is not set - pipeline will pass regardless of coverage percent"
    coverage report
else
    coverage report --fail-under=$MIN_CODE_COVERAGE
fi
