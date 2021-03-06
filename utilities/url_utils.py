'''
Module contains functions to get and organize the list of urls
from the bookmarked ones, that match the search pattern
'''

import json
from utilities.bigGsearch import search
from urllib.error import HTTPError
import time

__all__ = [

    # Main class to represent bookmarks.
    'dfs_chrome_bookmarks',

    # Search function.
    'do_search',
]

class dfs_chrome_bookmarks():
    """
    Class that explores the Chrome Bookmarks file
    to return a list of tuples, with (link, location in bmk tree)
    Params:
    count: number of links found
    link_list: list of tuples (link,location in bmk tree)"
    link_dict: dictionary of path: [list of links at that path]
    Methods:
    _explore_bmk_file: to fill the list of links and the dictionary
    """
    # Todo: make this class iterable (Iteration protocol support)

    def __init__(self, dd, loc=('na',)):
        self.count = 0
        self.link_list = []
        self.link_dict = dict()
        self._explore_bmk_file(dd, loc=('na',))


    def _explore_bmk_file(self, dd, loc=('na',)):
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

            # if the dictionary is about a url, add the url the list of urls, along with its position
            # in the tree of bookmarks
            self.link_list.append((dd['url'], loc + (dd['name'],)))

            # fill the simplified dictionary
            if tuple(loc) not in self.link_dict.keys():
                self.link_dict[tuple(loc)] = [dd['url']]
            else:
                self.link_dict[tuple(loc)].append(dd['url'])

            # increment the count of links
            self.count += 1
        else:
            # The received dict is related to a folder of bookmarks
            for i in dd.keys():
                if isinstance(dd[i], dict):
                    # let's explore into dict in any case: we will select interesting info as we go deep
                    if 'name' in dd.keys():
                        ml = loc + (dd['name'],)
                    else:
                        ml = loc + ('na',)
                    # recursively look into subtree
                    self._explore_bmk_file(dd[i], ml)

                elif isinstance(dd[i], list):  # this is the case of the children list of dicts
                    for k in dd[i]:
                        if isinstance(k, dict):
                            if 'name' in dd.keys():
                                ml = loc + (dd['name'],)
                            else:
                                ml = loc + ('na',)
                            # recursively look into subtree, for each dict in the list of dicts
                            self._explore_bmk_file(k, ml)
                else:
                    pass
                    # Todo: Make sure this is never relevant case

        return None


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


def _get_full_key(list_of_tuples, given_uncomplete):
    '''
    Getting the firt keys in list_of_lists_of_tuples that includes given_uncomplete
    :param list_of_tuples:
    :param given_uncomplete:
    :return: first matching key
    '''
    for ll in list_of_tuples:
            if ll[3:] == given_uncomplete:
                return ll[:]
    return None


def do_search(bmk_obj, pattern_sought=None, folder_list=None):
    '''
    Does the actual search for the pattern_sought in the urls contained in the
    bookmarks folder listed in the folder_list, using google.
    :param bmk_obj: dfs_chrome_bookmarks object representing the Chrome Bookmarks
    :param pattern_sought: pattern to match
    :param folder_list: list of Chrome Bookmarks folders for the specific search
    :return: None
    '''
    # test using google to search on for pattern on selected bookmarks
    # quick test on searching to match a pattern on a subset of bookmarked links:
    if folder_list is None:
        folder_list = [('Bookmarks Bar', 'Andrea', 'Science', 'Ricerca'),
                       ('Bookmarks Bar', 'POL PHD', 'Comp-Neurosc.'),
                       ('Bookmarks Bar', 'POL PHD', 'MathCognition')]
    if pattern_sought is None:
        pattern_sought = 'neuron'

    print(f"\n\n\ndo_search: Test of search of '{pattern_sought}' in selected bookmarks folders:\n{folder_list}")

    for i in folder_list:
        kk = _get_full_key(bmk_obj.link_dict.keys(), i)
        print(kk)
        for j in bmk_obj.link_dict[kk]:
            try:
                # Todo: Get from search the link with a sample of the sentence where the patter was found
                # for better and more informative display of results
                res = search(f"site:{j} {pattern_sought}", stop=10)
                print(f"Results for search of '{pattern_sought}'in folder {i}, url {j}:")
                print(list(res))
                time.sleep(3)  # avoid being banned by Google
            except HTTPError as e:
                print(f"While analysing site {j} got HTTP Error")
                print(f"HTTP Error: {e}")

    return None