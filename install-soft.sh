echo "updating repositories..."
sudo apt-get update
#sudo apt-get upgrade -y -o Dpkg::Options::='--force-confdef' -o Dpkg::Options::='--force-confold'
echo "installing mysql"
sudo apt-get install -y mysql-server
echo "starting service ..."
sudo cp ./mysqld.cnf /etc/mysql/mysql.conf.d/mysqld.cnf
sudo service mysql restart
echo "creating the database ..."
sudo mysql -u root < ./createdbs.sql
sudo mysql -u root < ./cerbos.sql
echo "installing cerbos ..."
docker compose up
