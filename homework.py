class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type,
                 duration,
                 distance,
                 speed,
                 calories
                 ):
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def show_message(self):
        return f'Тип тренировки: {self.training_type}; ' \
               f'Длительность: {self.duration} ч.;' \
               f' Дистанция: {self.distance} км;' \
               f' Ср. скорость: {self.speed} км/ч;' \
               f' Потрачено ккал: {self.calories}.'
    pass


class Training:
    """Базовый класс тренировки."""
    M_IN_KM = 1000
    LEN_STEP = 0.65
    coeff_calorie_1 = 18
    coeff_calorie_2 = 20
    coeff_calorie_3 = 0.035
    coeff_calorie_4 = 0.029
    coeff_calorie_5 = 1.1
    coeff_calorie_6 = 2.0

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight
        pass

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = self.action * Training.LEN_STEP / Training.M_IN_KM
        return round(distance, 3)
        pass

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        speed = Training.get_distance(self) / self.duration
        return round(speed, 3)
        pass

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        formula_part_1 = (Training.coeff_calorie_1 * Training.get_mean_speed(self) - Training.coeff_calorie_2)
        formula_part_2 = self.weight / Training.M_IN_KM * self.duration * 60
        calories = formula_part_1 * formula_part_2
        return round(calories, 3)
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories()
                           )
        pass


class Running(Training):
    """Тренировка: бег."""
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float
                 ) -> None:
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        formula_part_1 = (Training.coeff_calorie_1 * Training.get_mean_speed(self) - Training.coeff_calorie_2)
        formula_part_2 = self.weight / Training.M_IN_KM * self.duration * 60
        calories = formula_part_1 * formula_part_2
        return round(calories, 3)
    pass


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self):
        formula_part_1 = Training.coeff_calorie_3 * self.weight
        formula_part_2 = SportsWalking.get_mean_speed(self) ** 2 // self.height
        formula_part_3 = training.coeff_calorie_4 * self.weight
        calories = (formula_part_1 + formula_part_2 * formula_part_3) * self.duration * 60
        return round(calories, 3)
    pass


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38

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
        distance = self.action * Swimming.LEN_STEP / Training.M_IN_KM
        return round(distance, 3)
        pass

    def get_mean_speed(self) -> float:
        return self.length_pool * self.count_pool / Training.M_IN_KM / self.duration
        pass

    def get_spent_calories(self):
        calories = (Swimming.get_mean_speed(self) + training.coeff_calorie_5) * training.coeff_calorie_6 * self.weight
        return round(calories, 3)
    pass


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_dict = {'SWM': Swimming, 'RUN': Running, 'WLK': SportsWalking}
    return training_dict[workout_type](*data)
    pass


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.show_message())
    pass


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)

