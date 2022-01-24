def fibonacci(n: int):
    if n == 1:
        return [1]
    answer = [1, 1]
    for _ in range(n - 2):
        answer.append(answer[-1] + answer[-2])
    return answer


