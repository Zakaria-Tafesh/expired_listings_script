import csv
import os
import time
from zak_api_utils import *

City = 'Edmonton'
Area = 'AB'

PATH_THIS_FILE = os.path.realpath(__file__)
PATH_PARENT = os.path.abspath(os.path.dirname(__file__))
PATH_PARENT_PARENT = os.path.abspath(os.path.join(PATH_PARENT, os.pardir))

print(PATH_THIS_FILE)
print(PATH_PARENT)
print(PATH_PARENT_PARENT)

PATH_INPUT = os.path.join(PATH_PARENT_PARENT, 'input')
print(PATH_INPUT)


class CSVReader:
    def __init__(self, csv_path):

        self.csv_path = os.path.join(PATH_INPUT, csv_path)
        self.all_objects = []
        self.dataReader = None
        self.header = None

    def read_and_convert(self):
        self.read_csv()
        self.csv_to_objects()
        return self.all_objects

    def read_csv(self):
        start = time.time()
        print('Reading CSV', self.csv_path)
        self.dataReader = csv.reader(open(self.csv_path), delimiter=',', quotechar='"')
        self.header = next(self.dataReader, None)
        self.header = list(map(lambda item: str(item).replace(' ', '').replace('__', ''), self.header))
        print(f'Header : {self.header}')
        print(f'Done Reading CSV in {round((time.time() - start), 2)}')

    def csv_to_objects(self):
        start = time.time()
        print('Preparing Data (csv_to_objects)...')

        for row in self.dataReader:
            if not row:
                continue

            home_object = dict()
            for i in range(len(self.header)):
                if row[i]:
                    item = row[i]
                else:
                    item = None

                home_object[self.header[i]] = item

            self.all_objects.append(home_object)

        print(f'Time : {round((time.time() - start), 2)} Seconds')


class UpdateCSV(CSVReader):

    def __init__(self, csv_file):
        super().__init__(csv_file)

    def update_objects(self):
        for obj in self.all_objects:
            print('#'*30)
            address = obj.get('Address')
            if not address:
                continue
            addresses_dict = AddressesDetails.get_3_addresses_with_prices(address)

            print(f'addresses_dict: {addresses_dict}')
            print('#'*30)
            break

    @staticmethod
    def format_as_dollar(value):
        if value:
            value = int(value)
            value = "${:,}".format(value)
            return value
        return value


class AddressesDetails:
    # def __init__(self, address):
    address1 = ''
    address2 = ''
    address3 = ''
    addresses_prices = {
        'address1': {'address': ''
                     },
        'address2': {'address': ''
                     },
        'address3': {'address': ''
                     }
    }

    @classmethod
    def get_3_addresses_with_prices(cls, address):
        print(f'Start working on Addresses: {address}')
        cls.address1 = address + f', {City}, {Area}'
        cls.get_nearest_2_addresses()
        cls.get_estimates()
        return cls.addresses_prices

    @classmethod
    def get_nearest_2_addresses(cls):
        first_part = int(cls.address1.split()[0])
        other_parts = ' '.join(cls.address1.split()[1:])
        if first_part == 1:
            second = 2
            third = 3
        else:
            second = first_part + 1
            third = first_part - 1
        cls.address2 = f'{second} {other_parts}'
        cls.address3 = f'{third} {other_parts}'

        cls.addresses_prices['address1']['address'] = cls.address1
        cls.addresses_prices['address2']['address'] = cls.address2
        cls.addresses_prices['address3']['address'] = cls.address3

    @classmethod
    def get_estimates(cls):
        for address_num, address_dict in cls.addresses_prices.items():
            address = address_dict['address']
            print('#'*20)
            print(f'Getting estimate for {address}')
            resp = GetEstimateAPI.get_estimate(address)
            if resp.get('offer_price'):
                address_dict['offer_price'] = UpdateCSV.format_as_dollar(resp.get('offer_price'))
                address_dict['offer_price_90'] = UpdateCSV.format_as_dollar(resp.get('offer_price_90'))
            print('#'*20)

        print(cls.addresses_prices)
        return cls.addresses_prices


if __name__ == '__main__':

    Target_CSV = """Adam's_Custom_Spreadsheet.csv"""
    csv_obj = UpdateCSV(Target_CSV)
    csv_obj.read_and_convert()
    csv_obj.update_objects()

    # for obj in objs:
    #     print(obj)

