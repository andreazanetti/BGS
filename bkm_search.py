import argparse
import getpass
import utilities.url_utils as ul
import os


def report_on_data(bmk_links):
    # Todo: this should be a method
    print("...data about bookmarks obtained.")
    print(f"Number of links found: {len(bmk_links.link_list)}")
    # test for uniquess of links in the Bookmarks
    n_unique_links = len(set(i[0] for i in bmk_links.link_list))
    n_links = len(bmk_links.link_list)
    if n_links != n_unique_links:
        print(f"{n_links - n_unique_links} Duplicate links exists in your bookmarks!")
    else:
        print("There are no duplicate links! OK!")
    ask = input("\nDo you want to print the obtained links out? Y/N/How many? ")
    if str(ask).strip(' ') == 'Y':
        ul.myprint(bmk_links.link_list, N=n_links)
    elif (int(ask) > 0) and (int(ask) <= n_links):
        ul.myprint(bmk_links.link_list, N=int(ask))
    # Todo: do this well taking care of the N case....


def system_and_env_helper():
    '''
    Collects info about the system, platform and check/set env variables
    :return: list of proxy related env variables name
    '''
    # check and set env variables
    # get environment
    env_keys = os.environ.keys()
    # collect env variables related to proxy settings
    print("\n\n\nCurrent environment status relevant to proxy configuration is the following:\n")
    proxy_env_keys = [k for k in env_keys if ("PROXY" in k.upper()
                                            and "NO_PROXY" not in k.upper())]
    for k in proxy_env_keys:
        print(f"proxy related env variable {k} = {os.environ[k]}")
    proxy_choice = input("\n\nDo you want to use these proxy settings (Y) or you want to skip the proxy (S)?")
    # Todo: check input for correctness
    if proxy_choice.upper\
                () == 'S':
        for k in proxy_env_keys:
            del (os.environ[k])
        print("\nOK. Status of proxy environment variables has changed:\n")
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
    # print some info about the system and set env
    proxy_env_keys = system_and_env_helper()
    # identify bookmarks file, get it into a managable dict, report on the bookmarks status
    # Todo: check for data in input to be ok and deal with non-Mac cases
    bookmarks_file = username.join(['/Users/', '/Library/Application\ Support/Google/Chrome/Default/Bookmarks'])
    bookmarks_file = bookmarks_file.replace("\\", '')
    print(f"\nLooking into Bookmarks file: {bookmarks_file}")
    bmk_links = ul.get_Chrome_bookmarks_data(bookmarks_file)
    report_on_data(bmk_links)
    # Todo: user should input the pattern and the set of bookmarks folders to look into
    ul.do_search(bmk_links, pattern_sought=None, folder_list=None)
    # check dictionary has been populated
    # print("Dictionary of Bookmark folders with list of links only:")
    # ul.myprint_for_dict(bmk_links.link_dict)


if __name__ == '__main__':
    uname = getpass.getuser()
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--pattern', help='string to match in the bookmarked pages')
    args = parser.parse_args()
    pattern = args.pattern
    main(uname, pattern)


