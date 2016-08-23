from lxml import etree


def create_xml(csvTrades):

    class XMLNamespaces:
        core = 'http://cmegroup.com/schema/core/1.2'

    etree.register_namespace('core','http://cmegroup.com/schema/core/1.2')

    root = etree.Element(etree.QName(XMLNamespaces.core,'marginReq'),
                         nsmap={'core':XMLNamespaces.core})

    margin = etree.SubElement(root, 'margin')

    transactions = etree.SubElement(margin, 'transactions')

    transaction = etree.SubElement(transactions, 'transaction', type="TRADE", id="0")

    payload = etree.SubElement(transaction, 'payload', encoding="STRING", format="CSV")

    stringval = etree.SubElement(payload, 'string')

    stringval.text = csvTrades

    return etree.tostring(root, method='xml')

#fill in headers of portfolio margin request
def fill_data_line_header_object():

    portfolioLine = '"' + 'Firm Id' + '",'
    portfolioLine += '"' + 'Acct Id' + '",'
    portfolioLine += '"' + 'Exchange' + '",'
    portfolioLine += '"' + 'Ticker Symbol' + '",'
    portfolioLine += '"' + 'Product Name' + '",'
    portfolioLine += '"' + 'CC Code' + '",'
    portfolioLine += '"' + 'Period Code' + '",'
    portfolioLine += '"' + 'Put / Call' + '",'
    portfolioLine += '"' + 'Strike' + '",'
    portfolioLine += '"' + 'Underlying Period Code' + '",'
    portfolioLine += '"' + 'Net Positions' + '",'
    portfolioLine += '"' + 'Margin Type' + '",'
    portfolioLine += '"' + 'Client ID' + '",'

    portfolioLine += '\n'

    return portfolioLine


""""
fill_data_line_object with the following parameters
accountId : this should be an identifier of the portfolio you are interested in getting margin values on
exchangeSymbol : the symbol of the exchange (NYMEX, CME, etc...)
contractType : contract type (FUTURE, CALL, PUT)
spanFutureCode : the symbol used by the span and the exchange for the future (CL, ES ...)
spanOptionCode : the symbol used by the span and the exchange for the option (LO, ES ...)
futureContractYear : the future contract year (2016, 2017 ...)
futureContractMonth : the future contract month (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12)
optionYear : the option contract year (2016, 2017 ...)
optionMonth : the option contract month (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12)
optionStrike : the option strike
numberOfLots : the number of lots
"""
def fill_data_line_object(accountId, exchangeSymbol, contractType, spanFutureCode,
                       spanOptionCode, futureContractYear, futureContractMonth,
                       optionYear, optionMonth,
                       optionStrike, numberOfLots):

    portfolioLine = '"' + 'tml1' + '",'
    portfolioLine += '"' + accountId + '",'
    portfolioLine += '"' + exchangeSymbol.upper() + '",'
    portfolioLine += '"' + '",'
    portfolioLine += '"' + '",'

    if contractType.upper() == 'FUTURE':
        portfolioLine += '"' + spanFutureCode.upper() + '",'
        portfolioLine += '"' + str(futureContractYear) + str(futureContractMonth).zfill(2) + '",'
        portfolioLine += '"' + '",'
        portfolioLine += '"' + '",'
        portfolioLine += '"' + '",'
    else:
        portfolioLine += '"' + spanOptionCode.upper() + '",'
        portfolioLine += '"' + str(optionYear) + str(optionMonth).zfill(2) + '",'
        portfolioLine += '"' + contractType.upper() + '",'
        portfolioLine += '"' + str(optionStrike) + '",'
        portfolioLine += '"' + str(optionYear) + str(optionMonth).zfill(2) + '",'

    portfolioLine += '"' + str(numberOfLots) + '",'
    portfolioLine += '"' + '",'
    portfolioLine += '\n'

    return portfolioLine


# def createXMLtest():
#     # <membership/>
#     membership = Element('membership')
#
#     # <membership><users/>
#     users = SubElement(membership, 'users')
#
#     # <membership><users><user/>
#     SubElement(users, 'user', name='john')
#     SubElement(users, 'user', name='charles')
#     SubElement(users, 'user', name='peter')
#
#     # <membership><groups/>
#     groups = SubElement(membership, 'groups')
#
#     # <membership><groups><group/>
#     group = SubElement(groups, 'group', name='users')
#
#     # <membership><groups><group><user/>
#     SubElement(group, 'user', name='john')
#     SubElement(group, 'user', name='charles')
#
#     # <membership><groups><group/>
#     group = SubElement(groups, 'group', name='administrators')
#
#     # <membership><groups><group><user/>
#     SubElement(group, 'user', name='peter')
#
#     print(tostring(membership))
#
#     print('test2')

# def create_xml(csvTrades):
#     import sys
#
#     ElementTree.register_namespace('core','http://cmegroup.com/schema/core/1.2')
#
#     #et = ElementTree.ElementTree()
#
#     top = ElementTree.Element('core:marginReq')
#     #top.set('version', '1.0')
#     #top.set('encoding', 'utf-8')
#     #top.set('standalone', 'yes')
#
#     #top.append('xmlns:core="http://cmegroup.com/schema/core/1.2"')
#
#     #top.register_namespace('core', 'http://cmegroup.com/schema/core/1.2')
#
#     margin = ElementTree.SubElement(top, 'margin')
#
#     transactions = ElementTree.SubElement(margin, 'transactions')
#
#     transaction = ElementTree.SubElement(transactions, 'transaction', type="TRADE", id="0")
#
#     payload = ElementTree.SubElement(transaction, 'payload', encoding="STRING", format="CSV")
#
#     stringval = ElementTree.SubElement(payload, 'string')
#
#     stringval.text = csvTrades
#
#     #et = ElementTree.ElementTree(top)
#
#     #print(ElementTree.tostring(top, method='xml'))
#
#     #print('test2')
#
#     #ElementTree(top).write('test.xml')
#
#     tree = ElementTree.ElementTree(top)
#     #tree. register_namespace('core', 'http://cmegroup.com/schema/core/1.2')
#     #tree.write('test.xml')
#
#     print(ElementTree.tostring(tree, encoding='UTF-8', xml_declaration=True))
#
#     return ElementTree.tostring(top, method='xml') #ElementTree(top).write(sys.stdout)

