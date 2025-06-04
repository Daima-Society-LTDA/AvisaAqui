# Avisa Aqui

Este projeto utiliza Django como tecnologia principal e também ambiente virtual para controle de dependências.

### Como rodar

* Ter o python instalado, recomendado acima de 3.9;
* Criar o ambiente virtual
    * python3 -m venv ambienteVirtual
* Ativar o ambiente virtual
    * Windows
        * ambienteVirtual\Scripts\activate
    * Linux
        * source ambienteVirtual\bin\activate
* Instalar dependências
    * Django
        ```
        python3 -m pip install django
        ```
    * Pillow (biblioteca para trabalhar com imagens)
        ```
        python3 -m pip install pillow
        ```
* Rodar o projeto
    ```
    python3 manage.py runserver
    ```