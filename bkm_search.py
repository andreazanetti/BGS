import argparse
import getpass
import utilities.url_utils as ul
from utilities.bigGsearch import search


def main(username, lpattern):
    ''' Search for pattern in the list of Chrome bookmarks
    Paramaters:
    uname:    username - useful to find the Chrome Bookmar
    pattern:  the pattern to match in the bookmarked page content '''

    bookmarks_file = username.join(
        ['/Users/', '/Library/Application\ Support/Google/Chrome/Default/Bookmarks'])
    bookmarks_file = bookmarks_file.replace("\\", '')
    print(f"bookmarks file used is: {bookmarks_file}")
    bmk_links = ul.get_Chrome_bookmarks_data(bookmarks_file)
    print("Data about bookmarks obtained.")

    ask = input("Want to print them out? Y/N/How many? ")
    if str(ask).strip(' ') == 'Y':
        ul.myprint(bmk_links.link_list, N=len(bmk_links.link_list))
    elif (int(ask) > 0) and (int(ask) <= len(bmk_links.link_list)):
        ul.myprint(bmk_links.link_list, N=int(ask))
    else:
        pass

    # test for uniquess of links in the Bookmarks. Not necessary but informative!
    n_unique_links = len(set(i[0] for i in bmk_links.link_list))
    n_links = len(bmk_links.link_list)
    if n_links != n_unique_links:
        print(f"{n_links - n_unique_links}Duplicate links exists!")
    else:
        print("There are no duplicate links! OK!")


if __name__ == '__main__':
    uname = getpass.getuser()
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--pattern', help='string to match in the bookmarked pages')
    args = parser.parse_args()
    pattern = args.pattern
    main(uname, pattern)



