# import streamlit as st
# import csv
# import random

# # Function to read the CSV file and convert it to the desired format
# def read_csv_to_dict(file_path):
#     program_ratings = {}

#     with open(file_path, mode='r', newline='') as file:
#         reader = csv.reader(file)
#         # Skip the header
#         header = next(reader)

#         for row in reader:
#             program = row[0]
#             ratings = [float(x) for x in row[1:]]  # Convert the ratings to floats
#             program_ratings[program] = ratings

#     return program_ratings


# # Define the fitness function
# def fitness_function(schedule):
#     total_rating = 0
#     for time_slot, program in enumerate(schedule):
#         total_rating += ratings[program][time_slot]
#     return total_rating


# # Initialize the population
# def initialize_pop(programs, time_slots):
#     if not programs:
#         return [[]]

#     all_schedules = []
#     for i in range(len(programs)):
#         for schedule in initialize_pop(programs[:i] + programs[i + 1:], time_slots):
#             all_schedules.append([programs[i]] + schedule)

#     return all_schedules


# # Find the best schedule
# def finding_best_schedule(all_schedules):
#     best_schedule = []
#     max_ratings = 0

#     for schedule in all_schedules:
#         total_ratings = fitness_function(schedule)
#         if total_ratings > max_ratings:
#             max_ratings = total_ratings
#             best_schedule = schedule

#     return best_schedule


# # Genetic algorithm components
# def crossover(schedule1, schedule2):
#     crossover_point = random.randint(1, len(schedule1) - 2)
#     child1 = schedule1[:crossover_point] + schedule2[crossover_point:]
#     child2 = schedule2[:crossover_point] + schedule1[crossover_point:]
#     return child1, child2


# def mutate(schedule):
#     mutation_point = random.randint(0, len(schedule) - 1)
#     new_program = random.choice(all_programs)
#     schedule[mutation_point] = new_program
#     return schedule


# def genetic_algorithm(initial_schedule, generations, population_size, crossover_rate, mutation_rate, elitism_size):
#     population = [initial_schedule]

#     for _ in range(population_size - 1):
#         random_schedule = initial_schedule.copy()
#         random.shuffle(random_schedule)
#         population.append(random_schedule)

#     for generation in range(generations):
#         new_population = []

#         # Elitism
#         population.sort(key=lambda schedule: fitness_function(schedule), reverse=True)
#         new_population.extend(population[:elitism_size])

#         while len(new_population) < population_size:
#             parent1, parent2 = random.choices(population, k=2)
#             if random.random() < crossover_rate:
#                 child1, child2 = crossover(parent1, parent2)
#             else:
#                 child1, child2 = parent1.copy(), parent2.copy()

#             if random.random() < mutation_rate:
#                 child1 = mutate(child1)
#             if random.random() < mutation_rate:
#                 child2 = mutate(child2)

#             new_population.extend([child1, child2])

#         population = new_population

#     return population[0]


# # Streamlit App
# def main():
#     st.title("Genetic Algorithm for Program Scheduling")

#     # File input
#     st.subheader("Upload the CSV file")
#     file = st.file_uploader("Choose a CSV file with program ratings", type="csv")
#     if file:
#         file_path = file.name
#         with open(file_path, "wb") as f:
#             f.write(file.getbuffer())
#         st.success("File uploaded successfully!")

#         # Read and process CSV data
#         global ratings, all_programs, all_time_slots
#         ratings = read_csv_to_dict(file_path)
#         all_programs = list(ratings.keys())
#         all_time_slots = list(range(6, 24))  # Time slots from 6:00 to 23:00

#         # Parameter input
#         st.subheader("Set Genetic Algorithm Parameters")
#         GEN = 100
#         POP = 50
#         CO_R = st.slider("Crossover Rate (CO_R)", min_value=0.0, max_value=0.95, value=0.8, step=0.01)
#         MUT_R = st.slider("Mutation Rate (MUT_R)", min_value=0.01, max_value=0.05, value=0.02, step=0.01)
#         EL_S = 2

#         # Generate schedule
#         if st.button("Generate Optimal Schedule"):
#             # Brute force
#             all_possible_schedules = initialize_pop(all_programs, all_time_slots)
#             initial_best_schedule = finding_best_schedule(all_possible_schedules)

#             rem_t_slots = len(all_time_slots) - len(initial_best_schedule)
#             genetic_schedule = genetic_algorithm(
#                 initial_best_schedule,
#                 generations=GEN,
#                 population_size=POP,
#                 crossover_rate=CO_R,
#                 mutation_rate=MUT_R,
#                 elitism_size=EL_S,
#             )

#             final_schedule = initial_best_schedule + genetic_schedule[:rem_t_slots]

#             # Display results
#             st.subheader("Optimal Schedule")
#             for time_slot, program in enumerate(final_schedule):
#                 st.write(f"Time Slot {all_time_slots[time_slot]:02d}:00 - Program {program}")

#             st.subheader("Total Ratings")
#             st.write(fitness_function(final_schedule))


