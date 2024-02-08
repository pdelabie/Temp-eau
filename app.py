#IMPORT LIBRAIRIES
import streamlit as st 
import pandas as pd 
import numpy as np


#IMPORT DATA (détails)
#données plv filtrées sur eau rob et 37 (pour les infos de plv et com)
com = '/Users/perrine/Desktop/eaurob2023_37.csv'
df = pd.read_csv(com, delimiter = ',')

#données rslt filtrées sur eau rob et 37 (pour les résultats)
rslt = '/Users/perrine/Desktop/rslt_37.csv'
df1 = pd.read_csv(rslt, delimiter = ',')

#données rslt filtrées sur eau ditrib et 37 (pour avoir unite de ref)
dis = '/Users/perrine/Desktop/disresult2023_37.csv'
df2 = pd.read_csv(dis, delimiter = ',')
noms_colonnes = ['cdparametresiseeaux', 'libmajparametre', 'limitequal', 'refqual']
df2bis = df2.loc[:, noms_colonnes]

key_column1 = 'referenceprel'
merged_df = pd.merge(df, df1, on=key_column1, how='left')

key_column2 = 'cdparametresiseeaux'
final_df = pd.merge(merged_df, df2bis, on=key_column2, how='left')




#SIDE BAR :
with st.sidebar: 
    st.caption(" ")
    st.caption(" ")
    st.image('/Users/perrine/Downloads/Qualité de l’eau potable (3).png')
    st.caption(" ")
    st.caption(" ")
    st.caption(" ")
    
choice = st.sidebar.selectbox(
        'Sommaire',
        ('Contexte', 'La qualité de l\'eau, quésaco ?', 'Quelle est la situation chez moi ?', 'A propos')
)
with st.sidebar: 
    st.caption(" ")
    st.caption(" ")
    st.caption(" ")
    st.caption(" ")
    st.caption(" ")
    st.caption(" ")
    st.caption(" ")
    st.caption(" ")
    st.caption(" ")
    st.caption(" ")
    st.caption(" ")
    st.caption(" ")
    st.caption(" ")
    st.caption(" ")
    st.caption(" ")
    st.caption(" ")
    st.caption("Mots clés : Eau potable, Contrôle sanitaire, Qualité, Indre-et-Loire, France")
 

#PAGE INTRODUCTION
if choice == 'Contexte' :
    st.title(':blue[Temp\'eau]  🌍')
    st.caption(" ") 
    st.caption(" ") 
    st.header('Bienvenue sur Temp’eau, votre portail interactif vers la transparence de l\':blue[Eau Potable].')
    st.caption(" ") 
    st.caption("Dans un monde où l'accès à une eau de qualité devient une préoccupation majeure, notre application vous offre un aperçu de la qualité de l'eau en temps réel dans votre région.")
    st.caption("Explorez les analyses détaillées et restez informé(e) sur les paramètres cruciaux qui garantissent la sécurité de votre eau potable. Avec Temp’eau, nous mettons le pouvoir entre vos mains, vous permettant de prendre des décisions éclairées pour vous et votre communauté.") 
    st.caption("Il ne vous reste plus qu’à plongez dans les données 🌊💧")
    st.caption(" ")
    #INDICATORS
    st.subheader("Informations sur les données")
    col1, col2, col3 = st.columns(3)
    col1.metric("Source de données", "data.gouv", "Ministère des Solidarités et de la Santé")
    col2.metric("Mise à jour de la base de données", "Mensuelle")
    col3.metric("Localisation", "Indre-et-Loire (37) France")
    if st.button('Voir les données'):
     final_df
    else:
     st.write(' ')



