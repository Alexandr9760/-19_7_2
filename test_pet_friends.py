from api import PetFriends
from settings import valid_email, valid_password


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

def test_add_New_Pet_With_Valid_Data(self, name='Барбоскин', animal_type='двортерьер', age='4',
                                    pet_photo='images/P1040103.jpg'):
        pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
        _, auth_key = self.pf.get_api_key(valid_email, valid_password)
        status, result = self.pf.post_add_new_pet(auth_key, name, animal_type, age, pet_photo)
        assert status == 200
        assert result['name'] == name

def test_successful_Delete_Self_Pet(self):
        _, auth_key = self.pf.get_api_key(valid_email, valid_password)
        _, myPets = self.pf.get_list_of_pets(auth_key, "my_pets")

        if len(myPets['pets']) == 0:
            self.pf.post_add_new_pet(auth_key, "Суперкот", "кот", "3", "images/cat1.jpg")
            _, myPets = self.pf.get_list_of_pets(auth_key, "my_pets")

        pet_id = myPets['pets'][0]['id']
        status, _ = self.pf.delete_pet(auth_key, pet_id)
        _, myPets = self.pf.get_list_of_pets(auth_key, "my_pets")
        assert status == 200
        assert pet_id not in myPets.values()

def test_successful_Update_Self_Pet_Info(self, name='Мурзик', animal_type='Котэ', age='5'):
        _, auth_key = self.pf.get_api_key(valid_email, valid_password)
        _, myPets = self.pf.get_list_of_pets(auth_key, "my_pets")

        if len(myPets['pets']) > 0:
            status, result = self.pf.put_update_pet_info(auth_key, myPets['pets'][0]['id'], name, animal_type, age)
            assert status == 200
            assert result['name'] == name
        else:
            raise Exception("There is no my pets")




