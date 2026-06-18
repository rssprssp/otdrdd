import math
import streamlit as st

# Настройка страницы (заголовок вкладки браузера и иконка)
st.set_page_config(
    page_title="Калькулятор ДД OTDR",
    page_icon="⚡",
    layout="centered"
)

# Заголовок на странице
st.title("📟 Инженерный калькулятор динамического диапазона OTDR")
st.markdown("Программа для расчета необходимого паспортного динамического диапазона оптического рефлектометра.")

# Разделяем интерфейс на две колонки для удобства
col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Параметры трассы ВОЛС")
    
    length = st.slider(
        "Длина трассы (км):", 
        min_value=1.0, 
        max_value=150.0, 
        value=50.0, 
        step=1.0
    )
    
    wavelength = st.selectbox(
        "Длина волны:",
        options=["1310 нм", "1550 нм"],
        index=1  # По умолчанию выберет 1550 нм
    )
    
    min_event_loss = st.slider(
        "Минимальное измеряемое событие (дБ):", 
        min_value=0.02, 
        max_value=0.30, 
        value=0.10, 
        step=0.01,
        help="Величина потерь на сварке, которую необходимо четко видеть на конце линии."
    )

with col2:
    st.subheader("2. Настройки измерений")
    
    pulse_width_str = st.selectbox(
        "Ширина импульса рефлектометра:",
        options=["10 нс", "30 нс", "100 нс", "275 нс", "1 мкс", "2.5 мкс", "10 мкс", "20 мкс"],
        index=4  # По умолчанию выберет 1 мкс
    )
    
    avg_time_s = st.selectbox(
        "Время усреднения теста:",
        options=[(15, "15 сек"), (30, "30 сек"), (60, "1 мин (60 с)"), (180, "3 мин (180 с)"), (300, "5 мин (300 с)")],
        format_func=lambda x: x[1],
        index=3  # По умолчанию выберет 3 мин
    )[0]  # Берем только числовое значение в секундах

st.markdown("---")

# --- БЛОК МАТЕМАТИЧЕСКИХ РАСЧЕТОВ ---

# 1. Затухание в волокне
alpha = 0.35 if wavelength == "1310 нм" else 0.22
fiber_loss = length * alpha

# 2. Оптический запас по формуле B = 5 * log10(4 / a)
margin = 5 * math.log10(4 / min_event_loss)
required_trace_dr = fiber_loss + margin

# 3. Поправка на импульс: Di = 5 * log10(i1 / i2)
pulse_mapping = {
    "10 нс": 0.01, "30 нс": 0.03, "100 нс": 0.1, 
    "275 нс": 0.275, "1 мкс": 1.0, "2.5 мкс": 2.5, 
    "10 мкс": 10.0, "20 мкс": 20.0
}
pulse_selected = pulse_mapping[pulse_width_str]
pulse_ref = 20.0
D_i = 5 * math.log10(pulse_selected / pulse_ref)

# 4. Поправка на время: Dt = 2.5 * log10(t1 / t2)
time_ref = 180.0
D_t = 2.5 * math.log10(avg_time_s / time_ref)

# 5. Итоговый паспортный диапазон
required_passport_dr = required_trace_dr - D_i - D_t

# --- ВЫВОД РЕЗУЛЬТАТОВ ---
st.subheader("📊 Результаты анализа")

st.write(f"Потери в волокне: {fiber_loss:.2f} дБ")
st.write(f"Расчетный запас (Margin): {margin:.2f} дБ")
st.write(f"Живой ДД трассы: {required_trace_dr:.2f} дБ")
st.write(f"Изменение ДД из-за длительности импульса (D_i): {D_i:.2f} дБ")
st.write(f"Изменение ДД из-за времени накопления (D_t): {D_t:.2f} дБ")
st.write(f"ТРЕБУЕМЫЙ ПАСПОРТНЫЙ ДИАПАЗОН ПРИБОРА: **{required_passport_dr:.2f} дБ**")
st.caption("Примечание: данный диапазон должен быть указан в технических характеристиках (паспорте) рефлектометра для стандартных условий измерений (20 мкс / 3 мин).")