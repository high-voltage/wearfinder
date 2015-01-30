# -*- coding: utf-8 -*-
import sys
import time
import json
import string
import urllib2
from operator import itemgetter



# enter your API Key here
API_KEY = ""



class User(object):
    def __init__(self, steamid, itemid=None):
        self.steamid	= steamid
        self.PUBLIC_URL	= "http://steamcommunity.com/profiles/%s/inventory/json/730/2/?l=english"%self.steamid
        self.API_URL	= "http://api.steampowered.com/IEconItems_730/GetPlayerItems/v0001/?key=%s&SteamID=%s"%(API_KEY, self.steamid)
        self.items	= {}
        self.index	= 0
        self.itemid	= itemid
        self.readitems  = 0
        if self.itemid:
            self.get_wear()
        else:
            self.readitems = 1
            self.get_items()

    def get_items(self):
        contents = None
        
        try:
            contents = json.loads(urllib2.urlopen(self.PUBLIC_URL).read())
        except:
            print "Error gettings items from public API server. Retrying..."
            return self.get_contents()

        try:
            x = 0
            sorted_dict = {}
            for item in self.sort_items(contents['rgDescriptions']):
                x += 1
                nametag = ""
                self.items[x] = {}
                self.items[x]['name'] = "".join(c for c in contents['rgDescriptions'][item[0]]['market_hash_name'] if c in string.printable)
                self.items[x]['classid'] = contents['rgDescriptions'][item[0]]['classid']
                if 'fraudwarnings' in contents['rgDescriptions'][item[0]]:
                    self.items[x]['nametag'] = str(contents['rgDescriptions'][item[0]]['fraudwarnings'][0])
                    nametag = " (%s)"%str(contents['rgDescriptions'][item[0]]['fraudwarnings'][0])
                    
                print "%s: %s%s"%(x, self.items[x]['name'], nametag)

        except:
            print "Error getting items. Possible reasons: Profile is private, Backback is emtpy, Server is unresponsive."
            print "Retrying..."
            return self.get_items()
        
        self.get_item_index(contents)

    def get_item_index(self, contents):
        print " "
        index = raw_input("Enter the number infront of the item: ")
        try:
            index = int(index)
        except:
            print "You entered an invalid number. Please try again."
            return self.get_item_index(contents)

        if not int(index) in self.items:
            print "You entered an invalid number. Please only enter a number that is listed above."
            return self.get_item_index(contents)

        self.index = int(index)
        self.get_itemid(contents)

    def get_itemid(self, contents):
        for item in contents['rgInventory']:
            if contents['rgInventory'][item]['classid'] == self.items[self.index]['classid']:
                self.itemid = contents['rgInventory'][item]['id']
                self.get_wear()

    def get_wear(self):
        contents = None

        try:
            contents = json.loads(urllib2.urlopen(self.API_URL).read())
        except:
            print "Error getting items from API Server. Retrying..."
            return self.get_wear()

        try:
            for item in contents['result']['items']:
                if str(item['id']) == str(self.itemid):
                    for attribute in item['attributes']:
                        if attribute['defindex'] == 8:
                            if self.index:
                                print "\nWear value of %s: %s"%(self.items[self.index]['name'], attribute['float_value'])
                            else:
                                print "\nWear value of %s: %s"%(self.itemid, attribute['float_value'])
                                
            print " "
            print "Press ENTER to get another wear value..."
            print " "
            while True:
                char = sys.stdin.read(1)
                if str(char) == '\n':
                    if self.readitems:
                        self.get_items()
                    else:
                        get_steamid()
                    break
        except:
            print "Failed to get the wear value. Item does not exist?"

    def sort_items(self, contents):
        sorted_items = {}
        for item in contents:
            if contents[item]['tradable'] == 0:
                continue
            if contents[item]['type'] in ('Base Grade Key', 'Base Grade Container'):
                continue
            sorted_items[item] = contents[item]['market_hash_name']
        return sorted(sorted_items.items(), key=itemgetter(1))




def get_steamid():
    steamid = raw_input("Enter the Steamid64: ")
    if not steamid.startswith("765"):
        print "You entered an invalid Steamid64. Please try again."
        return get_steamid()
    
    try:
        steamid = int(steamid)
        get_itemid(steamid)
    except:
        print "You entered an invalid Steamid64. Please try again."
        return get_steamid()

def get_itemid(steamid):
    itemid = raw_input("\nDo you already have the Item ID? \nIf not, enter 'no', otherwise just enter the it: \n")
    if itemid.lower() == 'no':
        print " "
        print "Listing all items..."
        print " "
        print " "
        time.sleep(1)
        return User(steamid)
    else:
        try:
            itemid = int(itemid)
            User(steamid, itemid)
        except:
            print "You entered an invalid Item ID. Please try again."
            return get_itemid(steamid)

def start():
    print " "
    print "-----------------------------------------------------"
    print "CS:GO ITEM WEAR-FINDER WRITTEN BY H!GH VOLTAGE"
    print "http://steamcommunity.com/profiles/76561197982482557/"
    print "-----------------------------------------------------"
    print " "
    print "Wear Values:"
    print "0.00 - 0.06 : Factory New"
    print "0.06 - 0.15 : Minimal Wear"
    print "0.15 - 0.37 : Field Tested"
    print "0.37 - 0.44 : Well-Worn"
    print "0.44 - 1.00 : Battle-Scarred"
    print " "
    print " "
    get_steamid()

start()

