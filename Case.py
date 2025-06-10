import pulp
import random
import sys
sys.stdout.reconfigure(encoding='utf-8')

# -------------------------------
# PARÂMETROS
# -------------------------------

# Turnos (12 no total, 6 dias, 2 turnos por dia)
turnos = [f"T{t}" for t in range(1, 13)]

# Tipos de profissionais
tipos_profissionais = ["psicologo", "psiquiatra", "psicanalista"]

# Profissionais e suas disponibilidades
profissionais = {
    "PS1": {"tipo": "psicologo", "disponibilidade": 6},
    "PS2": {"tipo": "psicologo", "disponibilidade": 6},
    "PS3": {"tipo": "psicologo", "disponibilidade": 6},
    "PS4": {"tipo": "psicologo", "disponibilidade": 6},
    "PS5": {"tipo": "psicologo", "disponibilidade": 6},
    "PQ1": {"tipo": "psiquiatra", "disponibilidade": 4},
    "PQ2": {"tipo": "psiquiatra", "disponibilidade": 4},
    "PQ3": {"tipo": "psiquiatra", "disponibilidade": 4},
    "PA1": {"tipo": "psicanalista", "disponibilidade": 3},
    "PA2": {"tipo": "psicanalista", "disponibilidade": 3},
}

# Capacidade de atendimento por tipo de profissional
capacidade_atendimento = {
    "psicologo": 3,
    "psiquiatra": 4,
    "psicanalista": 2
}

# Demanda por tipo de atendimento por turno (hipotética)
# random.seed(42)  # Para reprodutibilidade

demanda = {
    "T1": {"psicologo": 10, "psiquiatra": 3, "psicanalista": 2},
    "T2": {"psicologo": 18, "psiquiatra": 4, "psicanalista": 2},
    "T3": {"psicologo": 12, "psiquiatra": 5, "psicanalista": 4},
    "T4": {"psicologo": 20, "psiquiatra": 7, "psicanalista": 3},
    "T5": {"psicologo": 13, "psiquiatra": 5, "psicanalista": 2},
    "T6": {"psicologo": 15, "psiquiatra": 6, "psicanalista": 3},
    "T7": {"psicologo": 14, "psiquiatra": 5, "psicanalista": 1},
    "T8": {"psicologo": 19, "psiquiatra": 8, "psicanalista": 4},
    "T9": {"psicologo": 11, "psiquiatra": 3, "psicanalista": 3},
    "T10": {"psicologo": 16, "psiquiatra": 4, "psicanalista": 2},
    "T11": {"psicologo": 17, "psiquiatra": 6, "psicanalista": 4},
    "T12": {"psicologo": 12, "psiquiatra": 4, "psicanalista": 3}
}


# Número máximo de salas por turno
salas_por_turno = 5

# -------------------------------
# VARIÁVEIS DE DECISÃO
# -------------------------------

# x[i][t] = 1 se profissional i trabalha no turno t, 0 caso contrário
x = pulp.LpVariable.dicts("x", ((i, t) for i in profissionais for t in turnos), cat='Binary')

# -------------------------------
# PROBLEMA
# -------------------------------

prob = pulp.LpProblem("Escalonamento_Profissionais", pulp.LpMinimize)

# -------------------------------
# FUNÇÃO OBJETIVO: minimizar demanda não atendida
# -------------------------------

# Para cada turno e tipo de profissional, computar a demanda não atendida
faltando = {}
for t in turnos:
    for tipo in tipos_profissionais:
        faltando[(tipo, t)] = pulp.LpVariable(f"faltando_{tipo}_{t}", lowBound=0)
        atendido = pulp.lpSum(
            capacidade_atendimento[profissionais[i]["tipo"]] * x[i, t]
            for i in profissionais if profissionais[i]["tipo"] == tipo
        )
        prob += atendido + faltando[(tipo, t)] >= demanda[t][tipo]

# Função objetivo: minimizar a soma da demanda não atendida
prob += pulp.lpSum(faltando.values())

