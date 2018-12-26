import requests
from xml.etree import ElementTree

url = "https://swsim.testing.stamps.com/swsim/swsimv71.asmx"

headers = {
    'User-Agent': 'Crosscheck Networks SOAPSonar',
    'content-type': 'text/xml; charset=utf-8',
    'charset': 'utf-8'
}

body = """
<?xml version="1.0" encoding="UTF-8"?>
<soap:Envelope
               xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
               xmlns:xsd="http://www.w3.org/2001/XMLSchema"
               xmlns:tns=“http://stamps.com/xml/namespace/2018/03/swsim/swsimv71”
>

    <soap:Body>
    
        <AuthenticateUser>
        
            <tns:Credentials>
            
                <IntegrationsID>
                    ID
                </IntegrationsID>
                
                <Username>
                    USERNAME
                </Username>
                
                <Password>
                    PASSWORD
                </Password>
            
            </tns:Credentials>
            
        </AuthenticateUser>
    
    </soap:Body>
</soap:Envelope>

""".encode('utf-8')

r = requests.post(url, headers=headers, data=body)
print(r.content)






