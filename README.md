# Курсовая работа
Работу выполнил Кильчуков Т. М3О-312Б-18.
  
### Постановка задачи
1. Скачать и установить веб-сервер.  
2. Настроить его на работу с localhost  
3. Реализовать форму с загрузкой файла  
4. Захостить python приложение из предыдущего семестра, при загрузке снимка рисовать в веб карту NDVI.  
  
## Ход выполнения работы:  
Работа выполненена на CentOS 7.
  
### 1. Cоздание рабочей директории и установка необходимых пакетов.

    [tkilch@localhost ~]$ mkdir ~/isak_project
    [tkilch@localhost ~]$ cd ~/isak_project
    [tkilch@localhost isak_project]$ sudo yum groupinstall "Development Tools"
    [tkilch@localhost isak_project]$ sudo yum install python-pip python-devel gcc nginx  

### 2. Создание приложения на Flask.  
Установим uwsgi и flask:  

    [tkilch@localhost isak_project]$ pip install uwsgi flask  

Создадим приложение Flask:  

    [tkilch@localhost isak_project]$ vim ~/isak_project/application.py  
Сохраним и закроем файл и сохраним его с помощью ":wq".  
  
### 3. Создание точки входа WSGI.  
Создадим файл wsgi.py:  

    [tkilch@localhost isak_project]$ vim ~/isak_project/wsgi.py  
Внутри напишем:  

    from isak_project import application  
    if __name__ == "__main__":  
      application.run()  
  
### 4. Настройка uWSGI.  
Протестируем uWSGI:  

    [tkilch@localhost isak_project]$ uwsgi --socket 0.0.0.0:8000 --protocol=http -w wsgi &   

После этого остановим uwsgi.

    [tkilch@localhost isak_project]$ fg  
    uwsgi --socket 0.0.0.0:8000 --protocol=http -w wsgi
    ^C  
Создадим файл конфигурации uWSGI:  

    [tkilch@localhost isak_project]$ vim ~/isak_project/isak_project.ini  
Введем следующее:  

    [uwsgi]  
    module = wsgi  
    master = true  
    socket = isak_project.sock  
    chmod-socket = 660  
      
### 5. Создание службы systemd.  
Создадим файл isak_project.service:  

    [tkilch@localhost isak_project]$ sudo vim /etc/systemd/system/isak_project.service  
Введем следующее: 

    [Unit]  
    Description=uWSGI for isak_project  
    After=network.target  
    [Service]  
    User=tkilch  
    Group=nginx  
    WorkingDirectory=/home/tkilch/isak_project  
    ExecStart=/home/tkilch/isak_project/uwsgi --ini isak_project.ini  
    [Install]  
    WantedBy=multi-user.target 

Запустим созданную службу:  
    
    [tkilch@localhost isak_project]$ sudo systemctl start isak_project  
    [tkilch@localhost isak_project]$ sudo systemctl enable isak_project  
      
### 6. Настроим серверный блок Nginx.  
Необходимо настроить Nginx для передачи веб-запросов в  сокет с использованием uWSGI протокола.  
Откроем файл конфигурации:  

    [tkilch@localhost isak_project]$ sudo vim /etc/nginx/nginx.conf  
Найдем блок server в теле http, выше него создадим свой:  

    server {  
      listen 80;  
      server_name 10.0.2.15;  
      
      location / {
        include uwsgi_params;
        uwsgi_pass unix:/home/tkilch/isak_project/isak_project.sock;
    }
Сохраним файл и закроем его.  
Добавим nginx пользователя в свою группу пользователей:  

    [tkilch@localhost isak_project]$ sudo usermod -a -G tkilch nginx  
Предоставим группе пользователей права на выполнение в домашнем каталоге:  

    [tkilch@localhost isak_project]$ chmod a+rwx /home/tkilch  
Запустим Nginx:  

    [tkilch@localhost isak_project]$ sudo systemctl start nginx  
    [tkilch@localhost isak_project]$ sudo systemctl enable nginx  

Для того, чтобы убедиться что сайт работает восполлзуемся командой curl:

    [tkilch@localhost isak_project]$ curl -L 10.0.2.15:80

Увидим следующий вывод в терминал:  

    <head>
      <title>NDVI</title>
    </head>
    <body>
      <p>Загрузите изображения в формате tif для красного и инфракрасного спектров Landsat 7:</p>
          <form method="POST" action="" enctype="multipart/form-data">
            <div>
              <input type="file" name="file" id="file-button" accept=".tif" multiple />
            </div>
            <br>
            <div>
              <input type="submit" id="file-submit" class="submitfile" />
            <br/>
            </div>
          </form>
    </html>
  
# Вывод:  
В ходе выполнения курсовой работы было создано python приложение для работы с Flask, позволяющее загружать и обрабатывать изображения спектров в формате ".tif" и выводить пользователю цветное изображение NDVI. 
Была создана и настроена точка входа WSGI, служба systemd и серверный блок Nginx. 
