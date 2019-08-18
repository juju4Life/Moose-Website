from lxml import etree, objectify
from decouple import config


class CreateXML:
    def __init__(self):
        self.amazon_xml_header = '''<?xml version="1.0"?>
       <AmazonEnvelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="amznenvelope.xsd"></AmazonEnvelope>
       '''

    def generate_mws_price_xml(self, sku, price, message_number):

        root = objectify.fromstring(self.amazon_xml_header)

        head = objectify.Element('Header')
        head.DocumentVersion = '1.01'
        head.MerchantIdentifier = config('MWS_SELLER_ID')

        message_type = '<MessageType>Price</MessageType>'

        message = objectify.Element('Message')
        message.MessageID = message_number
        message['Price'] = objectify.Element('Price')
        message.Price.SKU = sku
        message.Price.StandardPrice = objectify.fromstring(f'<StandardPrice currency="USD">{price}</StandardPrice>')

        root.append(head)
        root.append(objectify.fromstring(message_type))
        root.append(message)
        objectify.deannotate(root)
        etree.cleanup_namespaces(root)

        # create the xml string
        obj_xml = etree.tostring(root,
                                 pretty_print=True,
                                 xml_declaration=True,
                                 encoding='utf-8')

        # xml = parseString(obj_xml)
        # xml_pretty_str = xml.toprettyxml()
        # print(xml_pretty_str)

        return obj_xml

