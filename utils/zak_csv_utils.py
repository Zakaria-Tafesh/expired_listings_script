import copy
import csv
import os
import time
from .zak_api_utils import *
from .logger import logger, get_datetime_now

# Edit below
City = 'Edmonton'
Area = 'AB'

CSV_COLUMN_ADDRESS = 'Address'
CSV_COLUMN_POSTALCODE = 'Postal Code'
# Edit above

PATH_THIS_FILE = os.path.realpath(__file__)
PATH_PARENT = os.path.abspath(os.path.dirname(__file__))
PATH_PARENT_PARENT = os.path.abspath(os.path.join(PATH_PARENT, os.pardir))

logger.info(PATH_THIS_FILE)
logger.info(PATH_PARENT)
logger.info(PATH_PARENT_PARENT)

PATH_INPUT = os.path.join(PATH_PARENT_PARENT, 'input')
PATH_OUTPUT = os.path.join(PATH_PARENT_PARENT, 'output')

logger.info(PATH_INPUT)


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
        logger.info(f'Reading CSV: {self.csv_path}')
        self.dataReader = csv.reader(open(self.csv_path), delimiter=',', quotechar='"')
        self.header = next(self.dataReader, None)
        self.header = list(map(lambda item: str(item).strip(), self.header))
        logger.info(f'Header : {self.header}')
        logger.info(f'Done Reading CSV in {round((time.time() - start), 2)}')

    def csv_to_objects(self):
        start = time.time()
        logger.info('Preparing Data (csv_to_objects)...')

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

        logger.info(f'Time : {round((time.time() - start), 2)} Seconds')


class UpdateCSV(CSVReader):

    def __init__(self, csv_file, add_to_output, add_datetime_to_output):
        super().__init__(csv_file)
        self.new_objects = []
        self.input_name = csv_file
        self.add_to_output = add_to_output
        self.add_datetime_to_output = add_datetime_to_output
        self.output_header = []

    def update_objects(self):
        print('update_objects')
        for i, obj in enumerate(self.all_objects):
            time.sleep(2)
            print(obj)
            logger.info('#'*50 + f'{i + 1}/{len(self.all_objects)}')
            address = obj.get(CSV_COLUMN_ADDRESS)
            if not address:
                continue
            addresses_dict = AddressesDetails.get_3_addresses_with_prices(address)
            logger.info(f'addresses_dict : {addresses_dict}')

            new_3_objs = self.get_3_objects(obj, addresses_dict)
            logger.info(f'addresses_dict :: {addresses_dict}')

            self.new_objects.extend(new_3_objs)

            logger.info('#'*50)

        logger.info(self.new_objects)
        self.get_output_header()

    def write_objects(self):
        output_name = self.prepare_output_name()
        logger.info(f'Writing to CSV... : {output_name}')
        with open(output_name, 'w', encoding='UTF8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=self.output_header)
            writer.writeheader()
            writer.writerows(self.new_objects)
        logger.info('CSV Wrote Successfully.')

    def get_output_header(self):
        self.output_header = max(list(map(lambda x: (len(x), x), self.new_objects)), key=lambda i: i[0])[1].keys()
        return self.output_header

    def prepare_output_name(self):
        input_name = self.input_name
        first_part = input_name.split('.')[0]  # remove .csv
        second_part = self.add_to_output if self.add_to_output else ''
        third_part = get_datetime_now() if self.add_datetime_to_output else ''
        last_part = '.csv'
        output_name = f'{first_part}_{second_part}_{third_part}{last_part}'
        output_path = os.path.join(PATH_OUTPUT, output_name)
        return output_path

    @staticmethod
    def get_3_objects(obj: dict, addresses_dict: dict) -> list:
        old_keys = obj.keys()
        the_3_objs = []
        addresses_dict = copy.deepcopy(addresses_dict)

        first_obj = copy.deepcopy(obj)
        first_obj['offer_price'] = addresses_dict['address1']['offer_price']
        first_obj['offer_price_90'] = addresses_dict['address1']['offer_price_90']

        print(first_obj, type(first_obj))

        the_3_objs.append(first_obj)
        del addresses_dict['address1']
        for key, val in addresses_dict.items():
            new_obj = dict.fromkeys(old_keys, '')
            new_obj[CSV_COLUMN_ADDRESS] = val['address']
            new_obj['offer_price'] = val['offer_price']
            new_obj['offer_price_90'] = val['offer_price_90']

            new_obj[CSV_COLUMN_POSTALCODE] = first_obj[CSV_COLUMN_POSTALCODE]

            the_3_objs.append(new_obj)

        return the_3_objs

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
    address1_for_search = ''
    address2_for_search = ''
    address3_for_search = ''

    addresses_prices = {
        'address1': {'address': '',
                     'address_for_search': ''
                     },
        'address2': {'address': '',
                     'address_for_search': ''
                     },
        'address3': {'address': '',
                     'address_for_search': ''
                     }
    }

    @classmethod
    def get_3_addresses_with_prices(cls, address):
        logger.info(f'Start working on Addresses: {address}')
        cls.address1 = address
        cls.address1_for_search = address + f', {City}, {Area}'
        logger.info(f'address1: {cls.address1}')
        logger.info(f'address1_for_search: {cls.address1_for_search}')
        cls.get_nearest_2_addresses()
        cls.get_estimates()
        return cls.addresses_prices

    @classmethod
    def get_nearest_2_addresses(cls):
        logger.info(f'address1_for_search: {cls.address1_for_search}')

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
        cls.address2_for_search = cls.address2 + f', {City}, {Area}'
        cls.address3_for_search = cls.address3 + f', {City}, {Area}'

        cls.addresses_prices['address1']['address'] = cls.address1
        cls.addresses_prices['address1']['address_for_search'] = cls.address1_for_search
        cls.addresses_prices['address2']['address'] = cls.address2
        cls.addresses_prices['address2']['address_for_search'] = cls.address2_for_search
        cls.addresses_prices['address3']['address'] = cls.address3
        cls.addresses_prices['address3']['address_for_search'] = cls.address3_for_search

    @classmethod
    def get_estimates(cls):
        for address_num, address_dict in cls.addresses_prices.items():
            address = address_dict['address_for_search']
            logger.info('#'*20)
            logger.info(f'Getting estimate for {address}')
            resp = GetEstimateAPI.get_estimate(address)
            logger.info(f'resp:: {resp}')
            if resp.get('offer_price'):
                logger.info(resp.get('offer_price'))
                address_dict['offer_price'] = UpdateCSV.format_as_dollar(resp.get('offer_price'))
                address_dict['offer_price_90'] = UpdateCSV.format_as_dollar(resp.get('offer_price_90'))
            else:
                address_dict['offer_price'] = ''
                address_dict['offer_price_90'] = ''
            logger.info('#'*20)

        logger.info(cls.addresses_prices)
        return cls.addresses_prices


# if __name__ == '__main__':
#     Target_CSV = """Adam's_Custom_Spreadsheet.csv"""
#     ADD_TO_OUTPUT = """_Complete"""
#     ADD_DATETIME_TO_OUTPUT = True
#     csv_obj = UpdateCSV(Target_CSV, ADD_TO_OUTPUT, ADD_DATETIME_TO_OUTPUT)
#
#     csv_obj.read_and_convert()
#     csv_obj.update_objects()
#     csv_obj.write_objects()
#

