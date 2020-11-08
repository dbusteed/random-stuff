#
#  Make a SOAP request with Python
#

from zeep import Client
from zeep.helpers import serialize_object

wsdl = 'http://dneonline.com/calculator.asmx?wsdl'

client = Client(wsdl)

response = serialize_object(
    client.service.Add(intA=5, intB=7)
)

print(response)