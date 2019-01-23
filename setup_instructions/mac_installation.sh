echo "Setting up Compose for Mac. Make sure the setup_instructions folder is IN your current folder."
chmod +x ./setup_instructions/*
./setup_instructions/node_setup.sh
./setup_instructions/virtualenvw_setup.sh
./setup_instructions/pip_dep_setup.sh

echo "Running unit tests and integration tests:"
sh sls wsgi serve
python -m unittest
