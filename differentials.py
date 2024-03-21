import pickle
from query_recontructor import recon
import itertools
from collections import Counter
import os

def differential_diseases(query):
    with open('./Dataset/inverted_index.pkl','rb') as file:
        inverted_index = pickle.load(file)
    recon_query = recon(query)
    differentials = {}
    for i in recon_query:
        dis = inverted_index[i]
        for j in dis:
            if j in differentials:
                differentials[j] +=1
            else:
                differentials[j] =1
    sorted_differentials = dict(sorted(differentials.items(), key=lambda item: item[1], reverse=True))
    return sorted_differentials.keys()

def cosymptoms(query):
    # Query symptoms as a combination
    with open('./Dataset/association_rules.pkl', 'rb') as f:
        rules = pickle.load(f)
    query_symptoms_combination=tuple(recon(query))
    while True:
    # Get all combinations of symptoms
        all_combinations = []
        for r in range(1, len(query_symptoms_combination) + 1):
            all_combinations.extend(itertools.combinations(query_symptoms_combination, r))

    # Initialize a Counter to store the occurrence count of co-occurring symptoms
        co_occurring_symptoms_count = Counter()

    # Iterate over each combination of symptoms
        for combination in all_combinations:
        # Convert the combination to a frozenset for efficient membership testing
            query_symptoms_set = frozenset(combination)

        # Filter rules that involve the query symptoms combination
            filtered_rules = rules[rules['antecedents'].apply(lambda antecedent: query_symptoms_set.issubset(antecedent))]

        # Sort the filtered rules by confidence in descending order
            sorted_rules = filtered_rules.sort_values(by='confidence', ascending=False)

            top_co_occurring_symptoms = set()
            for consequent_list in sorted_rules['consequents']:
                top_co_occurring_symptoms.update(consequent_list)

            top_co_occurring_symptoms.difference_update(query_symptoms_set)

            co_occurring_symptoms_count.update(top_co_occurring_symptoms)

        top_co_occurring_symptoms = co_occurring_symptoms_count.most_common(10)

        co_occur_symp=[]
        count=1
        print("Top Co-occurring Symptoms:")
        for symptom in top_co_occurring_symptoms:
            if symptom[0] in list(query_symptoms_combination):
                pass
            else:
                co_occur_symp.append(symptom)
                print(str(count)+' '+symptom[0])
                count+=1

    # Ask the user if they want to add another symptom
        add_another = input("Do you want to add another symptom? (yes/no): ").lower()

    # If the user wants to add another symptom, update the query symptoms combination
        if add_another == 'yes':
        # Print the current query symptoms combination
            print("Current Query Symptoms Combination:", query_symptoms_combination)

        # Ask the user to enter the index of the symptom to add
            index = int(input("Enter the index of the symptom you want to add (1 to {}): ".format(len(tuple(co_occur_symp))))) - 1

        # Add the selected symptom to the query symptoms combination
            query_symptoms_combination += (co_occur_symp[index][0],)
            print('Final:',query_symptoms_combination)

    # If the user does not want to add another symptom, exit the loop
        elif add_another == 'no':
            return query_symptoms_combination

    # If the user enters an invalid response, ask again
        else:
            print("Invalid input! Please enter 'yes' or 'no'.")     



query = input("Enter the Symptoms seperated by comma: ")
query_combo=cosymptoms(query)
print(query_combo)
final_query=', '.join(query_combo)
differentials = list(differential_diseases(final_query))


corpus_path = "F:/IR Project/symtoms_redormulation/corpus"

# Get the list of top 15 diseases
top_diseases = differentials[:15]

# Print the top 15 diseases with indices
print("Top 15 Diseases:")
for i, disease in enumerate(top_diseases, 1):
    print(f"{i}. {disease}")

# Ask the user to select a disease by index
selected_index = int(input("Enter the index of the disease you want to view details for: ")) - 1

# Validate the selected index
if 0 <= selected_index < len(top_diseases):
    selected_disease = top_diseases[selected_index]

    # Load details from the corresponding .txt file
    file_path = os.path.join(corpus_path, f"{selected_disease}.txt")
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            disease_details = file.read()
        print(f"Details for {selected_disease}:")
        print(disease_details)
    else:
        print("Details not available for the selected disease.")
else:
    print("Invalid index. Please enter a valid index.")
