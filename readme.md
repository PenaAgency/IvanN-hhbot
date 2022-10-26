Бот для отклика на вакансии на hh.ru
=====
Запуск:
-----
    pip install -r requirements.txt
    python main.py -login login -password password \  
                   -letter_path letter_path -search_url search_url

login - Почта или телефон от аккаунта без +.  
password - Пароль от аккаунта.  
letter_path - Полный путь до файла с сопроводительным письмом.  
search_url - Url по которому будет искать вакансии. Обязатель в кавычках "".  
Как его получить: Заходите на hh.ru, выставляете фильтры, нажимаете поиск и копируете url.  


