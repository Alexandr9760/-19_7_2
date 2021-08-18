import json.decoder

import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder

class PetFriends:
    def __init__(self):
        self.base_url = "https://petfriends1.herokuapp.com/"

    def get_api_key(self, email: str, password: str) -> json:
        """Метод выполняет запрос к API сервера и возвращает статус запроса и результат в формате JSON
         с уникальным ключём пользователя, найденного по указанным email и паролю"""
        headers = {
            'email': email,
            'password': password
        }
        res = requests.get(self.base_url+'api/key', headers=headers)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def get_list_of_pets(self, auth_key: json, filter: str = "") -> json:
        """Метод выполняет запрос к API сервера и возвращает статус запроса и результат в формате JSON
         со списком найденных питомцев, совпадающих с фильтром. На данный момент фильтр может иметь либо
         пустое значение - получить список всех питомцев, либо 'my_pets' - получить список собственных питомцев
         со списком найденных питомцев, совпадающих с фильтром."""
        headers = {'auth_key': auth_key['key']}
        filter = {'filter': filter}

        res = requests.get(self.base_url+'api/pets', headers=headers, params=filter)

        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        return status, result


    def post_add_new_pet(self, auth_key: json, name: str, animal_type: str, age: int, pet_photo: str) -> json:
        """Метод отправляет (постит) на сервер данные о добавляемом питомце и возвращает статус запроса на сервер и
        результат в формате JSON с данными добавленного питомца. Так как в этом методе для передачи используются
        данные как в формате json, так и в виде файла изображения — multipart-данные. Для решения этой проблемы применяем
        библиотеку requests_toolbelt. Из неё импортируем класс MultipartEncoder. При этом в заголовок
        необходимо передать формат данных объекта data в ключ Content-Type"""
        data = MultipartEncoder(
            fields={
                'name': name,
                'animal_type': animal_type,
                'age': age,
                'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpg')
            })
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}


        res = requests.post(self.base_url+'api/pets', headers=headers, data=data)


        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        print(result)
        return status, result


    def delete_pet(self, auth_key: json, pet_id: str) -> json:
        """Метод отправляет на сервер запрос на удаление питомца по указанному ID и возвращает статус запроса и
        результат в формате JSON с текстом уведомления о успешном удалении. На сегодняшний день тут есть баг -
        в result приходит пустая строка, но status при этом = 200."""
        headers = {'auth_key': auth_key['key']}

        res = requests.delete(self.base_url+'api/pets/'+pet_id, headers=headers)

        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def put_update_pet_info(self, auth_key: json, pet_id: str, name: str, animal_type: str, age: int) -> json:
        """Метод отправляет запрос на сервер об обновлении данных питомца по указанному ID и возвращает
        статус запроса и result в формате JSON с обновлённыи данными питомца"""
        headers = {'auth_key': auth_key['key']}
        data = {
            'name': name,
            'age': age,
            'animal_type': animal_type
        }

        res = requests.put(self.base_url + 'api/pets/' + pet_id, headers=headers, data=data)

        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def post_add_new_pet_without_photo(self, auth_key: json, name: str, animal_type: str, age: int) -> json:
        """метод, который добавляет нового питомца без фотографии, возвращает статус запроса, и result в формате JSON"""
        data = MultipartEncoder(
            fields={
                'name': name,
                'animal_type': animal_type,
                'age': age
            })
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}

        res = requests.post(self.base_url + 'api/create_pet_simple', headers=headers, data=data)

        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        print(result)
        return status, result


    def post_add_new_photo_of_pet(self, auth_key: json, pet_id: str, pet_photo: str) -> json:
        """метод, позволяющий загрузить фотографию питомца с соответствующим идентификатором питомца, возвращающим result в формате JSON"""
        data = MultipartEncoder(
            fields={
                'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpg')
            })
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}

        res = requests.post(self.base_url + 'api/pets/set_photo/' + pet_id, headers=headers, data=data)

        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        print(result)
        return status, result
