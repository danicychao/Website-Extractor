import sys
import urllib.request as req
import requests
import bs4
from urllib.parse import urljoin
import re
import phonenumbers


def crawl_headerway(url):
    opener = req.build_opener()
    opener.addheaders = [('User-Agent', 'MyApp/1.0')]
    #opener.addheaders = [('User-Agent', 'Mozilla/5.0')]
    req.install_opener(opener)
    request = req.Request(url)

    with req.urlopen(request) as response:
        data=response.read().decode('utf-8')
        
    return data


def crawl_sessionway(url):
    session_obj = requests.Session()
    response = session_obj.get(url, headers={'User-Agent': 'MyApp/1.0'})
    
    if response.status_code == 200:
        data = response.text
        
    else:
        print(f"Failed to receive a HTML response. Response status code: {response.status_code}")
        return 0
    
    return data


def extract_ImageUrl(data):
    
    '''
    First, parse the html.
    Second, find all the tags with "img".
    Third, find all img tags with "src", a url.
    Fourth, guess the src/url including "logo" or "Logo" as the logo url.
    '''
    
    root=bs4.BeautifulSoup(data, "html.parser")
    potential_img_tags = root.find_all('img')
    
    logo_url = 'None'
    
    if len(potential_img_tags) == 0:
        return None

    for img_tag in potential_img_tags:
        if 'src' in img_tag.attrs:
            if 'logo' in (img_tag['src']):
                logo_url = urljoin(url, img_tag['src'])
                break
            elif 'Logo' in (img_tag['src']):
                logo_url = urljoin(url, img_tag['src'])
                break
                
    return logo_url


def extract_PhoneNumber(data, pattern, country=True):
    
    phone_pattern = pattern
    
    # Find all potential phone numbers in the HTML
    potential_phone_numbers = re.findall(phone_pattern, data)
    valid_phone_numbers = []
    
    for number in potential_phone_numbers:
        # Cleanup in order to remove any character that is not a number, plus sign or parenthesis
        cleaned = re.sub(r'[^0-9+()]', '', number)
        
        try:
            '''
            Validate the potential phone numbers to filter out only the good ones
            Note: in order that the phone number is valid, it must start with the correct country code
            which is a prerequirement as otherwise every seqnece of numbers could be a potential phone number (e.g. even the postal code)
            '''
            if country:
                parsed_number = phonenumbers.parse(cleaned, None)
            
            # Push the cleaned phone number from the HTML to the array of validated phone numbers
            valid_phone_numbers.append(cleaned)
            
        except Exception:
            continue
            
    return valid_phone_numbers



url=sys.argv[1]
data = crawl_headerway(url)
#data = crawl_sessionway(url)


if data != 0:
    
    logo_url = extract_ImageUrl(data)
    
    ''' 
    Regular expression pattern to find all potential phone numbers with country code
    Match sequences that have the following pattern: 
        - can start with plus sign
        - must contain at least 4 characters
        - characters can be digits, parentheses, slashes, periods, spaces, or hyphen
        - must end with a digit
    '''
    
    phone_pattern_standard = r'\+?[0-9()/. -]{4,}\d'
    valid_phone_numbers = extract_PhoneNumber(data, phone_pattern_standard)            
                        
    # Valid phone numbers
    if len(valid_phone_numbers) != 0:
        print(','.join(valid_phone_numbers))
    else:
        ''' 
        Regular expression pattern to find all potential phone numbers without country code
        Match sequences that have the following pattern: 
            - must start with left bracket sign
            - inside the brackets must contain at least 1 digit
            - must contain at least 4 characters after the brackets
            - characters can be digits, parentheses, slashes, periods, spaces, or hyphen
            - must end with a digit
        '''
        
        phone_pattern_NoCountry = r'\([0-9]{1,}\)[0-9()/. -]{4,}\d'
        valid_phone_numbers_2nd = extract_PhoneNumber(data, phone_pattern_NoCountry, country=False) 
        if len(valid_phone_numbers_2nd) != 0:
            print(','.join(valid_phone_numbers_2nd))
        else:
            ''' 
            Regular expression pattern to find all potential phone numbers in 0800 non-paid phone calls
            Match sequences that have the following pattern: 
                - must start with 0800
                - must contain at least 4 characters after 0800
                - characters can be digits, parentheses, slashes, periods, spaces, or hyphen
                - must end with a digit
            '''
            
            phone_pattern_Free = r'0800[0-9()/. -]{4,}\d'
            valid_phone_numbers_3rd = extract_PhoneNumber(data, phone_pattern_Free, country=False)
            
            if len(valid_phone_numbers_3rd) !=0:
                print(','.join(valid_phone_numbers_3rd))
            
            else:
                print('None')

    # Image url
    print(logo_url)