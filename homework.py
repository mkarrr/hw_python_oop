from dataclasses import dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration_h: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        return str(f'Тип тренировки: {self.training_type}; '
                   f'Длительность: {self.duration_h:.3f} ч.; '
                   f'Дистанция: {self.distance:.3f} км; '
                   f'Ср. скорость: {self.speed:.3f} км/ч; '
                   f'Потрачено ккал: {self.calories:.3f}.')


@dataclass
class Training:
    """Базовый класс тренировки."""
    action: int
    duration_h: float
    weight: float
    M_IN_KM = 1000
    LEN_STEP = 0.65
    M_IN_H = 60

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        speed = self.get_distance() / self.duration_h
        return speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        message = InfoMessage(self.__class__.__name__,
                              self.duration_h,
                              self.get_distance(),
                              self.get_mean_speed(),
                              self.get_spent_calories())
        return message


class Running(Training):
    """Тренировка: бег."""
    coeff_calorie_1 = 18
    coeff_calorie_2 = 20

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        calories = ((self.coeff_calorie_1 * Training.get_mean_speed(self)
                    - self.coeff_calorie_2) * self.weight / Training.M_IN_KM
                    * self.duration_h * Training.M_IN_H)
        return calories


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    height: float
    coeff_calorie_3 = 0.035
    coeff_calorie_4 = 0.029

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        calories = ((self.coeff_calorie_3 * self.weight
                    + (Training.get_mean_speed(self) ** 2 // self.height)
                    * self.coeff_calorie_4 * self.weight)
                    * self.duration_h * Training.M_IN_H)
        return calories


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38
    coeff_calorie_5 = 1.1
    coeff_calorie_6 = 2
    length_pool: float
    count_pool: int

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        speed = (self.length_pool * self.count_pool / Training.M_IN_KM
                 / self.duration_h)
        return speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        calories = ((self.get_mean_speed() + self.coeff_calorie_5)
                    * self.coeff_calorie_6
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