# -------------------------------
# RESTRIÇÕES
# -------------------------------

# Respeitar disponibilidade de cada profissional
for i in profissionais:
    prob += pulp.lpSum(x[i, t] for t in turnos) <= profissionais[i]["disponibilidade"]

# Limite de salas por turno
for t in turnos:
    prob += pulp.lpSum(x[i, t] for i in profissionais) <= salas_por_turno

# -------------------------------
# RESOLVER
# -------------------------------

prob.solve()

# -------------------------------
# RESULTADOS
# -------------------------------

print("Status:", pulp.LpStatus[prob.status])
print("\nEscalonamento de profissionais (ÓTIMO):")
for i in profissionais:
    turnos_trabalhados = [t for t in turnos if x[i, t].value() == 1]
    print(f"{i} ({profissionais[i]['tipo']}): {turnos_trabalhados}")

# Demanda não atendida por turno (ÓTIMO)
faltando_otimo_total = 0
print("\nDemanda não atendida por turno (ÓTIMO):")
for t in turnos:
    for tipo in tipos_profissionais:
        faltando_val = faltando[(tipo, t)].value()
        if faltando_val > 0:
            print(f"Turno {t} - {tipo}: {faltando_val} pacientes não atendidos")
            faltando_otimo_total += faltando_val
print(f"\nTotal de pacientes não atendidos (ÓTIMO): {faltando_otimo_total}")

# -------------------------------
# ESCALA MANUAL (substitua pelos seus dados)
# -------------------------------
escala_manual = {
    "PS1": ['T1', 'T2', 'T5', 'T6', 'T9', 'T10'],
    "PS2": ['T3', 'T4', 'T7', 'T8', 'T11', 'T12'],
    "PS3": ['T1', 'T3', 'T5', 'T7', 'T9', 'T11'],
    "PS4": ['T2', 'T4', 'T6', 'T8', 'T10', 'T12'],
    "PS5": ['T1', 'T2', 'T3', 'T10', 'T11', 'T12'],
    "PQ1": ['T1', 'T2', 'T3', 'T4'],
    "PQ2": ['T5', 'T6', 'T7', 'T8'],
    "PQ3": ['T9', 'T10', 'T11', 'T12'],
    "PA1": ['T1', 'T3', 'T5'],
    "PA2": ['T7', 'T9', 'T11']
}

print("\nEscalonamento de profissionais (MANUAL):")
for i in profissionais:
    turnos_trabalhados = escala_manual.get(i, [])
    print(f"{i} ({profissionais[i]['tipo']}): {turnos_trabalhados}")

# Calcular demanda não atendida para a escala manual
faltando_manual = {}
faltando_manual_total = 0
print("\nDemanda não atendida por turno (MANUAL):")
for t in turnos:
    for tipo in tipos_profissionais:
        atendido = sum(
            capacidade_atendimento[profissionais[i]["tipo"]]
            for i in escala_manual
            if profissionais[i]["tipo"] == tipo and t in escala_manual[i]
        )
        faltando_manual[(tipo, t)] = max(0, demanda[t][tipo] - atendido)
        if faltando_manual[(tipo, t)] > 0:
            print(f"Turno {t} - {tipo}: {faltando_manual[(tipo, t)]} pacientes não atendidos")
            faltando_manual_total += faltando_manual[(tipo, t)]
print(f"\nTotal de pacientes não atendidos (MANUAL): {faltando_manual_total}")

# -------------------------------
# COMPARAÇÃO FINAL
# -------------------------------
print("\nResumo da comparação:")
print(f"Total não atendido (ÓTIMO): {faltando_otimo_total}")
print(f"Total não atendido (MANUAL): {faltando_manual_total}")
if faltando_manual_total > faltando_otimo_total:
    print("A escala ótima atende mais pacientes que a manual.")
elif faltando_manual_total < faltando_otimo_total:
    print("A escala manual atende mais pacientes que a ótima (verifique restrições).")
else:
    print("Ambas as escalas atendem o mesmo número de pacientes.")
