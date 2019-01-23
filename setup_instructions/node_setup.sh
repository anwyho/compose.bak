echo "Installing node..."
brew install node

echo "Creating node modules..."
npm init

echo "Installing serverless with plugins and testing server..."
npm install -g serverless
npm install --save-dev serverless-wsgi serverless-python-requirements serverless-plugin-parent

echo "Setting default virtual environment folder to ~/VirEnvs..."
export WORKON_HOME=~/VirEnvs
export PROJECT_NAME=compose

echo "Installed NPM and Serverless globally."

echo "To set up your virtual environment:
  1. Install pip by running `python install pip3`.
  2. (Optional) Overwrite where virtualenvwrapper will keep virtual environments and what the environment name will be:
    i.  Run `export WORKON_HOME=[your_virenv_directory]`
    ii. Run `export PROJECT_NAME=[your_project_name]`
  3. Check to see that you have valid credentials and configs in ~/.aws/
  4. Check that you have the right parameters in AWS Parameter Store,
        specifically these two keys, as they are necessary for calling Facebook:
    i.  FB_PAGE_ACCESS
    ii. FB_VERIFY_TOK
  5. Insert any other necessary keys into the serverless.yml under functions.app.environment.[env_var_key_name]: \${ssm:[parameter_store_key_name]}
Once you've completed the above, run the next step by calling `./setup_instructions/virtualenvw_setup.sh`."
