import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats

"""
Решение заданий Практики к Уроку-10 (Итоговая)
"""

# Задание-1.
# Провести дисперсионный анализ для определения того,
# есть ли различия среднего роста среди взрослых футболистов, хоккеистов и штангистов.
# # Даны значения роста в трех группах случайно выбранных спортсменов:
# # Футболисты: 173, 175, 180, 178, 177, 185, 183, 182.
# # Хоккеисты: 177, 179, 180, 188, 177, 172, 171, 184, 180.
# # Штангисты: 172, 173, 169, 177, 166, 180, 178, 177, 172, 166, 170.

# Пояснение выбора  метода:
# 1) По условию задачи более 2-х групп для сравнения, поэтому используем критерий Фишера.
# 2) По условию на значение (средний рост) рассматривается влияние только одного фактора
#    (занятие тем или иным видом спорта), поэтому используем однофакторный дисперсионный анализ
# 3) Для расчетов используем формулу 𝐹_н = (𝜎_ф^2) / (𝜎_ост^2), где
#    𝜎_ф^2          = (𝑆_ф^2) / (𝑘−1),      где k - число выборок
#    𝜎_ост^2        = (𝑆_ост^2) / (𝑛−𝑘),    где n - общее во всех выборках число замеров
#    Здесь  𝑆_ф^2   = ∑(𝑖=1...𝑘) (𝑦_mean_𝑖 - 𝑌_mean)^2∗𝑛_𝑖, где 𝑌_mean - общая средняя по всем выборкам
#           𝑆_ост^2 = ∑(𝑖=1...𝑘) ∑_(𝑗=1...𝑛_𝑖) (𝑦_𝑖𝑗 − 𝑦_mean_𝑖)^2, где 𝑦_mean_𝑖 - средняя по n-й выборке

#
alfa = 0.05         # для анализа используем стандартный уровень значимости (5%)


# Набор данных по спортсменам:
tit = 'Роста в трех группах случайно выбранных спортсменов'
tit_mean = 'Средний рост спортсменов по группам'
y1 = np.array([173, 175, 180, 178, 177, 185, 183, 182])
y2 = np.array([177, 179, 180, 188, 177, 172, 171, 184, 180])
y3 = np.array([172, 173, 169, 177, 166, 180, 178, 177, 172, 166, 170])
K = 3
n1, n2, n3 = y1.size, y2.size, y3.size
N = n1 + n2 + n3

# Расчет:

# Средняя общая и средние по выборкам
print('\n--------------------------------------------')
print(f'Задание-1. Дисперсионный анализ.\n'
      f'{tit}:')
print(f'Футболисты - {y1}\n'
      f'Хоккеисты - {y2}\n'
      f'Штангисты - {y3}\n'
      f'Число выборок K = {K}\n'
      f'Число замеров во всех выборках N = {N}')

y1_mean, y2_mean, y3_mean = np.mean(y1), np.mean(y2), np.mean(y3)
yT = np.hstack([y1, y2, y3])
yt_mean = np.mean(yT)
print()
print(f'{tit_mean}:')
print(f'Футболисты = {round(y1_mean, 3)}\n'
      f'Хоккеисты = {round(y2_mean, 3)}\n'
      f'Штангисты = {round(y3_mean, 3)}\n'
      f'Общий = {round(yt_mean, 3)}')

# Сумма квадратов отклонений:
S_f = np.sum((y1_mean - yt_mean) ** 2) * n1 + \
      np.sum((y2_mean - yt_mean) ** 2) * n2 + \
      np.sum((y3_mean - yt_mean) ** 2) * n3

S_res = np.sum((y1 - y1_mean) ** 2) + \
        np.sum((y2 - y2_mean) ** 2) + \
        np.sum((y3 - y3_mean) ** 2)

S_total = np.sum((yT - yt_mean) ** 2)

# Дисперсии:
D_f = S_f / (K - 1)                         # факторная дисперсия
D_res = S_res / (N - K)

print(f'\nСумма квадратов отклонений и дисперсия:\n'
      f'Факторная  = {round(S_f, 3), round(D_f, 3)}\n'
      f'Остаточная = {round(S_res, 3), round(D_res, 3)}\n'
      f'Общая = {round(S_total, 3)}')

# Критерий Фишера:
# ------------------------------------------------------------
F_n = D_f / D_res

# По таблице Фишера определим граничное значения критерия,
# больше которого будет принята альтернативная гипотеза -
# существует значимое влияние вида спорта на ср.рост спортсмена
F_crit = 3.39
print(f'\nF_крит для степеней свободы в числителе ({K-1}) и в знаменателе ({N-K}) = {F_crit}')
print(f'Критерий Фишера для анализируемых выборок = {round(F_n, 3)}')

# Определение альтернативности гипотезы с помощью p_value
# Для этого воспользуемся встроенной функцией библиотеки statistic - f_oneway()
res = stats.f_oneway(y1, y2, y3)
m = K
alfa_triple = round(1 - (1-alfa)**m, 3)

# Результат:
H0_txt = f'Занятие тем или иным видом спорта не имеет влияние на средний рост спортсменов =>'
H1_txt = 'Значимое различие среднего роста спортсменов в зависимости от вида спорта имеется =>'

H0f_cond = f'(F_n = {round(F_n, 3)}) <= (F_crit = {F_crit})'
H1f_cond = f'(F_n = {round(F_n, 3)}) > (F_crit = {F_crit})'
txt_f0    = f'{H0_txt} {H0f_cond}'
txt_f1    = f'{H1_txt} {H1f_cond}'
p_value = round(res[1], 3)
H0v_cond = f'(p_value = {p_value}) >= (𝛼 ́ = {alfa_triple})'
H1v_cond = f'(p_value = {p_value}) < (𝛼 ́ = {alfa_triple})'
txt_v0    = f'{H0_txt} {H0v_cond}'
txt_v1    = f'{H1_txt} {H1v_cond}'

print('\nРезультат.\n'
      '===============================\n'
      f'1. По табличным данным F_крит:\n'
      f'{txt_f1 if F_n > F_crit else txt_f0}\n'
      f'2. По p_value => {res}:\n'
      f'{txt_v1 if res[1] < alfa_triple else txt_v0}\n')
