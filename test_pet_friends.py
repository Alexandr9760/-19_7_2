from api import PetFriends
from settings import valid_email, valid_password, incorrect_password, incorrect_email, unlisted_ID
import os.path

pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result

def test_get_all_pets_with_valid_key(filter=''):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0

def test_add_New_Pet_With_Valid_Data(name='Барбоскин', animal_type='двортерьер', age='4',
                                    pet_photo='images/P1040103.jpg'):
        pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
        _, auth_key = pf.get_api_key(valid_email, valid_password)
        status, result = pf.post_add_new_pet(auth_key, name, animal_type, age, pet_photo)
        assert status == 200
        assert result['name'] == name

def test_successful_Delete_Self_Pet():
        _, auth_key = pf.get_api_key(valid_email, valid_password)
        _, myPets = pf.get_list_of_pets(auth_key, "my_pets")

        if len(myPets['pets']) == 0:
            pf.post_add_new_pet(auth_key, "Суперкот", "кот", "3", "images/cat1.jpg")
            _, myPets = self.get_list_of_pets(auth_key, "my_pets")

        pet_id = myPets['pets'][0]['id']
        status, _ = pf.delete_pet(auth_key, pet_id)
        _, myPets = pf.get_list_of_pets(auth_key, "my_pets")
        assert status == 200
        assert pet_id not in myPets.values()

def test_successful_Update_Self_Pet_Info(name='Мурзик', animal_type='Котэ', age='5'):
        _, auth_key = pf.get_api_key(valid_email, valid_password)
        _, myPets = pf.get_list_of_pets(auth_key, "my_pets")

        if len(myPets['pets']) > 0:
            status, result = pf.put_update_pet_info(auth_key, myPets['pets'][0]['id'], name, animal_type, age)
            assert status == 200
            assert result['name'] == name
        else:
            raise Exception("There is no my pets")

def test_get_api_key_for_invalid_password(email=valid_email, password=incorrect_password):
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result

def test_add_new_pet_with_invalid_file_format(name='Мурзик', animal_type='кот', age='3', pet_photo='images/cat2.docx'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.post_add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 500

def test_get_api_key_with_nothing (email=None, password=None):
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result

def test_add_new_pet_with_unintended_info(name='Мурзик', animal_type='кот', age='маленький', pet_photo='images/P1040103.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, result = pf.post_add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert result['age'] == age

def test_get_api_key_without_email (email=None, password=valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result

def test_get_api_key_for_invalid_email(email=incorrect_email, password=valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result

def test_add_pet_with_digital_name(name=12396004, animal_type='cat', age=2, pet_photo='images/cat1.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, result = pf.post_add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert result['name'] == name

def test_add_pet_with_empty_info(name=None, animal_type=None, age=None, pet_photo=None):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, _ = pf.post_add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 400

def test_delete_unlisted_pet(pet_id=unlisted_ID):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, myPets = pf.get_list_of_pets(auth_key, "my_pets")
    _, result = pf.delete_pet(auth_key, pet_id)
    assert pet_id not in myPets.values()
    assert 'pet id' not in result





