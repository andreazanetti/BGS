'''
Module contains functions to get and organize the list of urls
from the bookmarked ones, that match the search pattern
'''

import json
from utilities.bigGsearch import search


class dfs_chrome_bookmarks():
    '''Class that explores the Chrome Bookmarks file
    to return a list of tuples, with (link, location in bmk tree)
    Params:
    count: number of links found
    link_list: list of tuples (link,location in bmk tree)"
    Methods:
    explorer_go: to generate fill the list of link
    '''

    def __init__(self, count=0):
        self.count = count
        self.link_list = []
        self.link_dict = dict()

    def explore_bmk_file(self, dd, loc=('na',)):
        '''
        Fills the link_list with visiting in DFS the tree of bookmarks
        keeping track of the folder structure, so as for the user to select
        which folder to include or exclude later
        params: dd - dictionary
        return: nothing - side effect to fill self.link_list with tuple(url, (location in bmks))
        '''

        if 'url' in dd.keys():
            # link dict
            # print(f"This dict {dd['name']} represents a link, as type field is: {dd['type']}")
            # print(": ".join([dd['type'], dd['url']]))
            # print(dd['name'], "\n")
            # print("URL found and loc is:", loc)
            self.link_list.append((dd['url'], loc + (dd['name'],)))  # whenever there url, name is there?
            if tuple(loc) not in self.link_dict.keys(): # dd['name']
                self.link_dict[tuple(loc)] = [dd['url']] # loc + (dd['name'],)
            else:
                self.link_dict[tuple(loc)].append(dd['url']) # loc + (dd['name'],)
            self.count += 1
        else:
            # print("The received dict is related to a folder and has the following key fields:")
            # print([k for k in dd])
            for i in dd.keys():
                if isinstance(dd[i], dict):
                    # let's explore into dict in any case: we will select interesting info as we go deep
                    # print("Exlporing dict corresponding to current level key: ", i)
                    # print("loc is: ", loc)
                    if 'name' in dd.keys():
                        ml = loc + (dd['name'],)
                    else:
                        ml = loc + ('na',)
                    self.explore_bmk_file(dd[i], ml)

                elif isinstance(dd[i], list):  # this is the case of the children list of dicts
                    for k in dd[i]:
                        # print(f"exploring dict {dd['name']}: key {i}")
                        if isinstance(k, dict):
                            # print("dd[i] is a list: Exploring dict corresponding to current level key: ", i)
                            # print("dd[i] is a list: loc is: ", loc)
                            if 'name' in dd.keys():
                                ml = loc + (dd['name'],)
                            else:
                                ml = loc + ('na',)
                            self.explore_bmk_file(k, ml)
                else:
                    # Todo: Make sure this is never relevant case
                    pass


def get_Chrome_bookmarks_data(bmk_file):
    '''
    Open the Chrome bookmarks file of the user and
    return an object that contains all the links in a list of tuples
    :param bmk_file:
    :return:
    '''
    # Todo: make it return a dict with keys the location in the bookmark tree and values
    # Todo: the list of urls for each folder

    with open(bmk_file, 'rt') as data_file:
        bookmark_data = json.load(data_file)

    exx = dfs_chrome_bookmarks(0)
    exx.explore_bmk_file(bookmark_data)

    return exx


def myprint(stack, N=1000, offset=3):
    '''
    Helper to print out a list of tuples with the second element being a list
    :param stack:  list of tuples
    :param N:      default max elements to print
    :param offset: exclude offset initial elements of the second component
    :return:       None
    '''
    #Todo
    i = 0
    while stack and i < N:
        k, v = stack.pop()
        print(i, ' ', k, v[offset:])  # exclude ('na', 'na', 'na',)
        i += 1

def myprint_for_dict(dict_of_list_of_links, N=1000, offset=3):
    '''
    Helper to print out a list of tuples with the second element being a list
    :param dict_of_list_of_links:  dictionary of list of links, pertaining to a bookmark folder
    :param N:      default max elements to print
    :param offset: exclude offset initial elements of the second component
    :return:       None
    '''
    # Todo: make this check better
    assert(isinstance(dict_of_list_of_links, dict))

    for i, t in enumerate(dict_of_list_of_links.items()):
        (k, list_of_links) = t
        print(i,' ', k[offset:], list_of_links)

