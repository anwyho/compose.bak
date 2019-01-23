echo "Installing awscli, virtualenv, and virtualenvwrapper globally..."
pip install awscli virtualenv virtualenvwrapper

echo "Setting up global variables for virtual environment..."
mkdir -p $WORKON_HOME

echo "Appending the following lines to ~/.bashrc and sourcing ~/.bashrc..."
COMMANDS="export WORKON_HOME=${WORKON_HOME}
source /usr/local/bin/virtualenvwrapper.sh"
echo "$COMMANDS" | tee -a ~/.bashrc
source ~/.bashrc

echo "Making virtual environment named ${PROJECT_NAME} ...
(Following https://virtualenvwrapper.readthedocs.io/en/latest/install.html)"
mkvirtualenv ${PROJECT_NAME}
workon ${PROJECT_NAME}

echo "Moving hook scripts to virtual environment and setting up hooks..."
cp ./compose/scripts/hooks/postactivate ./compose/scripts/hooks/predeactivate $WORKON_HOME/$PROJECT_NAME/bin/
source $WORKON_HOME/$PROJECT_NAME/bin/postactivate

echo "Testing success in virtual environment installation..."
deactivate
lsvirtualenv
workon ${PROJECT_NAME}

echo "Installed awscli, virtualenv, and virtualenvwrapper globally."

./setup_instructions/pip_dep_setup.sh


