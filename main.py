import sys
import os.path
from telethon import TelegramClient, sync
from telethon.tl.functions.contacts import ImportContactsRequest
from telethon.tl.types import InputPhoneContact

import private_constants

# TODO investigate limitations of Telegram API regarding importing contacts
from PhoneNumber import PhoneNumber


def check_telegram(phone_number_list):
    with TelegramClient('detect', private_constants.TELEGRAM_API_ID, private_constants.TELEGRAM_API_HASH) as client:
        input_contact_list = []
        for phone_number in phone_number_list:
            input_contact_list.append(
                InputPhoneContact(client_id=0, phone=phone_number.get_phone_number(), first_name=phone_number.get_phone_number(), last_name='cba'))
        client(ImportContactsRequest(input_contact_list))
        for phone_number in phone_number_list:
            try:
                contact = client.get_input_entity(phone_number.get_phone_number())
                phone_number.set_telegram(contact.user_id > 0)

            except ValueError:
                # TODO Use an error logger
                phone_number.set_telegram(False)
    return phone_number_list


def create_phone_numbers(arguments):
    #Currently the proccessing of numbers to objects is sensitive. Meaning that empty and invalid lines might get processed into an objects, which obviously shouldn't. Bear that in mind
    phone_number_list = []
    if os.path.isfile(arguments[1]):
        with open(arguments[1]) as file:
            for line in file:
                phone_number_list.append(PhoneNumber(line.strip('\n')))
    else:
        phone_number_list.append(arguments[1:])
    #TODO Check if list is empty and provide warning
    return phone_number_list


def main():
    phone_number_list = create_phone_numbers(sys.argv)
    check_telegram(phone_number_list)
    for number in phone_number_list:
        print(number)


if __name__ == "__main__":
    main()