# To contribute improvements to CI/CD templates, please follow the Development guide at:
# https://docs.gitlab.com/ee/development/cicd/templates.html
# This specific template is located at:
# https://gitlab.com/gitlab-org/gitlab/-/blob/master/lib/gitlab/ci/templates/Python.gitlab-ci.yml

# Official language image. Look for the different tagged releases at:
# https://hub.docker.com/r/library/python/tags/
image: python:latest

# Change pip's cache directory to be inside the project directory since we can
# only cache local items.
variables:
  PIP_CACHE_DIR: "$CI_PROJECT_DIR/.cache/pip"

# https://pip.pypa.io/en/stable/topics/caching/
cache:
  paths:
    - .cache/pip

before_script:
  - python --version ; pip --version  # For debugging
  - pip install virtualenv
  - virtualenv venv
  - source venv/bin/activate

test:
  script:
    - pip install ruff tox  # you can also use tox
    - pip install --editable ".[test]"
    - tox -e py,ruff

run:
  script:
    - pip install .
    # run the command here
  artifacts:
    paths:
      - build/*

pages:
  script:
    - pip install sphinx sphinx-rtd-theme
    - cd doc
    - make html
    - mv build/html/ ../public/
  artifacts:
    paths:
      - public
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH

deploy:
  stage: deploy
  script: echo "Define your deployment script!"
  environment: production

