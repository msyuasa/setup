# 時刻の固定
sudo apt-get install fake-hwclock
# /etc/default/fake-hwclockのFORCE=forceのコメントを外す
sed -i -e "s/#FORCE=force/FORCE=force/" /etc/default/fake-hwclock

# NTPサーバの設定
sudo apt-get install ntp
# /etc/ntp.confの書き換え
sed -i -e "s/server 0.cz.pool.ntp.org iburst/#server 0.cz.pool.ntp.org iburst/" /etc/ntp.conf
sed -i -e "s/server 1.cz.pool.ntp.org iburst/#server 1.cz.pool.ntp.org iburst/" /etc/ntp.conf
sed -i -e "s/server 2.cz.pool.ntp.org iburst/#server 2.cz.pool.ntp.org iburst/" /etc/ntp/conf
sed -i -e "s/server 3.cz.pool.ntp.org iburst/#server 3.cz.pool.ntp.org iburst/" /etc/ntp.conf
#sed -i -e "s/server 3.cz.pool.ntp.org iburst/i server 192.168.0.2 iburst" /etc/ntp.conf

#sudo service ntp restart

# 固定IPの設定
# /etc/network/interfacesの書き換え
cp interfaces /etc/network/intefaces
sudo /etc/init.d/networking restart

