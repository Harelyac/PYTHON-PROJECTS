import xml.etree.ElementTree as ET
from copy import deepcopy
import re


def get_attribute(store_db, ItemCode, tag):
    '''
    Returns the attribute (tag) 
    of an Item with code: Itemcode in the given store
    '''

    attribute = store_db[ItemCode][tag]
    return attribute

def string_item(item):
    '''
    Textual representation of an item in a store.
    Returns a string in the format of '[ItemCode] (ItemName)'
    '''
    TAB = "\t"

    item_identifier = "[" + item['ItemCode'] + "]" + TAB + "{" + item['ItemName'] + "}"
    return item_identifier


def string_store_items(store_db):
    '''
    Textual representation of a store.
    Returns a string in the format of:
    string representation of item1
    string representation of item2
    '''

    BREAK_LINE = "\n"

    items = store_db.keys()
    full_store = ""
    if store_db != {}:
        for item in items:
            full_store = full_store + string_item(store_db[item]) + BREAK_LINE
    return full_store

#print(string_store_items(temp_store))

def read_prices_file(filename):
    '''
    Read a file of item prices into a dictionary.  The file is assumed to
    be in the standard XML format of "misrad haclcala".
    Returns a tuple: store_id and a store_db,
    where the first variable is the store ID
    and the second is a dictionary describing the store.
    The keys in this db will be ItemCodes of the variety items in the store and the
    values are inner dictionaries mapping attribute names to their values.
    Important attributes include 'ItemCode', 'ItemName', and 'ItemPrice'
    '''

    tree = ET.parse(filename)
    root = tree.getroot()
    items = root.find('Items')
    store_id = root.find('StoreId').text

    # Make the two dicts
    items_dict = dict()
    attributes_dict = dict()
    attributes_dict_copy = dict()

    # Go over each item in the store
    for item in items:
        # Go over each attribute of the item
        for attribute in item:
            # Put all of them in "attributes dic"
            attributes_dict[attribute.tag] = attribute.text
        # Add all this deep copy dict as value to the "item code dic"
        attributes_dict_copy = deepcopy(attributes_dict)
        items_dict[item.find('ItemCode').text] = attributes_dict_copy

    return (store_id, items_dict)

def filter_store(store_db, filter_txt):
    '''
    Create a new dictionary that includes only the items
    that were filtered by user.
    I.e. items that text given by the user is part of their ItemName.
    Args:
    store_db: a dictionary of dictionaries as created in read_prices_file.
    filter_txt: the filter text as given by the user.
    '''
    filtered_store = dict()
    attributes_dict = dict()
    attributes_dict_copy = dict()

    for item in store_db:
        if filter_txt in store_db[item]["ItemName"]:
            for attribute in store_db[item]:
                attributes_dict[attribute] = store_db[item][attribute]
            attributes_dict_copy = deepcopy(attributes_dict)
            filtered_store[item] = attributes_dict_copy
    return filtered_store



def create_basket_from_txt(basket_txt):
    '''
    Receives text representation of few items (and maybe some garbage
      at the edges)
    Returns a basket- list of ItemCodes that were included in basket_txt
    '''

    DIGITS = "\d+"
    new_basket = list()
    p = re.compile('\[' + DIGITS + '\]')
    new_basket = p.findall(basket_txt)
    p = re.compile(DIGITS)
    new_basket = p.findall("".join(new_basket))

    return new_basket

def get_basket_prices(store_db, basket):
    '''
    Arguments: a store - dictionary of dictionaries and a basket -
       a list of ItemCodes
    Go over all the items in the basket and create a new list
      that describes the prices of store items
    In case one of the items is not part of the store,
      its price will be None.

    '''

    basket_prices = list()
    keys_list = store_db.keys()
    for item_code in basket:
        # Check if the item exist in the store at all
        if item_code in keys_list:
            if store_db[item_code]['ItemPrice']:
                basket_prices.append(float(store_db[item_code]['ItemPrice']))
        else:
            basket_prices.append(None)
    return basket_prices



