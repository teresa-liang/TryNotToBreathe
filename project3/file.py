import json
import sys

def data_from_file(file: str) -> dict| list:
    '''Given a file name containing the result of a previous call to an api (either Nominatim or PurpleAir),
    returns the result in json format'''
    try:
        with open(file, encoding="utf-8") as f:
            lines = f.read()
            obj = json.loads(lines)

            return obj
    except FileNotFoundError:
        _print_failure(file)
        print('MISSING')
        sys.exit()
    except json.decoder.JSONDecodeError:
        _print_failure(file)
        print('FORMAT')
        sys.exit()
    except:
        # execute if the file could not be opened
        _print_failure(file)
        print('MISSING')
        sys.exit()

def _print_failure(file: str) -> None:
    '''Lets the user know that the file could not be fetched'''
    print('FAILED')
    print(file)
