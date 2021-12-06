from dataclasses import dataclass
from typing import ClassVar


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        return str(f'Тип тренировки: {self.training_type}; '
                   f'Длительность: {self.duration:.3f} ч.; '
                   f'Дистанция: {self.distance:.3f} км; '
                   f'Ср. скорость: {self.speed:.3f} км/ч; '
                   f'Потрачено ккал: {self.calories:.3f}.')


@dataclass
class Training:
    """Базовый класс тренировки."""
    action: int
    duration: float
    weight: float
    M_IN_KM: ClassVar[int] = 1000
    LEN_STEP: ClassVar[float] = 0.65
    M_IN_H: ClassVar[int] = 60

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        speed = self.get_distance() / self.duration
        return speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        message = InfoMessage(self.__class__.__name__,
                              self.duration,
                              self.get_distance(),
                              self.get_mean_speed(),
                              self.get_spent_calories())
        return message


class Running(Training):
    """Тренировка: бег."""
    COEFF_CALORIE_1: ClassVar[int] = 18
    COEFF_CALORIE_2: ClassVar[int] = 20

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        calories = ((self.COEFF_CALORIE_1 * Training.get_mean_speed(self)
                    - self.COEFF_CALORIE_2) * self.weight / Training.M_IN_KM
                    * self.duration * Training.M_IN_H)
        return calories


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    height: float
    COEFF_CALORIE_3: ClassVar[float] = 0.035
    COEFF_CALORIE_4: ClassVar[float] = 0.029

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        calories = ((self.COEFF_CALORIE_3 * self.weight
                    + (Training.get_mean_speed(self) ** 2 // self.height)
                    * self.COEFF_CALORIE_4 * self.weight)
                    * self.duration * Training.M_IN_H)
        return calories


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: ClassVar[float] = 1.38
    COEFF_CALORIE_5: ClassVar[float] = 1.1
    COEFF_CALORIE_6: ClassVar[int] = 2
    length_pool: float
    count_pool: int

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        speed = (self.length_pool * self.count_pool / Training.M_IN_KM
                 / self.duration)
        return speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        calories = ((self.get_mean_speed() + self.COEFF_CALORIE_5)
                    * self.COEFF_CALORIE_6
                    * self.weight)
        return calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    trn_type = {'SWM': Swimming, 'RUN': Running, 'WLK': SportsWalking}

    if workout_type in trn_type:
        return trn_type.get(workout_type)(*data)
    raise KeyError('Несуществующий тип тренировки')


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    return print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
