import lxml
from firebase import firebase
FBConn = firebase.FirebaseApplication('https://dazzling-forest-311718-default-rtdb.firebaseio.com/', None)

import requests
from bs4 import BeautifulSoup


first = requests.get("https://wesleyan.cafebonappetit.com/cafe/the-marketplace-at-usdan/")
src0 = first.content
soup0 = BeautifulSoup(src0, 'lxml')

def get_menu():
    for a_tag in soup0.find_all('a', class_ = "hidden-small"):
        link = a_tag.attrs['href']
        #print(link)

    result = requests.get(link)
    src = result.content
    soup = BeautifulSoup(src, 'lxml')

    menu = [[]]
    daykey = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    statkey = {
        '4260' : "Stockpot",
        '445' : "Classics",
        '446' : "Vegan",
        '447' : "Kosher",
        '4262' : "Marketplace Grill",
        '448' : "Mongolian Grill",
        '698' : "Hearth Baked Pizza",
        '4535' : "Pastabilities",
        '699' :  "Cardinal Deli"

    }
    menu_counter = 1

    menu_dict = {
        "Monday" : [],
        "Tuesday" : [],
        "Wednesday" : [],
        "Thursday" : [],
        "Friday" : [],
        "Saturday" : [],
        "Sunday" : []

    }
    for div_tag in soup.find_all('div', class_ = "day cell_menu_item"):
        address = div_tag.attrs['id']
        address = address.split("-")
        val = int(address[2])
        address[2] = daykey[val]
        address[1] = statkey[address[1]]


        menu.append([address[1],address[2]])
        for item in div_tag.find_all('span', class_ = "weelydesc"):
            for char in item:
                if "topping" not in char:
                    if "request" not in char:
                        menu[menu_counter].append(char)
        menu_counter += 1

    del menu[0]

    for list in menu:
        for day in daykey:
            if list[1] == day:
                menu_dict[day].append(list)


    result =  FBConn.post('menu_items',menu_dict)
    print(result)
    # for line in menu:
    #     print(line)

get_menu()
