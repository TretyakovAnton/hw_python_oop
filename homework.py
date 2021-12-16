class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type};'
                f' Длительность: {self.duration:.3f} ч.;'
                f' Дистанция: {self.distance:.3f} км;'
                f' Ср. скорость: {self.speed:.3f} км/ч;'
                f' Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    M_IN_KM: int = 1000
    LEN_STEP: float = 0.65
    coeff_clr_1: int = 18
    coeff_clr_2: int = 20

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

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
        part_1 = self.coeff_clr_1 * self.get_mean_speed() - self.coeff_clr_2
        part_2 = self.weight / self.M_IN_KM * self.duration * 60
        calories = part_1 * part_2
        return calories

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
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float
                 ) -> None:
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        part_1 = (self.coeff_clr_1 * self.get_mean_speed() - self.coeff_clr_2)
        calories = part_1 * self.weight / self.M_IN_KM * (self.duration * 60)
        return calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    coeff_clr_3 = 0.035
    coeff_clr_4 = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self):
        part_1 = self.coeff_clr_3 * self.weight
        part_2 = self.get_mean_speed() ** 2 // self.height
        part_3 = self.coeff_clr_4 * self.weight
        calories = (part_1 + part_2 * part_3) * self.duration * 60
        return calories


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38
    coeff_clr_5 = 1.1
    coeff_clr_6 = 2.0

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return round(distance, 3)

    def get_mean_speed(self) -> float:
        part_1 = self.length_pool * self.count_pool
        return part_1 / self.M_IN_KM / self.duration

    def get_spent_calories(self):
        part_1 = (self.get_mean_speed() + self.coeff_clr_5)
        part_2 = self.coeff_clr_6 * self.weight
        calories = part_1 * part_2
        return calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_dict = {'SWM': Swimming, 'RUN': Running, 'WLK': SportsWalking}
    return training_dict[workout_type](*data)


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
        main(training)
