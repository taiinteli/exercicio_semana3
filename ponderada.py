import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist, Point
from nav_msgs.msg import Odometry
from tf_transformations import euler_from_quaternion
from math import atan2

# Distância máxima permitida para que o robô considere que chegou em um ponto
MAX_DIFF = 0.15

# Lista de pontos que o robô deve percorrer
GOALS = [(0.5, 1.0),
         (2.0, 2.5),
         (4.0, 3.5),
         (6.0, 4.0),
         (5.0, 5.0),
         (3.5, 6.0),
         (2.0, 7.0),
         (1.0, 5.0)]


class RobotController(Node):
    def __init__(self, goals):
        super().__init__('robot_controller')
        
        # Inicializa as variáveis de posição e orientação do robô
        self.x, self.y, self.theta = 0.0, 0.0, 0.0
        
        # Inicializa a lista de pontos e o índice do ponto atual
        self.point_list = goals
        self.current_point_index = 0
        
        # Cria o publisher para enviar os comandos de velocidade
        self.publisher = self.create_publisher(Twist, '/cmd_vel', qos_profile=10)
        
        # Cria o subscription para receber as informações de odometria
        self.subscription = self.create_subscription(Odometry, '/odom', self.listener_callback, qos_profile=4)
        
        # Cria um timer para chamar a função publisher_callback a cada 0.02 segundos
        self.timer = self.create_timer(0.02, self.publisher_callback)

    def listener_callback(self, msg):
        # Atualiza as variáveis de posição e orientação do robô
        self.x = msg.pose.pose.position.x
        self.y = msg.pose.pose.position.y
        rot = msg.pose.pose.orientation
        _, _, self.theta = euler_from_quaternion([rot.x, rot.y, rot.z, rot.w])
        
        # Imprime as informações de posição do robô
        self.get_logger().info(f"x={self.x:3f}, y={self.y:3f}")

    def publisher_callback(self):
        # Obtém o ponto atual da lista de pontos
        goal = Point()
        goal.x = self.point_list[self.current_point_index][0]
        goal.y = self.point_list[self.current_point_index][1]
        
        # Calcula as distâncias em x e y entre o robô e o ponto atual
        inc_x = goal.x - self.x
        inc_y = goal.y - self.y
        
        # Calcula o ângulo necessário para que o robô se oriente em direção ao ponto atual
        angle_to_goal = atan2(inc_y, inc_x)
        
        # Cria a mensagem de velocidade a ser publicada
        speed = Twist()
        
        # Se a distância em x e y for menor que a distância máxima permitida,
        # o robô considera que chegou no ponto e passa para o próximo
        if abs(inc_x) < MAX_DIFF and abs(inc_y) < MAX_DIFF:
            self.current_point_index = (self.current_point_index + 1) % len(self.point_list)
            
        if abs(angle_to_goal - self.theta) > MAX_DIFF:
            speed.linear.x = 0.0
            speed.angular.z = 0.5 if angle_to_goal - self.theta > 0.0 else -0.5
        else:
            speed.linear.x = 0.3
            speed.angular.z = 0.0
        
        self.publisher.publish(speed)


def main(args=None):
    rclpy.init(args=args)
    robot_node = RobotController(GOALS)
    rclpy.spin(robot_node)
    robot_node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()