def sum_basket(price_list):
    '''
    Receives a list of prices
    Returns a tuple - the sum of the list (when ignoring Nones)
      and the number of missing items (Number of Nones)

    '''

    sum_price_list = 0
    missing_items = 0

    for price in price_list:
        if not price:
            missing_items +=1
        else:
            sum_price_list = sum_price_list + price
    return sum_price_list, missing_items


def basket_item_name(stores_db_list, ItemCode):
    '''
    stores_db_list is a list of stores (list of dictionaries of
      dictionaries)
    Find the first store in the list that contains the item and return its
    string representation (as in string_item())
    If the item is not avaiable in any of the stores return only [ItemCode]

    '''

    for store in stores_db_list:
        for item in store:
            if store[item]["ItemCode"] == ItemCode:
                return string_item(store[item])
    return '[' + ItemCode + ']'


def save_basket(basket, filename):
    '''
    Save the basket into a file
    The basket reresentation in the file will be in the following format:
    [ItemCode1]
    [ItemCode2]
    ...
    [ItemCodeN]
    '''


    # Save a basket to file
    with open(filename, 'w') as basket_file:
        basket_file.write('[')
        basket_file.write(']\n['.join(basket))
        basket_file.write(']')

def load_basket(filename):
    '''
    Create basket (list of ItemCodes) from the given file.
    The file is assumed to be in the format of:
    [ItemCode1]
    [ItemCode2]
    ...
    [ItemCodeN]
    '''
    basket_list = list()

    # Load basket from a file
    with open(filename, 'r') as basket_file:
        basket_list = basket_file.readlines()
        p = re.compile('\d+')
        new_basket = p.findall("".join(basket_list))

    return new_basket

def best_basket(list_of_price_list):
    '''
    Arg: list of lists, where each inner list is list of prices as created
    by get_basket_prices.
    Returns the cheapest store (index of the cheapest list) given that a
    missing item has a price of its maximal price in the other stores *1.25

    '''
    sum_of_store1 = 0
    sum_of_store3 = 0
    sum_of_store2 = 0

    temp_list = deepcopy(list_of_price_list)
    PENALTY_NUM = 1.25
    STORE1 = 0
    STORE2 = 1
    STORE3 = 2

    # Convert all list to float and None to 0
    for list in range(len(temp_list)):
        for price_str in range(len(temp_list[list])):
            if not temp_list[list][price_str]:
                temp_list[list][price_str] = 0
            else:
                temp_list[list][price_str] = float(temp_list[list][price_str])

    for price in range(len(temp_list[STORE1])):
        #checks a penalty for a store
        if not temp_list[STORE1][price]:
            temp_list[STORE1][price] = PENALTY_NUM*(max(temp_list[STORE2][price], temp_list[STORE3][price]))

        elif not temp_list[STORE2][price]:
            temp_list[STORE2][price] = PENALTY_NUM*(max(temp_list[STORE1][price], temp_list[STORE3][price]))

        elif not temp_list[STORE3][price]:
            temp_list[STORE3][price] = PENALTY_NUM*(max(temp_list[STORE2][price], temp_list[STORE1][price]))

        # Sum up all the prices in store
        sum_of_store1 = sum_of_store1 + temp_list[STORE1][price]
        sum_of_store2 = sum_of_store2 + temp_list[STORE2][price]
        sum_of_store3 = sum_of_store3 + temp_list[STORE3][price]

    if min(sum_of_store1, sum_of_store2, sum_of_store3) == sum_of_store1:
        return STORE1
    elif min(sum_of_store1, sum_of_store2, sum_of_store3) == sum_of_store2:
        return STORE2
    elif min(sum_of_store1, sum_of_store2, sum_of_store3) == sum_of_store3:
        return STORE3
