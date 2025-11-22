import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# Генерация данных: [рост (см), вес (кг)]
np.random.seed(42)
heights = np.random.normal(170, 15, 1000)  # Средний рост 170 см
weights = np.random.normal(70, 20, 1000)   # Средний вес 70 кг
ages = np.random.randint(15, 30, 1000)     # Возраст от 15 до 30 лет
# Целевая переменная: 1 — взрослый (18+), 0 — несовершеннолетний
labels = (ages >= 18).astype(int)

# Объединяем признаки (рост и вес)
features = np.column_stack((heights, weights))

# Разделение данных на обучающую и тестовую выборки
X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, random_state=42)

# Обучение модели
model = LogisticRegression()
model.fit(X_train, y_train)

# Прогноз на тестовой выборке
y_pred = model.predict(X_test)

# Оценка точности
accuracy = accuracy_score(y_test, y_pred)
print(f"Точность модели: {accuracy:.2f}")

# Пример предсказания для нового человека: [175 см, 75 кг]
new_person = np.array([[175, 75]])
prediction = model.predict(new_person)
print(f"Предсказание для [175 см, 75 кг]: {'Взрослый' if prediction[0] == 1 else 'Несовершеннолетний'}")