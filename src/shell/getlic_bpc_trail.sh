#/bin/bash
eth_name=`dmidecode -s system-uuid|fold -12|sed -n '$p'`
cd /opt/smartprobe/sp/dp/bin && ./digest.sh
cd /root
curl -X POST "http://172.16.11.54:8090/munich/login" -H "Content-Type:application/x-www-form-urlencoded" -d "userName=sherry.zheng" -d "password=enh5QDkxOA==" -o /root/result.txt --cookie-jar /root/cookie.txt
curl -v -X GET "http://172.16.11.54:8090/munich/npm/devEnterprise"  --cookie cookie.txt>/dev/null
curl -v -X POST "http://172.16.11.54:8090/munich/npm/devEnterprise" --cookie cookie.txt -o result.txt -H "Content-Type: multipart/related" -H "Host:172.16.11.54:8090" -H "Connection:keep-alive" -H "User-Agent: Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.36 Safari/537.36" -H "Accept:*/*" -H "Origin:http://172.16.11.54:8090" -H "X-Requested-With:XMLHttpRequest" -H "Referer:http://172.16.11.54:8090/munich/npm/devEnterprise" -H "Accept-Encoding:gzip, deflate" -F digestInputFile=@/opt/smartprobe/sp/dp/bin/dataprovider.digest -F expireDaysAfter=30 -F orderNo=TESTORDER -F volume=512 -F socp=10 -F serialNumber=LIC_${eth_name}_$(date +"%B_%d_%Y") -F authorizedUser=授权信息${eth_name} -F scope=dev -F desc=主服务器 -F projectType=DevEnterprise -F insistOnSubmit=false 
sleep 8
curl -v -X POST http://172.16.11.54:8090$(curl -X POST http://172.16.11.54:8090/munich/npm/lic -H "Content-Type:application/x-www-form-urlencoded" -H "Accept-Encoding:gzip, deflate" --cookie cookie.txt --silent --stderr -|grep -A 30 ${eth_name}|grep -Eo 'data-url="[^\"]+download"'|grep -Eo '(/munich)[^"]+'|head -1) -F downloadToken=$(date +'%s') --cookie cookie.txt -o /opt/smartprobe/sp/dp/bin/dataprovider.lic