# PAGE ET CHEZ MOI ALORS ?
if choice == 'Quelle est la situation chez moi ?' :
    st.title(':blue[Quelle est la situation chez moi ?]')
    st.caption(" ")
    st.caption(" ")
    
    # Sélecteur pour choisir une ville
    ville_selectionnee = st.selectbox("Choisissez une ville", final_df['nomcommune'].unique())
    
    # Filtrer les données en fonction de la ville sélectionnée
    df_filtre_ville = final_df[final_df['nomcommune'] == ville_selectionnee]
    
    # Mettre à jour la session_state avec les options possibles pour le deuxième sélecteur
    options_reseau = df_filtre_ville['nomreseau'].unique()
    if 'options_reseau' not in st.session_state:
        st.session_state.options_reseau = options_reseau
    
    # Sélecteur pour choisir un réseau après avoir sélectionné une ville
    reseau_selectionne = st.selectbox("Choisissez un réseau", options_reseau)

    # Filtrer les données en fonction de la ville et du réseau sélectionnés
    df_filtre_ville_reseau = df_filtre_ville[df_filtre_ville['nomreseau'] == reseau_selectionne]

    #Mettre à jour la session_state avec les options possibles pour le troisième sélecteur
    options_ptsurv = df_filtre_ville_reseau['nompointsurv'].unique()
    if 'options_ptsurv' not in st.session_state:
        st.session_state.options_ptsurv = options_ptsurv
    
    # Sélecteur pour choisir un réseau après avoir sélectionné une ville
    ptsurv_selectionne = st.selectbox("Choissisez un point de surveillance", options_ptsurv)

    # Filtrer les données en fonction de la ville et du réseau sélectionnés
    df_filtre_ville_reseau_pointsurv = df_filtre_ville_reseau[df_filtre_ville_reseau['nompointsurv'] == ptsurv_selectionne]

    # Trier le DataFrame par date de manière décroissante
    df_filtre_ville_reseau_trie = df_filtre_ville_reseau_pointsurv.sort_values(by='dateprel', ascending=False)
    
    # Sélectionner la première ligne qui correspondra à la date maximale
    df_filtre_max_date = df_filtre_ville_reseau_trie.head(1)
    
      # Vérifier les conditions pour afficher le message "CONFORME" ou "NON CONFORME"
    date_max = df_filtre_max_date['dateprel'].iloc[0]
    st.caption(" ")
    st.caption("(Les données affichées datent du "+date_max+')')
    st.write(" ")
    st.write(" ")
    st.write(" ")
    if (df_filtre_max_date['plvconformitechimique'].iloc[0] == "C" and 
        df_filtre_max_date['plvconformitebacterio'].iloc[0] == "C"):
            st.markdown('<h1 style="text-align: center; color: green;">CONFORME</h1>', unsafe_allow_html=True)
    else:
            st.markdown('<h1 style="text-align: center; color: red;">NON CONFORME</h1>', unsafe_allow_html=True)

# Filtrer df1 en fonction de la ville, du réseau et de la date la plus récente
    st.write(" ")
    st.write(" ")
    st.write(" ")
    st.write(" ")
    st.write(" ")
    st.write(" ")
    if st.button(":grey[Voir les résultats de l\'analyse]"):
        if final_df is not None:
            df_filtre_final_df = final_df[(final_df['nomcommune'] == ville_selectionnee) &
                            (final_df['nomreseau'] == reseau_selectionne) &
                            (final_df['nompointsurv'] == ptsurv_selectionne) &
                            (final_df['dateprel'] == df_filtre_max_date['dateprel'].iloc[0])]
        
        # Renommer les colonnes
            df_filtre_final_df = df_filtre_final_df.rename(columns={
                'cdparametresiseeaux': 'Paramètre analysé',
                'rqana': "Résultat de l'analyse",
                'cdunitereferencesiseeaux': 'Unité de référence',
                'libmajparametre': 'Détails paramètre', 
                'limitequal': 'Limites de qualité', 
                'refqual': 'Références de qualité',
            })
        
        # Afficher les résultats dans un tableau unique
            st.write(df_filtre_final_df[['Paramètre analysé', 'Détails paramètre', "Résultat de l'analyse", 'Unité de référence','Limites de qualité','Références de qualité']])
            st.write(" ")
            st.caption("Limites de qualité : Paramètres microbiologiques et chimiques auxquels les eaux doivent impérativement répondre")
            st.write(" ")
            st.caption("Références de qualité : Paramètres qui reflètent de la maîtrise des procédés de traitement et de distribution de l\'eau, qui permettent l\'évaluation des risques pour la santé et qui prennent en compte l\'agrément d\'usage de l\'eau pour les consommateurs")
        else:
            st.write('Aucun résultat disponible.')


 #PAGE LA QUALITE DE LEAU QUESACO ?
