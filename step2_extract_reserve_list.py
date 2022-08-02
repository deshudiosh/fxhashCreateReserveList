import dataclasses
import json
from collections import Counter, OrderedDict


@dataclasses.dataclass
class Objkt:
    owner_id: str
    owner_name: str
    minter_id: str
    minter_name: str


def get_objkts():
    content = json.load(open('results.json'))

    objkts = []

    for GenerativeToken in content['user']['generativeTokens']:
        for entry in GenerativeToken["entireCollection"]:
            owner_id = entry['owner']['id']
            owner_name = entry['owner']['name']

            minter_id = entry['minter']['id']
            minter_name = entry['minter']['name']

            objkts.append(Objkt(owner_id, owner_name, minter_id, minter_name))

    return objkts


def print_reserve_list_names(reserve_list, objkts):
    print(f"----- Reserve list names:")
    names = []
    for id in reserve_list:
        for objkt in objkts:
            name = None
            if id == objkt.owner_id:
                name = objkt.owner_name
            if id == objkt.minter_id:
                name = objkt.minter_name

            if name:
                break

        if not name:
            name = id

        names.append(name)

    print(names)

    with open("reserve_list_names.txt", "w") as f:
        json.dump(names, f, indent=4)


def save_reserve_list():
    objkts = get_objkts()

    owners = []
    minters = []

    for objkt in objkts:
        owners.append(objkt.owner_id)
        minters.append(objkt.minter_id)

    owners = OrderedDict(Counter(owners).most_common())
    minters = OrderedDict(Counter(minters).most_common())

    reserve_list = []

    for wallet, count in owners.items():
        if count >= 3:
            reserve_list.append(wallet)

    for wallet, count in minters.items():
        if count >= 5:
            reserve_list.append(wallet)

    reserve_list = Counter(reserve_list)

    f = open("reserve_list.csv", "w")
    f.write("address,amount\n")
    [f.write(wallet + ",1\n") for wallet in reserve_list]
    f.close()

    print_reserve_list_names(reserve_list, objkts)


if __name__ == '__main__':
    save_reserve_list()
