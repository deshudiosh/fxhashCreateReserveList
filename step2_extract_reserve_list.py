import json
from collections import Counter, OrderedDict


def extract():
    content = json.load(open('results.json'))
    # content = content['user']['generativeTokens'][0]['entireCollection'][0]["owner"]["id"]
    owners = []
    minters = []
    for gentk in content['user']['generativeTokens']:
        for entry in gentk["entireCollection"]:
            owner = entry['owner']['id']
            owners.append(owner)

            minter = entry['minter']['id']
            minters.append(minter)

    owners = Counter(owners)
    owners = OrderedDict(owners.most_common())

    minters = Counter(minters)
    minters = OrderedDict(minters.most_common())

    reserve_list = []

    for wallet, count in owners.items():
        if count >= 3:
            reserve_list.append(wallet)

    for wallet, count in minters.items():
        if count >= 5:
            reserve_list.append(wallet)

    # print(len(reserve_list))
    reserve_list = Counter(reserve_list)
    print(len(reserve_list))

    f = open("reserve_list.csv", "w")
    f.write("address, amount\n")
    [f.write(wallet + ", 1\n") for wallet in reserve_list]
    f.close()



if __name__ == '__main__':
    extract()