if choice == 'La qualité de l\'eau, quésaco ?' :
    st.title(':blue[La qualité de l\'eau, quésaco ?]')
    st.write(" ")
    st.write(" ")
    st.write("Le Ministère des Solidarités et de la Santé assure le contrôle de la qualité de l'eau potable distribuée par les réseaux publics en France. Ce contrôle vise à garantir la sécurité sanitaire de l'eau du robinet et à protéger la santé des consommateurs.")
    st.write(" ")
    st.caption("Les principales missions du contrôle de la qualité de l'eau du robinet comprennent :")
    st.caption("1. Surveillance régulière : Les autorités sanitaires effectuent une surveillance régulière de la qualité de l'eau potable, en prélevant des échantillons dans les réseaux de distribution et en les analysant dans des laboratoires agréés.")
    st.caption("2. Analyse des paramètres : Les échantillons d'eau sont analysés pour détecter la présence éventuelle de contaminants tels que les bactéries, les nitrates, les pesticides, les métaux lourds, les résidus de médicaments et autres substances chimiques.")
    st.caption("3. Respect des normes : Les résultats des analyses sont comparés aux normes de qualité de l'eau établies par la réglementation française et européenne. Ces normes fixent des seuils à ne pas dépasser pour chaque paramètre afin de garantir la sécurité sanitaire de l'eau du robinet.")
    st.caption("4. Information du public : Les résultats des analyses sont rendus publics et communiqués aux consommateurs via différents canaux, tels que les rapports annuels sur la qualité de l'eau, les sites web des autorités sanitaires et les campagnes d'information.")
    st.caption("5. Actions correctives : En cas de dépassement des normes de qualité de l'eau, des mesures correctives sont mises en place par les autorités sanitaires et les gestionnaires des réseaux de distribution pour remédier à la situation et garantir la qualité de l'eau du robinet.")
    st.caption("En résumé, le contrôle de la qualité de l'eau du robinet est une priorité pour les autorités sanitaires françaises afin de protéger la santé des consommateurs et de garantir l'accès à une eau potable sûre et de qualité.")



# PAGE A PROPOS
if choice == 'A propos' :
    st.title(':blue[A propos]')
    st.caption(" ")
    st.caption(" ")
    st.subheader('Merci pour votre soutien et votre partage !')
    st.caption("Temp\'eau une initiative bénévole basée sur l'open data, qui s'engage à vous informer gratuitement sur la qualité de l'eau que vous consommez au quotidien.💧🌍 ")
    st.caption(" ")
    st.caption(" ")
    col1, col2= st.columns(2)
    with col1 :
        st.caption('Je suis Perrine Delabie et je vous invite à me suivre sur les réseaux : ')
        if st.button('Github'):
            st.caption('https://github.com/pdelabie')
        if st.button('Linkedin'):
            st.caption('www.linkedin.com/in/perrine-delabie')
    with col2 :
        st.caption('N\'hésitez pas à partager votre avis sur ce sujet ! Vous pouvez m\'envoyer un message avec ce formulaire : ')
        contact_form_2 = """
                  <div class="container contact-form">
                      <form action="https://formsubmit.co/exemple@hotmail.com" method="POST">
                          <div class="row">
                              <div class="col-md-6">
                                  <div class="form-group">
                                      <input type="text" name="name" class="form-control" placeholder="Your Name *" required>
                                  </div>
                                  <div class="form-group">
                                      <input type="email" name="email" class="form-control" placeholder="Your Email *" required>
                                  </div>
                              <div class="form-group">
                                <input type="text" name="Phone number" class="form-control" placeholder="Your Phone Number *" required>
                            </div>
                              </div>
                              <div class="col-md-6">
                                  <div class="form-group">
                                      <textarea name="Message" class="form-control-message" placeholder="Your Message *" style="width: 330px; height: 220px;"></textarea>
                                  </div>
                                  <div class="form-group">
                                      <button type="submit" class="btnContact">Send Message</button>
                                  </div>
                              </div>
                          </div>
                      </form>
            </div> """
        st.markdown(contact_form_2, unsafe_allow_html=True)