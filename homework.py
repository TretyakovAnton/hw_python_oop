from dataclasses import dataclass
from typing import Dict, Type


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        """Вывод результата тренировки"""
        return ('Тип тренировки: {training_type}; '
                'Длительность: {duration:.3f} ч.; '
                'Дистанция: {distance:.3f} км; '
                'Ср. скорость: {speed:.3f} км/ч; '
                'Потрачено ккал: {calories:.3f}.'
                .format(training_type=self.training_type,
                        duration=self.duration,
                        distance=self.distance,
                        speed=self.speed,
                        calories=self.calories))


class Training:
    """Базовый класс тренировки."""

    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    MIN_IN_HOUR: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action: int = action
        self.duration: float = duration
        self.weight: float = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories()
                           )


class Running(Training):
    """Тренировка: бег."""

    index_calorie_1: int = 18
    index_calorie_2: int = 20

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        mean_speed: float = self.get_mean_speed()
        time_training_min: float = self.duration * self.MIN_IN_HOUR
        return ((self.index_calorie_1 * mean_speed
                 - self.index_calorie_2) * self.weight /
                 self.M_IN_KM * time_training_min)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    index_calorie_3: float = 0.035
    index_calorie_4: float = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height: float = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        part_1: float = self.index_calorie_3 * self.weight
        part_2: float = self.get_mean_speed() ** 2 // self.height
        part_3: float = self.index_calorie_4 * self.weight
        time_training_min: float = self.duration * self.MIN_IN_HOUR
        return (part_1 + part_2 * part_3) * time_training_min


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: float = 1.38
    index_calorie_5: float = 1.1
    index_calorie_6: float = 2.0

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool: float = length_pool
        self.count_pool: int = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        swam: float = self.length_pool * self.count_pool
        return swam / self.M_IN_KM / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        part_1: float = self.get_mean_speed() + self.index_calorie_5
        part_2: float = self.index_calorie_6 * self.weight
        return part_1 * part_2


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_dict: Dict[str, Type[Training]] = \
        {'SWM': Swimming,
         'RUN': Running,
         'WLK': SportsWalking}
    if training_dict.get(workout_type):
        return training_dict[workout_type](*data)
    else:
        return None


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [1206, 12, 6]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        if training is None:
            print('Данного типа тренировки нету')
        else:
            main(training)
