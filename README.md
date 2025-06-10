### 🧠 Lógica do Código

O script desenvolvido em Python utiliza Programação Inteira (com a biblioteca PuLP) para otimizar o escalonamento de profissionais da saúde mental. Ele segue a seguinte lógica:

## 1. Definição dos parâmetros do problema

- Lista de turnos disponíveis (12 turnos: 6 dias, 2 turnos por dia).
- Tipos de profissionais envolvidos (psicólogos, psiquiatras e psicanalistas).
- Quantidade de profissionais por tipo e suas respectivas disponibilidades.
- Capacidade de atendimento por tipo de profissional.
- Demanda esperada por tipo de atendimento em cada turno.
- Limite de salas disponíveis por turno.

## 2. Modelagem do problema

- O modelo define variáveis binárias que indicam se um profissional será alocado em determinado turno.
- A função objetivo é minimizar a soma total de pacientes não atendidos em todos os turnos.

## 3. Aplicação de restrições

- Cada profissional só pode ser escalado até o limite máximo de turnos definido por sua disponibilidade semanal.
- Em cada turno, o total de profissionais alocados não pode exceder a quantidade de salas disponíveis.
- A soma dos atendimentos prestados por profissionais de cada especialidade deve cobrir ao menos parte da demanda prevista.

## 4. Resolução do problema

- O solver executa a otimização e gera a melhor escala possível dentro das restrições.

## 5. Impressão dos resultados

- Exibe a escala de trabalho ótima (gerada pelo modelo), indicando os turnos alocados para cada profissional.
- Exibe a quantidade de pacientes não atendidos em cada turno.
- Compara os resultados da escala ótima com uma escala manual (pré-definida), permitindo avaliar a eficiência do modelo matemático.

---

#📌 Resultado esperado: minimizar as filas de espera, equilibrar a carga de trabalho dos voluntários e aproveitar melhor os recursos limitados (salas e turnos).
