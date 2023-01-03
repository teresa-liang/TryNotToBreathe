import json
import sys
import urllib.parse
import urllib.request

def get_result(url: str) -> dict:
    '''
    This function takes a URL and returns a Python dictionary representing the
    parsed JSON response.
    '''
    response = None

    try:
        request = urllib.request.Request(url, headers = {'Referer' : 'https://www.ics.uci.edu/~thornton/ics32/ProjectGuide/Project3/liangth1@uci.edu'}, method = 'GET')
        response = urllib.request.urlopen(request)
        json_text = response.read().decode(encoding = 'utf-8')

        return json.loads(json_text)
    except urllib.error.HTTPError as e:
        _print_failure(e, url)
        if e.code != None:
            print('NOT 200')
        else:
            print('NETWORK')
        sys.exit()
    except json.decoder.JSONDecodeError as e:
        _print_failure(e, url)
        print('FORMAT')
        sys.exit()
    finally:
        if response != None:
            response.close()

def _print_failure(error: str, url: str) -> None:
    '''Lets the user know that the api call failed'''
    print('FAILED')
    print(str(error.code), url)
