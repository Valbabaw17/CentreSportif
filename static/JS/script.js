/************************************************
 *              PARTIE POS                      *
 *                                              *
*********************************************** */
/*Récupérer les les 3 vues diférentes de la patie POS avec leurs id*/
var vue_achats_divers = document.getElementById("vue_achats_divers");
var vue_abonnements = document.getElementById("vue_abonnements");
var vue_membres = document.getElementById("vue_membres");

/*Récupréer les 3 boutons donnant accès aux vues grâce à la classe boutons_vues*/
var boutons_vues = document.getElementById("boutons_vues");

/*Récupérer le bouton d'ajout de nouveau membre*/
var bouton_nouveau_membre = document.getElementById("bouton_nouveau_membre");

/*Vue Achats divers*/
function achats_divers(){
    boutons_vues.style.display = 'none';
    vue_achats_divers.style.display = 'inline';
}

/*Vue Abonnements*/
function abonnements(){
    boutons_vues.style.display = 'none';
    vue_abonnements.style.display = 'inline';

    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function(){
        if(this.readyState === 4 && this.status === 200){
            vue_abonnements.innerHTML = this.responseText;
        }
    };
    xhttp.open("GET","abonnements",true);
    xhttp.send();

}

/*Membres*/
function membres(){
    boutons_vues.style.display = 'none';
    vue_membres.style.dispay='inline';
    bouton_nouveau_membre.style.display='inline';
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function(){
        if(this.readyState === 4 && this.status === 200){
            vue_membres.innerHTML = this.responseText;
        }
    };
    xhttp.open("GET","infos_membres",true);
    xhttp.send();
}

/*Afficher le formulaire pour ajouter membre*/
function ajouter_membre(){
    vue_membres.style.dispay='none';
    bouton_nouveau_membre.style.display='none';
    document.getElementById("formulaire_inscription").style.display='inline';
}

/*Ajouter un membre dans la DB avec le formulaire*/
function ajouter_membre_db(){

}
/************************************************
 *              PARTIE COMPTABLE                *
 *                                              *
*********************************************** */



