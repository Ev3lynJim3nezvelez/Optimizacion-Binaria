# Modelamiento, Análisis Analítico-Numérico y Validación Experimental del Llenado Forzado de un Globo Elástico

**Autores:** Santiago Londoño & Evelyn Jiménez  
**Asignatura:** Modelamiento Matemático (2026-10)  
**Docente:** Juan Pablo Moreno  
**Fecha:** 9 de octubre de 2026  

---

## Resumen

Este trabajo presenta la formulación, solución analítica, implementación numérica mediante el método de Runge-Kutta de orden 4 (RK4) y la validación experimental del proceso de llenado de un globo elástico pequeño conectado a un globo grande mediante un conducto rígido[cite: 1, 12, 13]. Partiendo del modelo constitutivo hiperelástico de neo-Hooke y la ley de Laplace integrados con la resistencia neumática de Poiseuille (desarrollados en la Fase 1)[cite: 1], se extiende el modelo dinámico para adaptarlo a la condición experimental real de la Fase 2, en la cual el globo grande actúa como una fuente de presión por apriete dinámico $P_1(t)$[cite: 12]. La solución numérica muestra un ajuste óptimo con un error relativo medio del **0.18 %** frente a las mediciones experimentales[cite: 12].

---

## 1. Descripción del Fenómeno y Marco Teórico (Fase 1 Revisitada)

### 1.1. Fundamentos Físicos
El comportamiento mecánico de la membrana elástica y la presión manométrica interna se rige por las siguientes relaciones constitutivas:

1. **Ley de Laplace para membranas esféricas delgadas:**
   $$P(r) = \frac{2 T(r)}{r}$$[cite: 9]

2. **Tensión de membrana para un material hiperelástico neo-Hookeano:**
   $$T(\lambda) = \frac{E h_0}{3} \left(\lambda - \lambda^{-5}\right)$$[cite: 9]
   donde $\lambda = \frac{r}{r_0}$ es la razón de estiramiento (elongación equibiaxial)[cite: 3], $E$ es el módulo elástico y $h_0$ el espesor inicial de la membrana[cite: 4].

3. **Presión manométrica interna (Curva no monótona de "joroba"):**
   Sustituyendo $T(\lambda)$ en la ley de Laplace con $r = \lambda r_0$[cite: 9]:
   $$P(\lambda) = P_0 \left(\lambda^{-1} - \lambda^{-7}\right), \qquad P_0 \equiv \frac{2 E h_0}{3 r_0}$$[cite: 9]

   La función $P(\lambda)$ presenta un máximo característico en $\lambda^* = 7^{1/6} \approx 1.383$, donde alcanza un pico de presión $P_{\max} \approx 0.618 P_0$[cite: 9, 12]. En función del volumen $V = \frac{4}{3}\pi r^3 = V_0 \lambda^3$[cite: 9]:
   $$P(V) = P_0 \left[ \left(\frac{V_0}{V}\right)^{1/3} - \left(\frac{V_0}{V}\right)^{7/3} \right]$$[cite: 9]

---

### 1.2. Ecuación Diferencial del Llenado Forzado (Fase 2)
En el montaje experimental de la Fase 2, el globo grande no evoluciona de manera pasiva como en el modelo cerrado simétrico de la Fase 1, sino que es comprimido manualmente para forzar el inflado del globo pequeño[cite: 12]. Esta fuerza ejercida externamente se modela como una rampa de presión impuesta[cite: 12]:
$$P_1(t) = P_0 \cdot \tau \cdot (A + B \cdot t)$$[cite: 12]

El balance de caudal volumétrico $Q(t) = \frac{P_1(t) - P(V)}{R}$ que ingresa al globo pequeño a través de la resistencia neumática del tubo $R$ genera la EDO ordinaria no lineal y no autónoma para el volumen $V(t)$[cite: 10, 12]:
$$\frac{dV}{dt} = \frac{1}{R} \left[ P_1(t) - P(V) \right], \qquad V(0) = V_0$$[cite: 10, 12]

