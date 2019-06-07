#!/bin/bash -xe

function install_python27_env() {
    sudo yum install -y python27 python27-devel gcc
    python2.7 --version
    curl https://bootstrap.pypa.io/get-pip.py | sudo python2.7
    pip2.7 -V
    sudo pip2.7 install --upgrade pip
    sudo pip2.7 install virtualenv
    virtualenv -p python2.7 venv
}

function install_python3_env() {
    sudo yum install -y python3 python3-devel gcc
    python3 --version
    curl https://bootstrap.pypa.io/get-pip.py | sudo python3
    pip3 -V
    sudo pip3 install --upgrade pip
    sudo pip3 install virtualenv3
    virtualenv3 -p python3 venv
}

function activate_python_env() {
    . ./venv/bin/activate
}

function deactivate_python_env() {
    deactivate
}

function install_xi_iot_sdk_python2() {
    pushd xiiot_api
    python setup.py install
    popd
    python -c "import xiiot_api" 
    retval=$?
    if [[ "$retval" -ne "0" ]] ; then
        exit $retval
    fi 
}

function install_xi_iot_sdk_python3() {
    pushd xiiot_api
    python3 setup.py install
    popd
    python3 -c "import xiiot_api" 
    retval=$?
    if [[ "$retval" -ne "0" ]] ; then
        exit $retval
    fi 
}

function list_pip_installed_modules() {
    pip freeze
    pip3 freeze
}

function uninstall_xi_io_api() {
    pip uninstall -y xi-iot-sdk==1.0.0
    pip3 uninstall -y xi-iot-sdk==1.0.0
}

function fetch_public_api_swagger_json() {
    wget https://iot.nutanix.com/xi_iot_api.json -O xi_iot_api.json
 }

function generate_code_from_json() {
    download_swagger_codegen_cli
    #if mac
    # brew install swagger-codegen
    # swagger-codegen generate -i ./xi_iot_api.json \
    #                                        -l python \
    #                                        -o ./xiiot_api \
    #                                        -DpackageName=xiiot_api,projectName=xi_iot_sdk

    java -jar swagger-codegen-cli.jar config-help -l python 
    java -jar swagger-codegen-cli.jar help generate
    java -jar swagger-codegen-cli.jar generate -i ./xi_iot_api.json \
                                                -l python \
                                                -o ./xiiot_api \
                                                -DpackageName=xiiot_api,projectName=xi_iot_sdk
}

# function install_java() {

# }

function download_swagger_codegen_cli() {
    SWAGGER_CODEGEN_CLI_JAR_HTTP=http://central.maven.org/maven2/io/swagger/codegen/v3/swagger-codegen-cli/3.0.8/swagger-codegen-cli-3.0.8.jar
    SWAGGER_CODEGEN_CLI_JAR=swagger-codegen-cli.jar
    if [[ ! -f ${SWAGGER_CODEGEN_CLI_JAR} ]] ; then
        wget ${SWAGGER_CODEGEN_CLI_JAR_HTTP} -O ${SWAGGER_CODEGEN_CLI_JAR}
    fi
}

python_ver=-1
while getopts ":h23db:"  opt; do
  case ${opt} in
    2 ) # process option 2
      echo "user python ver2"
      python_ver=2
      ;;
    3 ) # process option 3
      echo "user python ver3"
      python_ver=3
      ;;
    * ) echo "Usage: $0 [-h|--help] [-2|-3]"; exit 1
      ;;
  esac
done

if [[ "$python_ver" == "-1" ]]; then
    echo "Usage: $0 [-h|--help] [-2|-3]"; exit 1
fi

rm -r xiiot_api || true
fetch_public_api_swagger_json
generate_code_from_json

if [[ "$python_ver" == "2" ]]; then
    install_xi_iot_sdk_python2

elif [[ "$python_ver" == "3" ]]; then
    install_xi_iot_sdk_python3
fi





