import folium
import random
import json

# Générer des points le long du trajet du drone
def generer_donnees_sur_trajet(point_depart, point_arrivee, nb_points=30, rayon=0.002):
    donnees = []
    priorites = ['critique', 'modéré', 'faible']
    
    lat_diff = (point_arrivee[0] - point_depart[0]) / nb_points
    lon_diff = (point_arrivee[1] - point_depart[1]) / nb_points
    
    for i in range(nb_points):
        base_lat = point_depart[0] + lat_diff * i
        base_lon = point_depart[1] + lon_diff * i
        
        # Ajoute un petit décalage autour du trajet pour simuler des données réalistes
        point = {
            'latitude': round(base_lat + random.uniform(-rayon, rayon), 6),
            'longitude': round(base_lon + random.uniform(-rayon, rayon), 6),
            'victime_detectee': random.choices([True, False], weights=[0.4, 0.6])[0],
        }
        point['priorite'] = random.choice(priorites) if point['victime_detectee'] else None
        donnees.append(point)
    return donnees

# Carte interactive avec le trajet et points générés sur ce trajet
def generer_carte_avec_trajet(donnees, point_depart, point_arrivee, fichier='carte_victimes_trajet.html'):
    carte = folium.Map(location=[(point_depart[0]+point_arrivee[0])/2, (point_depart[1]+point_arrivee[1])/2], zoom_start=14)

    # Ajouter les victimes et points neutres
    for point in donnees:
        if point['victime_detectee']:
            couleur = {'critique':'red', 'modéré':'orange', 'faible':'green'}[point['priorite']]
            folium.Marker(
                [point['latitude'], point['longitude']],
                popup=f"Victime : {point['priorite']}",
                icon=folium.Icon(color=couleur, icon='exclamation-sign')
            ).add_to(carte)

    # Marqueurs départ/arrivée et trajet du drone
    folium.Marker(point_depart, popup="Départ du drone", icon=folium.Icon(color='blue', icon='plane')).add_to(carte)
    folium.Marker(point_arrivee, popup="Arrivée du drone", icon=folium.Icon(color='purple', icon='flag')).add_to(carte)
    folium.PolyLine([point_depart, point_arrivee], color='black', weight=2.5, opacity=1).add_to(carte)

    carte.save(fichier)
    print(f"Carte avec trajet sauvegardée sous {fichier}")

# Simulation cohérente complète
def simulation():
    # Points réalistes (exemple: Montréal)
    point_depart = [45.51, -73.59]
    point_arrivee = [45.56, -73.54]

    donnees = generer_donnees_sur_trajet(point_depart, point_arrivee)

    # Stockage local des victimes
    victimes = [d for d in donnees if d['victime_detectee']]
    with open('stockage_local.json', 'w') as f:
        json.dump(victimes, f)

    # Générer carte interactive
    generer_carte_avec_trajet(donnees, point_depart, point_arrivee)

if __name__ == "__main__":
    simulation()