Expresada en términos de la elongación $\lambda(t) = \left(\frac{V}{V_0}\right)^{1/3}$ y definiendo la constante de tiempo neumática $\tau = \frac{R V_0}{P_0}$, se obtiene la EDO adimensional reducida[cite: 12]:
$$\frac{d\lambda}{dt} = \frac{(A + B t) - \frac{p(\lambda)}{\tau}}{3 \lambda^2}, \qquad \lambda(0) = 1$$[cite: 12]
donde $p(\lambda) = \lambda^{-1} - \lambda^{-7}$[cite: 9, 12].

---

## 2. Solución Analítica Aproximada

### 2.1. Clasificación de la EDO
La EDO que gobierna el sistema es de **primer orden, no lineal y no autónoma**[cite: 12].

### 2.2. Procedimiento de Solución
Cuando la presión ejercida por el apriete manual domina sobre la contrapresión elástica de la membrana del globo pequeño ($\tau(A + Bt) \gg p(\lambda)$), se puede despreciar el término $\frac{p(\lambda)}{\tau}$[cite: 12]. Bajo esta aproximación, la ecuación se vuelve separable[cite: 12]:
$$3 \lambda^2 d\lambda = (A + B t) dt$$[cite: 12]

Integrando desde las condiciones iniciales $\lambda(0) = 1$ en $t = 0$[cite: 12]:
$$\int_{1}^{\lambda} 3 \tilde{\lambda}^2 d\tilde{\lambda} = \int_{0}^{t} (A + B \tilde{t}) d\tilde{t} \implies \lambda(t)^3 - 1 = A t + \frac{B}{2} t^2$$[cite: 12]

### 2.3. Solución Particular Explícita para la Circunferencia $C(t)$
A partir de la relación geométrica entre la elongación y la circunferencia medida $C(t) = 2\pi r_0 (\lambda(t) - 1)$[cite: 12]:
$$C(t) = 2\pi r_0 \left[ \left(1 + A_a t + \frac{B_a}{2} t^2\right)^{1/3} - 1 \right]$$[cite: 12]

### 2.4. Interpretación Física
La solución analítica cerrada muestra que el volumen crece proporcionalmente a la rampa de caudal impuesta externamente por el apriete[cite: 12]. Las constantes ajustadas ($A_a, B_a$) absorben el efecto de la contrapresión elástica omitida durante la simplificación[cite: 12].

---

## 3. Solución Numérica (RK4)

Para resolver la EDO completa sin despreciar la respuesta no lineal de la membrana hiperelástica, se utiliza el algoritmo explícito de Runge-Kutta de 4.º orden (RK4)[cite: 12]:

$$k_1 = F(t_n, \lambda_n)$$[cite: 12]
$$k_2 = F\left(t_n + \frac{h}{2}, \lambda_n + \frac{h}{2}k_1\right)$$[cite: 12]
$$k_3 = F\left(t_n + \frac{h}{2}, \lambda_n + \frac{h}{2}k_2\right)$$[cite: 12]
$$k_4 = F(t_n + h, \lambda_n + h k_3)$$[cite: 12]
$$\lambda_{n+1} = \lambda_n + \frac{h}{6} (k_1 + 2k_2 + 2k_3 + k_4)$$[cite: 12]

donde la función diferencial está definida como[cite: 12]:
$$F(t, \lambda) = \frac{(A + B t) - \frac{p(\lambda)}{\tau}}{3 \lambda^2}$$[cite: 12]

---

## 4. Comparación de Resultados y Análisis de Error

El error relativo porcentual en la circunferencia $C$ se calcula como[cite: 12]:
$$\varepsilon = \frac{|C_{\text{modelo}} - C_{\text{exp}}|}{C_{\text{exp}}} \times 100\%$$[cite: 12]

### 4.1. Tabla Comparativa de Error Relativo (Evaluado en 6 Instantes)

