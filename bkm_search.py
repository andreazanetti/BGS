import argparse
import getpass
import utilities.url_utils as ul
import os
import sys;


def report_on_data(bmk_links):

    print("...data about bookmarks obtained.")
    print(f"Number of links found: {len(bmk_links.link_list)}")

    # test for uniquess of links in the Bookmarks
    n_unique_links = len(set(i[0] for i in bmk_links.link_list))
    n_links = len(bmk_links.link_list)
    if n_links != n_unique_links:
        print(f"{n_links - n_unique_links} Duplicate links exists in your bookmarks!")
    else:
        print("There are no duplicate links! OK!")

    ask = input("Want to print the obtained links out? Y/N/How many? ")
    if str(ask).strip(' ') == 'Y':
        ul.myprint(bmk_links.link_list, N=n_links)
    elif (int(ask) > 0) and (int(ask) <= n_links):
        ul.myprint(bmk_links.link_list, N=int(ask))
    #Todo: do this well taking care of the N case....


def system_and_env_helper():
    '''
    Collects info about the system, platform and check/set env variables
    :return: list of proxy related env variables name
    '''
    # preliminary check on system
    # print('Python %s on %s' % (sys.version, sys.platform))

    # check and set env variables
    # get environment
    env_keys = os.environ.keys()

    # collect env variables related to proxy settings
    print("Initial environment is the following:")
    for k, v in os.environ.items():
        print(f'{k}={v}')
    proxy_env_keys = [k for k in env_keys if ("PROXY" in k.upper()
                                            and "NO_PROXY" not in k.upper())]
    for k in proxy_env_keys:
        print(f"proxy related env variable {k} = {os.environ[k]}")
    proxy_choice = input("Do you want to use thi proxy settings (Y) or you want to skip the proxy (S)?")
    if proxy_choice.upper\
                () == 'S':
        for k in proxy_env_keys:
            del (os.environ[k])
        print("\n\n\Current status of proxy env vars AFTER del:")
        for k in proxy_env_keys:
            print(f'{k}={os.environ.get(k)}')

    return proxy_env_keys


def print_env():
    '''
    Helper function to print env variables
    :return: None
    '''
    for k, v in os.environ.items():
            print(f'{k}={v}')

    return None

def main(username, lpattern):
    '''
    Search for pattern in the list of Chrome bookmarks
    :param username: useful to find the Chrome Bookmarks
    :param lpattern: pattern to match in the bookmarked page content
    '''

    proxy_env_keys = system_and_env_helper()
    # # check that the environment is set after the call:
    # print("\n\nCurrent status of environment AFTER del but in MAIN:")
    # for k in proxy_env_keys:
    #     print(f'{k}={os.environ.get(k)}')
    #print_env()

    #Todo: check for data in input to be ok

    bookmarks_file = username.join(
        ['/Users/', '/Library/Application\ Support/Google/Chrome/Default/Bookmarks'])
    bookmarks_file = bookmarks_file.replace("\\", '')
    print(f"Bookmarks file used is: {bookmarks_file}")
    bmk_links = ul.get_Chrome_bookmarks_data(bookmarks_file)
    report_on_data(bmk_links)

    # check dictionary has been populated
    print("Dictionary of folders with list of links only:")
    ul.myprint_for_dict(bmk_links.link_dict)

    from utilities.bigGsearch import search
    #quick test on searching to match a pattern on a single page
    mys2_ok = search("site:https://it.wikipedia.org/wiki/Traglia_di_Jelsi pattini", stop=20)
    print(list(mys2_ok))


if __name__ == '__main__':
    uname = getpass.getuser()
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--pattern', help='string to match in the bookmarked pages')
    args = parser.parse_args()
    pattern = args.pattern
    main(uname, pattern)


