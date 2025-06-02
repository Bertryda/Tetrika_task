def strict(func):
    """Функция-декоратор для проверки введенных 
    значений в сравнении с сигнатурой функции"""
    def wrapper(*args, **kwargs):
        annotation = func.__annotations__
        return_type = annotation.pop("return", None)
        wrap_args = {i: type(args[i]) for i in range(len(args))} | kwargs # Получаем общий словарь данных
        
        #Проверка на количество переданных обязательных параметров
        if len(annotation) != len(wrap_args):
            raise TypeError(
                f"{func.__name__} takes {len(annotation)} arguments but {len(wrap_args)} were given"
            )
        count = 0
        
        #Проверка позиционных и именованных параметров
        for i in annotation:
            if i in wrap_args:
                if annotation[i] != wrap_args[i]:
                    raise TypeError(
                        "Type mismatch"
                    )
            else:
                if annotation[i] != wrap_args[count]:
                    raise TypeError(
                        "Type mismatch"
                    )
                count += 1
        result = func(*args, **kwargs) 
        
        #Проверка возвращаемого значения
        if return_type and (return_type != type(result)):
            raise TypeError(
                "result type mismatch"
            )
        return result 
    
    return wrapper


@strict
def sum_two(a: int, b: int) -> int:
    return a + b

print(sum_two(1, 2))

