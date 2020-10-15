from lxml import etree, objectify
from decouple import config


class CreateXML:
    def __init__(self):
        self.amazon_xml_header = '''<?xml version="1.0"?>
       <AmazonEnvelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="amznenvelope.xsd"></AmazonEnvelope>
       '''

    def generate_mws_price_xml(self, data):

        root = objectify.fromstring(self.amazon_xml_header)
        head = objectify.Element('Header')
        head.DocumentVersion = '1.01'
        head.MerchantIdentifier = config('MWS_SELLER_ID')

        message_type = '<MessageType>Price</MessageType>'

        root.append(head)
        root.append(objectify.fromstring(message_type))

        for index, d in enumerate(data):
            message = objectify.Element('Message')
            message.MessageID = index + 1
            message['Price'] = objectify.Element('Price')
            message.Price.SKU = d['sku']
            message.Price.StandardPrice = objectify.fromstring(f'<StandardPrice currency="USD">{d["price"]}</StandardPrice>')

            root.append(message)

        objectify.deannotate(root)
        etree.cleanup_namespaces(root)

        # create the xml string
        obj_xml = etree.tostring(root,
                                 pretty_print=True,
                                 xml_declaration=True,
                                 encoding='utf-8')

        # from xml.dom.minidom import parseString
        # xml = parseString(obj_xml)
        # xml_pretty_str = xml.toprettyxml()
        # print(xml_pretty_str)

        return obj_xml


