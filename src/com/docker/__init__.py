from client import DockerClient


class RobotDocker(DockerClient):
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'