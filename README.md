# Avisa Aqui

Este projeto utiliza Django como tecnologia principal e também ambiente virtual para controle de dependências.

É um fórum de ocorrências voltado à cidade de Praia Grande, visando permitir que a comunidade possa se alertar à respeito de situações perigosas como roubo, furto, acidente, etc. O sistema permite cadastro de usuários, posts e comentários, além de disponibilizar uma api dos posts, utilizando-se das facilidades do Django Rest Framework. 

Este projeto foi realizado na FATEC PG apenas como trabalho disciplinar de conclusão de semestre, buscando testar o que foi passado durante esse tempo.

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
    * Djangorestframework (api)
        ```
        pip install djangorestframework
        ```
    * widget-tweaks (personalizar atributos dos elementos melhor)
        ```
        pip install django-widget-tweaks
        ``` 
* Rodar o projeto
    ```
    python3 manage.py runserver
    ```