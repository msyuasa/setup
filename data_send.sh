. /etc/default/iot.conf
echo $HOST
sudo python data_send.py -i ${PRODUCTID} -t ${TENANTID} -e ${HOST}