| Tiempo $t$ [s] | $C_{\text{exp}}$ [cm] | $C_{\text{analítica}}$ [cm] | $C_{\text{RK4}}$ [cm] | Error RK4 vs Exp [%] | Error Analít. vs Exp [%] | Error Analít. vs RK4 [%] |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 4.0 | 2.50 | 2.50 | 2.52 | **0.627 %** | 0.088 % | 0.538 % |
| 8.0 | 5.00 | 5.00 | 5.00 | **0.016 %** | 0.011 % | 0.027 % |
| 12.0 | 7.80 | 7.81 | 7.80 | **0.057 %** | 0.160 % | 0.217 % |
| 16.0 | 10.70 | 10.70 | 10.70 | **0.012 %** | 0.003 % | 0.015 % |
| 20.0 | 13.70 | 13.70 | 13.70 | **0.252 %** | 0.207 % | 0.459 % |
| 24.0 | 16.60 | 16.60 | 16.60 | **0.149 %** | 0.231 % | 0.380 % |

* **Error Relativo Medio (RK4 vs. Exp):** **0.18 %**[cite: 12]

### 4.2. Análisis de Convergencia Numérica
Para verificar el orden teórico del método RK4, se evaluó la solución en $T = 10\text{ s}$ reduciendo el paso de integración $h \in \{2.0, 1.0, 0.5, 0.25, 0.125\}\text{ s}$[cite: 12]. El ajuste en escala logarítmica arroja una pendiente de **4.00**, lo que confirma el orden de convergencia de $\mathcal{O}(h^4)$[cite: 12].

---

## 5. Variaciones del Modelo (Análisis de Sensibilidad)

1. **Variación A — Sensibilidad al Radio Natural $r_0$:** Se evaluó el modelo con $r_0 \in \{1.5, 2.0, 3.0, 4.0\}\text{ cm}$[cite: 12, 15]. Al reajustar los parámetros $(A, B, \tau)$, todos los casos reproducen los datos experimentales con un $\text{RMSE} \approx 0.02\text{ cm}$, demostrando que $r_0$ no es identificable unívocamente sin mediciones directas de presión[cite: 12, 15].
2. **Variación B — Apriete Constante ($B = 0$):** Se suprimió la rampa temporal de apriete[cite: 12, 15]. Esto provoca un apartamiento en los instantes finales, demostrando que la fuerza de compresión manual aumentó gradualmente durante la prueba[cite: 12, 15].
3. **Variación C — Variación de la Contrapresión ($\tau$):** Escalar la constante de tiempo neumática ($\tau \to 0.5\tau$ y $2\tau$) confirma que a mayor rigidez de la membrana, menor es la tasa de expansión inicial[cite: 12, 15].
4. **Variación D — Modelo Constitutivo Mooney-Rivlin:** Se incluyó el término no lineal $\beta \lambda^2$ ($p(\lambda) \to p(\lambda)(1 + \beta \lambda^2)$), lo cual permite capturar el endurecimiento del caucho ante gran deformación[cite: 12, 15].
5. **Variación E — Fuga de Aire:** Se incorporó un término de pérdida continua de caudal de la forma $-\frac{c \lambda}{3}$, permitiendo representar sistemas con fugas en los acoples[cite: 12, 15].

---

## 6. Conclusiones y Discusión Final

1. **Adecuación del Modelo:** El modelo pasivo puro de la Fase 1 es insuficiente para describir el llenado forzado (error RMSE $\approx 7\text{ cm}$)[cite: 12]. La formulación extendida de la Fase 2 reduce el error por debajo de la precisión instrumental de la cinta de medición ($\approx 0.1\text{ cm}$)[cite: 12].
2. **Comparación Analítica vs. Numérica:** La solución analítica aproximada captura la tendencia cuando se optimizan sus constantes de forma independiente[cite: 12]. Sin embargo, la integración por RK4 resuelve la EDO exacta considerando la mecánica hiperelástica completa[cite: 12].
3. **Limitaciones y Recomendaciones:** Se recomienda instrumentar prototipos futuros con sensores de presión manométrica para medir directamente el perfil $P_1(t)$ y evitar la estimación indirecta de parámetros[cite: 5, 12].
