# Run black on all the project
black:
    black *.py

# Remove all python artifacts
clean:
    rm -rf __pycache__/

# Display the first errors of pydocstrings
checkdocstrings:
    pydocstyle -e 2> /dev/null | head
