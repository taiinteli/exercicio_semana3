# Introdução: Motivação e simulação de robôs com o Gazebo, ROS2 e um controlador python.
Objetivo principal: Ao implementar uma rota pré-estabelecida construída em python, o sistema armazena a lista de pontos que o robô fará para alcançar seu
 alvo, além de que há a possibilidade de interagir com os tópicos de velocidades e extrair dados de posicionamento e orientação (theta).

Componentes utilizados:

Gazebo, uma ferramenta muito eficaz dentro da simulação 3D que faz parte do ecossistema do ROS, seu ambiente virtual consegue ser preciso e fiel a realidade, nele é possível simular e testar diversos ambientes robôticos. 

O ROS2 (Robot Operating System 2), oferece um conjunto de ferramentas e bibliotecas e nos permitirá integrar todo o sistema operacional para termos um ambiente robótico. Para a instalação do framework o manual a seguir evidencia como instalar o ROS2 no Ubuntu Linux, lembre-se de colocar cada linha  de comando individualmente por vez: 
https://docs.ros.org/en/dashing/Installation/Ubuntu-Install-Binary.html  

Controlador em python, para a definição dos pontos que o robô irá percorrer, há uma lista de pontos predefinidos. O robô utiliza dados de odometria para atualizar sua posição e orientação (theta). E, sua velocidade é publicada a cada interação para controlar seus movimentos. Após cada interação, o controlador verifica se o TurtleBot(Buguer) está perto o suficiente do ponto atual da lista, caso não estiver ele gira em direção ao ponto. Assim que ele fica totalmente alinhado com o seu ponto “alvo”, ele se move até seu objetivo final de chegada. 
