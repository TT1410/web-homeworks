# Примітивний веб-додаток із використанням технології **socket** у бекенді


1. Перейдіть у каталог із проектом, де знаходиться **Dockerfile**:

       cd D:/GoIT/web-homeworks/homework_4

2. Для створення образу введіть команду:

       docker build . -t hw-4

3. Для запуску контейнера введіть команду:

       docker run -itd --name container_hw-4 -p 3000:3000 -v ${PWD}/storage:/app/storage/ hw-4

4. Перейдіть за посиланням:

   http://localhost:3000/
