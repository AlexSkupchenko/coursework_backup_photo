import requests
import json
import os
from tqdm import tqdm

def main():
    
    class VK_user:
        
        def __init__(self, access_token, version='5.131'):
            self.token = access_token
            self.version = version
            self.params = {'access_token': self.token,
                           'v': self.version
                        }
        
        def photos_get(self, owner_id):
            photos_url = 'https://api.vk.com/method/photos.get'
            photos_params = {'owner_id': owner_id,
                            'album_id': 'profile',
                            'count': '5',
                            'extended': '1',
                            'photo_sizes': '1',
                            **self.params
                            }
            
            if not os.path.exists('Photos_VK'):
                os.mkdir('Photos_VK')
            
            photos_list = requests.get(photos_url, params={**self.params, **photos_params}).json()['response']['items'][-5:]
            photos_info = []
            for photo in tqdm(photos_list, desc='Processing'):
                # for i in tqdm(photos_list, desc='Processing'):
                info = {"file_name": str(photo['likes']['count']) + ".jpg",
                        "size": photo['sizes'][-1]['type']
                        }
                photos_info.append(info)
                file_url = photo['sizes'][-1]['url']
                filename = photo['likes']['count']
                resp = requests.get(file_url)
            
                with open("Photos_VK/%s" % filename, "wb") as file:
                    file.write(resp.content)
                
            with open("vk_photos_info.json", "w") as file:
                json.dump(photos_info, file)
    
    class YaUploader:
        def __init__(self, token: str):
            self.token = token
            self.url = 'https://cloud-api.yandex.net/v1/disk/resources'
            self.headers = {'Content-Type': 'application/json',
                            'Accept': 'application/json',
                            'Authorization': f'OAuth {self.token}'
                            }

        def folder_creation(self):
            params = {'path': f'{folder_name}',
                      'overwrite': 'false'}
            res = requests.put(url=self.url, headers=self.headers, params=params)
        
        def upload(self, file_path: str):
            params = {'path': f'{folder_name}/{file_name}',
                      'overwrite': 'true'}
            response = requests.get(url=self.url + "/upload", headers=self.headers, params=params)
            href = response.json().get('href')            
            upload = requests.put(href, data=open(files_path, 'rb'))
    
    access_token = '...'
    user_id = '...'
    user_vk_up = VK_user(access_token)
    user_vk_up.photos_get(user_id)

    Yadisk_token = '...'
    ya_user_up = YaUploader(Yadisk_token)
    folder_name = 'Photos'
    ya_user_up.folder_creation()

    photos_list = os.listdir('Photos_VK')
    for photo in tqdm(photos_list, desc='Processing'):
        file_name = photo
        files_path = os.getcwd() + '\Photos_VK\\' + photo
        res = ya_user_up.upload(files_path)

if __name__ == '__main__':
    main()