# if __name__ == "__main__":
#     main()


import streamlit as st
import pandas as pd
import csv
import random

# Function to read the CSV file and convert it to the desired format
def read_csv_to_dict(file_path):
    program_ratings = {}

    with open(file_path, mode="r", newline="") as file:
        reader = csv.reader(file)
        header = next(reader)  # Skip the header

        for row in reader:
            program = row[0]
            ratings = [float(x) for x in row[1:]]  # Convert the ratings to floats
            program_ratings[program] = ratings

    return program_ratings

# Define the fitness function
def fitness_function(schedule):
    total_rating = 0
    for time_slot, program in enumerate(schedule):
        total_rating += ratings[program][time_slot]
    return total_rating

# Initialize the population
def initialize_pop(programs, time_slots):
    if not programs:
        return [[]]

    all_schedules = []
    for i in range(len(programs)):
        for schedule in initialize_pop(programs[:i] + programs[i + 1:], time_slots):
            all_schedules.append([programs[i]] + schedule)

    return all_schedules

# Find the best schedule
def finding_best_schedule(all_schedules):
    best_schedule = []
    max_ratings = 0

    for schedule in all_schedules:
        total_ratings = fitness_function(schedule)
        if total_ratings > max_ratings:
            max_ratings = total_ratings
            best_schedule = schedule

    return best_schedule

# Genetic algorithm components
def crossover(schedule1, schedule2):
    crossover_point = random.randint(1, len(schedule1) - 2)
    child1 = schedule1[:crossover_point] + schedule2[crossover_point:]
    child2 = schedule2[:crossover_point] + schedule1[crossover_point:]
    return child1, child2

def mutate(schedule):
    mutation_point = random.randint(0, len(schedule) - 1)
    new_program = random.choice(all_programs)
    schedule[mutation_point] = new_program
    return schedule

def genetic_algorithm(initial_schedule, generations, population_size, crossover_rate, mutation_rate, elitism_size):
    population = [initial_schedule]

    for _ in range(population_size - 1):
        random_schedule = initial_schedule.copy()
        random.shuffle(random_schedule)
        population.append(random_schedule)

    for generation in range(generations):
        new_population = []

        # Elitism
        population.sort(key=lambda schedule: fitness_function(schedule), reverse=True)
        new_population.extend(population[:elitism_size])

        while len(new_population) < population_size:
            parent1, parent2 = random.choices(population, k=2)
            if random.random() < crossover_rate:
                child1, child2 = crossover(parent1, parent2)
            else:
                child1, child2 = parent1.copy(), parent2.copy()

            if random.random() < mutation_rate:
                child1 = mutate(child1)
            if random.random() < mutation_rate:
                child2 = mutate(child2)

            new_population.extend([child1, child2])

        population = new_population

    return population[0]

# Streamlit App
def main():
    st.set_page_config(page_title="Optimal Program Scheduler", layout="wide")
    st.title("📺 Optimal Program Scheduler Using Genetic Algorithm")

    st.sidebar.header("Upload & Configure")
    # File input
    file = st.sidebar.file_uploader("Upload a CSV file with program ratings:", type="csv")

    if file:
        file_path = file.name
        with open(file_path, "wb") as f:
            f.write(file.getbuffer())
        st.sidebar.success("File uploaded successfully!")

        # Read and process CSV data
        global ratings, all_programs, all_time_slots
        ratings = read_csv_to_dict(file_path)
        all_programs = list(ratings.keys())
        all_time_slots = list(range(6, 24))  # Time slots from 6:00 to 23:00

        st.sidebar.header("Set Genetic Algorithm Parameters")
        GEN = 100
        POP = 50
        CO_R = st.sidebar.slider("Crossover Rate", min_value=0.0, max_value=1.0, value=0.8, step=0.01)
        MUT_R = st.sidebar.slider("Mutation Rate", min_value=0.0, max_value=0.1, value=0.02, step=0.01)
        EL_S = 2

        # Generate schedule
        if st.button("Generate Optimal Schedule"):
            all_possible_schedules = initialize_pop(all_programs, all_time_slots)
            initial_best_schedule = finding_best_schedule(all_possible_schedules)

            rem_t_slots = len(all_time_slots) - len(initial_best_schedule)
            genetic_schedule = genetic_algorithm(
                initial_best_schedule,
                generations=GEN,
                population_size=POP,
                crossover_rate=CO_R,
                mutation_rate=MUT_R,
                elitism_size=EL_S,
            )

            final_schedule = initial_best_schedule + genetic_schedule[:rem_t_slots]

            # Display results
            st.subheader("🎯 Optimal Schedule")
            schedule_df = pd.DataFrame({
                "Time Slot": [f"{hour}:00" for hour in all_time_slots],
                "Program": final_schedule,
            })
            st.table(schedule_df)

            st.subheader("📈 Total Ratings")
            st.write(f"**{fitness_function(final_schedule):.2f}**")

if __name__ == "__main__":
    main()


