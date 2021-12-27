# Run black on all the project
black:
    black *.py

# Display the first errors of pylint
pylint:
    pylint --output-format=colorized *.py 2> /dev/null | head

# Remove all python artifacts
clean:
    rm -rf __pycache__/

# Display the first errors of pydocstrings
checkdocstrings:
    pydocstyle -e 2> /dev/null | head

# Simulate a pre-commit check on added files
prepre:
    git status
    pre-commit run --all-files

# Print the answers to the puzzles
answer:
    python advent.py
