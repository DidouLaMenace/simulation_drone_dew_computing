import folium
import random
import json
from datetime import datetime
import os

def generer_donnees_sur_trajet(point_depart, point_arrivee, nb_points=30, rayon=0.0005):
    donnees = []
    priorites = ['critique', 'modéré', 'faible']
    
    lat_diff = (point_arrivee[0] - point_depart[0]) / nb_points
    lon_diff = (point_arrivee[1] - point_depart[1]) / nb_points
    
    for i in range(nb_points):
        base_lat = point_depart[0] + lat_diff * i
        base_lon = point_depart[1] + lon_diff * i
        
        point = {
            'latitude': round(base_lat + random.uniform(-rayon, rayon), 6),
            'longitude': round(base_lon + random.uniform(-rayon, rayon), 6),
            'victime_detectee': random.choices([True, False], weights=[0.4, 0.6])[0],
        }
        point['priorite'] = random.choice(priorites) if point['victime_detectee'] else None
        donnees.append(point)
    return donnees

def generer_carte_avec_trajet(donnees, point_depart, point_arrivee, fichier='carte_victimes_trajet.html'):
    carte = folium.Map(location=[(point_depart[0]+point_arrivee[0])/2, (point_depart[1]+point_arrivee[1])/2], zoom_start=14)

    for point in donnees:
        if point['victime_detectee']:
            couleur = {'critique':'red', 'modéré':'orange', 'faible':'green'}[point['priorite']]
            folium.Marker(
                [point['latitude'], point['longitude']],
                popup=f"Victime : {point['priorite']}",
                icon=folium.Icon(color=couleur, icon='exclamation-sign')
            ).add_to(carte)

    folium.Marker(point_depart, popup="Départ du drone", icon=folium.Icon(color='blue', icon='plane')).add_to(carte)
    folium.Marker(point_arrivee, popup="Arrivée du drone", icon=folium.Icon(color='purple', icon='flag')).add_to(carte)
    folium.PolyLine([point_depart, point_arrivee], color='black', weight=2.5, opacity=1).add_to(carte)

    carte.save(fichier)
    print(f"Carte finale générée sous {fichier}")

def simulation_depuis_json():
    try:
        with open("coordonnees_points.json", "r") as f:
            coords = json.load(f)
            point_depart = [coords['depart']['lat'], coords['depart']['lng']]
            point_arrivee = [coords['arrivee']['lat'], coords['arrivee']['lng']]
    except FileNotFoundError:
        print("Le fichier coordonnees_points.json n'existe pas. Lance d'abord la sélection des points.")
        return

    donnees = generer_donnees_sur_trajet(point_depart, point_arrivee)

    victimes = [d for d in donnees if d['victime_detectee']]
    with open("stockage_local.json", "w") as f:
        json.dump(victimes, f)

    generer_carte_avec_trajet(donnees, point_depart, point_arrivee)

    return victimes 

def afficher_resume_victimes(victimes):
    if not victimes:
        print("\nAucune victime détectée.")
        return

    print("\nRésumé des données récupérées à l’atterrissage du drone :\n")

    stats = {'critique': 0, 'modéré': 0, 'faible': 0}

    for v in victimes:
        stats[v['priorite']] += 1

    total = sum(stats.values())
    # print(f"Total de victimes détectées : {total}")
    # print(f"Critiques : {stats['critique']}")
    # print(f"Modérées : {stats['modéré']}")
    # print(f"Faibles : {stats['faible']}")

    # print("\nLocalisation des victimes :")
    # for v in victimes:
    #     print(f" - [{v['priorite'].upper()}] Lat: {v['latitude']}, Lon: {v['longitude']}")


if __name__ == "__main__":
    victimes = simulation_depuis_json()

    if victimes is None:
        exit()

    afficher_resume_victimes(victimes)

    # Génération d'un fichier texte avec le résumé
    stats = {'critique': 0, 'modéré': 0, 'faible': 0}
    for v in victimes:
        stats[v['priorite']] += 1
    total = sum(stats.values())

    lines = []
    lines.append("Résumé de mission du drone autonome\n")
    lines.append(f"Total de victimes détectées : {total}")
    lines.append(f"Critiques : {stats['critique']}")
    lines.append(f"Modérées : {stats['modéré']}")
    lines.append(f"Faibles : {stats['faible']}\n")
    lines.append("Liste des victimes (coordonnées GPS) :")

    priorite_ordre = {'critique': 1, 'modéré': 2, 'faible': 3}
    victimes_triees = sorted(victimes, key=lambda v: priorite_ordre[v['priorite']])

    for v in victimes_triees:
        lines.append(f" - [{v['priorite'].upper()}] Lat: {v['latitude']} | Lon: {v['longitude']}")

    
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    
    
    os.makedirs("rapport", exist_ok=True)

    filename = f"rapport/resume_mission_drone_{timestamp}.txt"
    with open(filename, "w") as f:
        f.write("\n".join(lines))

    print(f"\n📄 Rapport enregistré dans : {filename}")

