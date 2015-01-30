# -*- coding: utf-8 -*-
import sys
import time
import json
import string
import urllib2
from operator import itemgetter



# enter your API Key here
API_KEY = "XXXXXXXXXXXXXXXXXXXXXX"



class User(object):
    def __init__(self, steamid, itemid=None):
        self.steamid	        = steamid
        self.PUBLIC_URL	        = "http://steamcommunity.com/profiles/%s/inventory/json/730/2/?l=english"%self.steamid
        self.API_URL	        = "http://api.steampowered.com/IEconItems_730/GetPlayerItems/v0001/?key=%s&SteamID=%s"%(API_KEY, self.steamid)
        self.public_contents    = None
        self.api_contents       = None
        self.items	        = {}
        self.itemid	        = itemid
        
        if self.itemid:
            self.get_api_contents()
            self.get_single_item(self.itemid)
        else:
            self.get_public_contents()
            self.get_api_contents()
            self.get_items()

    def get_public_contents(self):
        try:
            self.public_contents = json.loads(urllib2.urlopen(self.PUBLIC_URL).read())
        except:
            print "Error gettings items from public API server. Retrying..."
            time.sleep(1)
            return self.get_public_contents()

    def get_api_contents(self):
        try:
            self.api_contents = json.loads(urllib2.urlopen(self.API_URL).read())
        except:
            print "Error getting items from API Server. Retrying..."
            time.sleep(1)
            return self.get_api_contents()

    def get_items(self):
        try:
            print " "
            print "Listing all items..."
            print " "
            for item in self.public_contents['rgInventory']:
                index = "%s_%s"%(self.public_contents['rgInventory'][item]['classid'], self.public_contents['rgInventory'][item]['instanceid'])
                self.items[index] = {}
                self.items[index]['id'] = self.public_contents['rgInventory'][item]['id']
                
            for item in self.sort_items(self.public_contents['rgDescriptions']):
                if item[0] in self.items:
                    self.items[item[0]]['name'] = "".join(c for c in self.public_contents['rgDescriptions'][item[0]]['market_hash_name'] if c in string.printable)
                    nametag = ""
                    if 'fraudwarnings' in self.public_contents['rgDescriptions'][item[0]]:
                        self.items[item[0]]['nametag'] = self.public_contents['rgDescriptions'][item[0]]['fraudwarnings'][0]
                        nametag = "(%s) "%self.items[item[0]]['nametag']

                    id = self.items[item[0]]['id']
                    name = self.items[item[0]]['name']
                    wear = self.get_wear(id)
                    print "%s\n%sID: %s Wear: %s\n"%(name, nametag, id, wear)

            print " "
            self.next()


        except Exception, e:
            print "Error getting items. Possible reasons: Profile is private, Backpack is emtpy, Server is unresponsive."
            print "Retrying..."
            return self.get_items()

    def get_single_item(self, id):
        wear = self.get_wear(id)
        print " "
        print "Wear of %s: %s"%(id, wear)
        print " "
        self.next()

    def get_wear(self, id):
        try:
            for item in self.api_contents['result']['items']:
                if str(item['id']) == str(id):
                   for attribute in item['attributes']:
                        if attribute['defindex'] == 8:
                            return attribute['float_value']
        except:
            print "Failed to get the wear value. Something went wrong.. :("
            time.sleep(3)

    def next(self):
        input = raw_input("Enter another Steamid64:\n")
        if not input.startswith('765'):
            print "You entered an invalid Steamid64. Please try again."
            return self.next()
        try:
            steamid = int(input)
            print " "
            print "Listing all items..."
            print " "
            self.__init__(steamid)
        except:
            print "You entered an invalid Steamid64. Please try again."
            return self.next()
            
    def sort_items(self, contents):
        sorted_items = {}
        for item in contents:
            if contents[item]['tradable'] == 0:
                continue
            if contents[item]['type'] in ('Base Grade Key', 'Base Grade Container'):
                continue
            if 'Sticker' in contents[item]['type']:
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
    itemid = raw_input("\nPress ENTER to list all items or insert a specific Item ID: \n")
    if not itemid:
        print " "
        print "Connecting..."
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
    if not API_KEY:
        print "API Key not defined. Get your api key here: https://steamcommunity.com/dev/apikey"
        time.sleep(3)
        return
    print " "
    print "-----------------------------------------------------"
    print "CS:GO ITEM WEAR-FINDER WRITTEN BY H!GH VOLTAGE"
    print "http://steamcommunity.com/profiles/76561197982482557/"
    print "-----------------------------------------------------"
    print " "
    print "General Wear Values:"
    print "0.00 - 0.06 : Factory New"
    print "0.06 - 0.15 : Minimal Wear"
    print "0.15 - 0.37 : Field Tested"
    print "0.37 - 0.44 : Well-Worn"
    print "0.44 - 1.00 : Battle-Scarred"
    print " "
    print "Note: For some items the minimum and maximum wear values are different"
    print "Read them up here: http://i-am-fat.org/csgo-skins/#rifles"
    print " "
    get_steamid()

start()
