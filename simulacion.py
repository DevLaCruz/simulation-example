import simpy
import random
import matplotlib.pyplot as plt
import networkx as nx


def area_preparacion_parte_a(env):
    while True:
        # Llegada de cajas de metal moldeado para Parte A (exp(5) tiempo entre llegadas)
        yield env.timeout(random.expovariate(1/5))
        
        # Proceso en el Área de preparación de Parte A (distribución triangular: 1, 4, 8)
        tiempo_proceso = random.triangular(1, 8, 4)
        yield env.timeout(tiempo_proceso)
        
        # Transfiere la parte al Área de sellado
        yield env.process(area_sellado(env))

def area_preparacion_parte_b(env):
    while True:
        # Llegada de lotes de Parte B (exp(30) tiempo entre llegadas)
        yield env.timeout(random.expovariate(1/30))
        
        # Proceso en el Área de preparación de Parte B (distribución triangular: 3, 10, 5)
        tiempo_proceso = random.triangular(3, 10, 5)
        yield env.timeout(tiempo_proceso)
        
        # Dividir el lote de Parte B en cuatro unidades individuales y enviar cada una al Área de preparación
        for _ in range(4):
            env.process(area_preparacion_parte_a(env))

def area_sellado(env):
    # Proceso en el Área de sellado
    tipo_parte = random.choices(['Parte A', 'Parte B'], [0.91, 0.09])[0]
    if tipo_parte == 'Parte A':
        tiempo_proceso = random.triangular(1, 4, 3)
    else:
        tiempo_proceso = random.weibullvariate(2.5, 5.3)
    yield env.timeout(tiempo_proceso)
    
    # Inspección de unidades selladas
    if random.random() <= 0.91:  # 91% pasa la inspección
        print(f'{env.now:.2f}: {tipo_parte} aprobada y enviada al departamento de envío.')
    else:
        yield env.process(area_retrabajo(env))

def area_retrabajo(env):
    # Proceso de retrabajo (exp(45) tiempo para reprocesar una parte)
    yield env.timeout(random.expovariate(1/45))
    
    # Probabilidad de recuperación (80% reprocesado y enviado al departamento de envío)
    if random.random() <= 0.8:
        print(f'{env.now:.2f}: Parte reprocesada y enviada al departamento de envío.')
    else:
        print(f'{env.now:.2f}: Parte descartada.')


#Función para generar el gráfico
def generate_graph():
  # Crear un gráfico dirigido
    G = nx.DiGraph()

    # Agregar nodos al gráfico
    G.add_node("Cajas de metal moldeado")
    G.add_node("Lote de Parte B")
    G.add_node("Área de preparación Parte A")
    G.add_node("Área de preparación Parte B")
    G.add_node("Área de sellado")
    G.add_node("Área de retrabajo")
    G.add_node("Departamento de envío")
    G.add_node("Parte A")
    G.add_node("Parte B")

    # Agregar aristas al gráfico (representan los eventos y transiciones)
    G.add_edge("Cajas de metal moldeado", "Área de preparación Parte A")
    G.add_edge("Lote de Parte B", "Área de preparación Parte B")
    G.add_edge("Área de preparación Parte B", "Área de preparación Parte A")
    G.add_edge("Área de preparación Parte A", "Área de sellado")
    G.add_edge("Área de preparación Parte B", "Área de sellado")
    G.add_edge("Área de sellado", "Departamento de envío")
    G.add_edge("Área de sellado", "Área de retrabajo")
    G.add_edge("Área de retrabajo", "Área de preparación Parte A")
    G.add_edge("Área de retrabajo", "Área de preparación Parte B")

    # Asignar posiciones a los nodos para una mejor visualización
    pos = {
        "Cajas de metal moldeado": (0, 2),
        "Lote de Parte B": (0, 1),
        "Área de preparación Parte A": (1, 2),
        "Área de preparación Parte B": (1, 1),
        "Área de sellado": (2, 2),
        "Área de retrabajo": (2, 1),
        "Departamento de envío": (3, 2),
        "Parte A": (1, 3),
        "Parte B": (1, 0),
    }

    nx.draw(G, pos, with_labels=True, node_size=1000, node_color="skyblue", font_size=8, font_weight="bold")
    plt.title("Modelo Conceptual de Simulación")
    plt.show()

# Inicializar la simulación
env = simpy.Environment()
env.process(area_preparacion_parte_b(env))
env.run(until=1000)  # Tiempo de simulación (Puede variar)

# Generar el gráfico del modelo conceptual
generate_graph()