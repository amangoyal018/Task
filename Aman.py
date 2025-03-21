import requests
import urllib.parse
import time

# config file for api url and threshold value
CONFIG = {
    "v1": {
        "url": "http://35.200.185.69:8000/v1/autocomplete?query=",
        "threshold": 10,
        "allowed_chars": "abcdefghijklmnopqrstuvwxyz"
    },
    "v2": {
        "url": "http://35.200.185.69:8000/v2/autocomplete?query=",
        "threshold": 12,
        "allowed_chars": "abcdefghijklmnopqrstuvwxyz0123456789"
    },
    "v3": {
        "url": "http://35.200.185.69:8000/v3/autocomplete?query=",
        "threshold": 15,
        "allowed_chars": "abcdefghijklmnopqrstuvwxyz0123456789+-."
    }
}

#to provide list of names returned with current prefix
def get_names(prefix,url,requests_cnt):
    # URL-encode the prefix to convert '+' to '%2B'
    #so "a+" will be converted to "a%2B" and not "a"
    encoded_prefix = urllib.parse.quote(prefix, safe="")
    full_url = url + encoded_prefix
    
    try:
        response = requests.get(full_url);
        requests_cnt["count"] += 1
        if response.status_code == 200:
            data = response.json()
            if 'results' in data:
                return data['results']
            else:
                return []
        else:
            #particular prefix response status code
            print(f"Error: '{prefix}' returned status {response.status_code}")
            return []
    except requests.exceptions.RequestException as e:
        print(f"Request error for '{prefix}': {e}")
        return []

def extract_names(prefix, all_names,requests_cnt, url, threshold, characters):
    
    names = get_names(prefix,url,requests_cnt)
    
    #rate limiting as 100 words per minute
    time.sleep(0.6) 
    
    if len(names) >= threshold:
        
        #if prefix is present and threshold is reached then we will search for next prefix with allowed characters
        #so add it here only
        if prefix and prefix in names:
            print(prefix)
            all_names.add(prefix)
            
        for char in characters:
            new_prefix = prefix + char
            extract_names(new_prefix, all_names,requests_cnt, url, threshold, characters)
        return
            
    for name in names:
        print(name)
        all_names.add(name)



def main():
    for version,config in CONFIG.items():
        all_names = set()
        requests_cnt = {"count": 0}
        
        extract_names("", all_names,requests_cnt , config["url"], config["threshold"], config["allowed_chars"])
        
        print(len(all_names), "names found")
        print(requests_cnt["count"], "requests made in version ", version)    
    
    
if __name__ == "__main__":
    main()