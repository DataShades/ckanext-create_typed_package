#nex!/bin/bash
set -e

echo "This is travis-build.bash..."

echo "Installing the packages that CKAN requires..."
sudo apt-get update -qq
sudo apt-get install solr-jetty

if python -c 'import sys;exit(sys.version_info < (3,))'
then
    PYTHONVERSION=3
else
    PYTHONVERSION=2
fi

echo "Installing CKAN and its Python dependencies..."
git clone https://github.com/ckan/ckan
cd ckan

if [ -f requirement-setuptools.txt ]
then
    pip install -r requirement-setuptools.txt
fi
python setup.py develop

if [ -f requirements-py2.txt ] && [ $PYTHONVERSION = 2 ]
then
    grep -v psycopg2 < requirements-py2.txt > reqs.txt
else
    grep -v psycopg2 < requirements.txt > reqs.txt
fi
pip install psycopg2==2.7.7  # workaround travis 10 psycopg2 incompatibility
pip install -r reqs.txt
pip install -r dev-requirements.txt
cd -

echo "Setting up Solr..."
printf "NO_START=0\nJETTY_HOST=127.0.0.1\nJETTY_PORT=8983\nJAVA_HOME=$JAVA_HOME" | sudo tee /etc/default/jetty
sudo cp ckan/ckan/config/solr/schema.xml /etc/solr/conf/schema.xml
sudo service jetty restart

echo "Creating the PostgreSQL user and database..."
sudo -u postgres psql -c "CREATE USER ckan_default WITH PASSWORD 'pass';"
sudo -u postgres psql -c 'CREATE DATABASE ckan_test WITH OWNER ckan_default;'

echo "Initialising the database..."
cd ckan
ckan -c test-core.ini db init
cd -

echo "Installing extension and its requirements..."
python setup.py develop
pip install -r dev-requirements.txt

echo "Updating solr_url to single core"
sed -i -e 's/use = config:..\/ckan\/test-core.ini/use = config:..\/ckan\/test-core.ini\nsolr_url = http:\/\/127.0.0.1:8983\/solr/' test*.ini


echo "Moving test.ini into a subdir..."
mkdir subdir
mv test.ini subdir

echo "travis-build.bash is done."
